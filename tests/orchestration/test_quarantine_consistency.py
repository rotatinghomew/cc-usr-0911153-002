from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from robot_corpus.control_plane import Application
from robot_corpus.orchestration.session_lifecycle import decide
from robot_corpus.session.contracts import DomainRecord
from robot_corpus.synchronization.timeline import alignment, coverage_gap_report, coverage_lattice


def session(record_id: str, *, robot: str, part: str, angle: float, skew: float) -> DomainRecord:
    return DomainRecord(record_id, {
        "robot_id": robot, "part_family": part, "grip_angle": angle, "deformation": 0,
        "illumination": 100, "dust_level": 0, "camera_fps": 30, "force_hz": 30,
        "clock_skew_ms": skew, "dropped_frames": 0, "operator_id": "op-1",
        "consent_scope": "training"})


class QuarantineCoverageConsistencyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.application = Application(Path(temporary.name) / "consistency.sqlite3")
        # Two robots; robot r2 only has a severely skewed session for its condition cell.
        self.healthy = session("s-healthy", robot="r1", part="axle", angle=0, skew=4)
        self.skewed = session("s-skewed", robot="r2", part="bracket", angle=60, skew=260)
        for record in (self.healthy, self.skewed):
            self.application.repository.save_record(record)

    def test_quarantined_fragment_cannot_inflate_coverage(self):
        self.assertFalse(alignment(self.healthy).quarantine)
        self.assertTrue(alignment(self.skewed).quarantine)
        report = self.application.coverage_report()
        # Only the healthy cell counts as usable; the skewed one stays an open gap.
        self.assertEqual(report["coverage"]["usable_cell_count"], 1.0)
        self.assertEqual(report["gaps"]["open_gap_cells"], 1)
        self.assertEqual(report["gaps"]["open_gaps"][0]["isolated_sessions"], ["s-skewed"])
        # Quarantine evidence is still retained for the audit trail.
        self.assertEqual([item["record_id"] for item in report["quarantine_evidence"]], ["s-skewed"])

    def test_reevaluation_reopens_gap_instead_of_just_lowering_score(self):
        before = self.application.coverage_report()
        self.assertEqual(before["gaps"]["open_gap_cells"], 1)
        # Re-adjudicating without correcting the data must keep the session isolated.
        result = self.application.reevaluate()
        self.assertEqual(result["reevaluated"]["s-skewed"], "quarantine")
        self.assertEqual(result["gaps"]["open_gap_cells"], 1)
        stored = self.application.repository.get_record("s-skewed")
        self.assertEqual(stored.state, "quarantined")

    def test_correction_recovers_the_cell_and_closes_the_gap(self):
        # Establish the quarantine first.
        self.application.reevaluate()
        self.assertEqual(self.application.repository.get_record("s-skewed").state, "quarantined")
        # Correct the clock skew and re-adjudicate the affected session.
        stored = self.application.repository.get_record("s-skewed")
        corrected = stored.with_payload({"clock_skew_ms": 6})
        self.application.repository.save_record(corrected, expected_version=stored.version)
        result = self.application.reevaluate(["s-skewed"])
        self.assertNotEqual(result["reevaluated"]["s-skewed"], "quarantine")
        self.assertEqual(result["gaps"]["open_gap_cells"], 0)
        self.assertEqual(result["coverage"]["usable_count"], 2.0)
        recovered = self.application.repository.get_record("s-skewed")
        self.assertIn(recovered.state, ("curated", "sealed"))

    def test_duplicate_fragments_partial_recovery_is_explained_per_unit(self):
        duplicate = session("s-duplicate", robot="r2", part="bracket", angle=60, skew=230)
        self.application.repository.save_record(duplicate)
        self.application.reevaluate()
        gaps = coverage_gap_report(self.application.repository.list_records())
        # Both isolated sessions land on the same cell, which remains open.
        target = next(unit for unit in gaps["units"] if unit["isolated_sessions"])
        self.assertEqual(sorted(target["isolated_sessions"]), ["s-duplicate", "s-skewed"])
        self.assertTrue(target["gap_open"])
        # Recover only one of the duplicates.
        stored = self.application.repository.get_record("s-skewed")
        self.application.repository.save_record(
            stored.with_payload({"clock_skew_ms": 5}), expected_version=stored.version)
        self.application.reevaluate(["s-skewed"])
        after = coverage_gap_report(self.application.repository.list_records())
        unit = next(unit for unit in after["units"]
                    if tuple(unit["condition"]) == (4, 0, 1, 0))
        self.assertFalse(unit["gap_open"])
        self.assertEqual(unit["usable_sessions"], ["s-skewed"])
        self.assertEqual(unit["isolated_sessions"], ["s-duplicate"])

    def test_gate_rejects_unsealed_session_and_manifest_tracks_usable_evidence(self):
        # Two adjudications move a non-quarantined session planned -> capturing -> curated.
        self.application.reevaluate()
        self.application.reevaluate()
        # The healthy session is curated after adjudication; the skewed one stays
        # quarantined. Publishing both is allowed (audit evidence retained) but only
        # the healthy session backs coverage.
        healthy_state = self.application.repository.get_record("s-healthy").state
        skewed_state = self.application.repository.get_record("s-skewed").state
        self.assertIn(healthy_state, ("curated", "sealed"))
        self.assertEqual(skewed_state, "quarantined")
        manifest = self.application.publish_dataset("batch-1", ["s-healthy", "s-skewed"])
        self.assertEqual(manifest["usable_item_count"], 1)
        self.assertEqual(manifest["quarantined_item_count"], 1)
        self.assertEqual(manifest["coverage"]["usable_count"], 1.0)

        # A brand new, still-planned session must be refused by the delivery gate.
        pending = session("s-pending", robot="r3", part="clamp", angle=15, skew=2)
        self.application.repository.save_record(pending)
        from robot_corpus.session.contracts import ContractError
        with self.assertRaisesRegex(ContractError, "admission"):
            self.application.publish_dataset("batch-x", ["s-healthy", "s-pending"])

    def test_review_opinion_keeps_sealed_basis_distinct(self):
        self.application.reevaluate()
        self.application.reevaluate()
        self.application.publish_dataset("batch-1", ["s-healthy", "s-skewed"])
        sealed_before = self.application.dataset_manifest("batch-1")
        # Correct the skewed session after sealing.
        stored = self.application.repository.get_record("s-skewed")
        self.application.repository.save_record(
            stored.with_payload({"clock_skew_ms": 5}), expected_version=stored.version)
        self.application.reevaluate(["s-skewed"])
        opinion = self.application.review_dataset("batch-1")
        # Sealed basis is untouched and still reports one usable session.
        self.assertEqual(self.application.dataset_manifest("batch-1"), sealed_before)
        self.assertEqual(sealed_before["coverage"]["usable_count"], 1.0)
        # The distinguishable review opinion records the recovery.
        review = next(item for item in opinion["session_reviews"] if item["session_id"] == "s-skewed")
        self.assertEqual(review["status"], "recovered")
        self.assertEqual(opinion["current_coverage"]["usable_count"], 2.0)
        self.assertNotEqual(opinion["opinion_hash"], sealed_before["snapshot_hash"])


class DecisionQuarantineTests(unittest.TestCase):
    def test_quarantine_outcome_overrides_synthetic_score(self):
        skewed = session("q", robot="r9", part="x", angle=45, skew=300)
        decision = decide(skewed)
        self.assertEqual(decision.outcome, "quarantine")
        self.assertTrue(any("quarantine=" in reason for reason in decision.reasons))
        self.assertEqual(decision.metrics["alignment_quarantine"], 1.0)

    def test_hold_does_not_jump_to_superseded(self):
        from robot_corpus.orchestration.session_lifecycle import advance_for_outcome
        healthy = session("h", robot="r9", part="x", angle=0, skew=1)
        decision = decide(healthy)
        advanced = advance_for_outcome(healthy, decision)
        self.assertNotEqual(advanced.state, "superseded")


if __name__ == "__main__":
    unittest.main()
