from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from robot_corpus.control_plane import Application
from robot_corpus.orchestration.session_lifecycle import (
    advance_for_outcome, apply_transition, decide,
)
from robot_corpus.session.contracts import ContractError, DomainRecord
from robot_corpus.synchronization.timeline import (
    alignment, condition_cell, coverage_gap_report, coverage_lattice, quarantine_reasons,
)


def admit(application: Application, record: DomainRecord) -> DomainRecord:
    """Drive a session through the real workflow to its publishable/isolated state."""
    current = application.repository.get_record(record.record_id) or record
    decision = decide(current)
    advanced = advance_for_outcome(current, decision)
    if advanced.fingerprint != current.fingerprint:
        application.repository.save_record(advanced, expected_version=current.version)
        current = advanced
    if current.state in ("quarantined", "curated", "sealed"):
        return current
    # Healthy sessions proceed through the adjacent transition planner.
    for target in ("capturing", "curated"):
        stored = application.repository.get_record(current.record_id)
        if stored.state == target:
            current = stored
            continue
        moved = apply_transition(stored, target, {"transition_threshold": 0.0})
        application.repository.save_record(moved, expected_version=stored.version)
        current = moved
    return current


class SealedDatasetTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.application = Application(Path(temporary.name) / "capture.sqlite3")
        self.good = DomainRecord("healthy", {"robot_id": "r1", "part_family": "axle",
            "grip_angle": 0, "deformation": 0, "illumination": 100, "dust_level": 0,
            "camera_fps": 30, "force_hz": 30, "clock_skew_ms": 0, "dropped_frames": 0})
        self.bad = DomainRecord("isolated", dict(self.good.payload) | {
            "grip_angle": 60, "clock_skew_ms": 250})
        self.application.repository.save_record(self.good)
        self.application.repository.save_record(self.bad)
        self.healthy = admit(self.application, self.good)
        self.isolated = admit(self.application, self.bad)

    def test_quarantine_evidence_is_retained_but_does_not_back_coverage(self):
        self.assertTrue(alignment(self.bad).quarantine)
        self.assertEqual(self.isolated.state, "quarantined")
        manifest = self.application.publish_dataset("batch-a", ["isolated", "healthy"])
        self.assertEqual(manifest["item_count"], 2)
        self.assertEqual(manifest["usable_item_count"], 1)
        self.assertEqual(manifest["quarantined_item_count"], 1)
        self.assertEqual([item["quarantined"] for item in manifest["items"]], [False, True])
        # Coverage must be computed from the healthy session alone.
        self.assertEqual(manifest["coverage"], coverage_lattice([self.good, self.bad]))
        self.assertEqual(manifest["coverage"]["cell_count"], 1.0)
        self.assertEqual(manifest["coverage"]["usable_count"], 1.0)
        self.assertEqual(manifest["coverage"]["quarantined_count"], 1.0)
        # Audit evidence (reasons) stays attached to the isolated item.
        isolated_item = next(item for item in manifest["items"] if item["session_id"] == "isolated")
        self.assertTrue(isolated_item["quarantine_reasons"])
        self.assertEqual(self.application.publish_dataset("batch-a", ["healthy", "isolated"]), manifest)

    def test_gate_and_manifest_point_at_the_same_usable_evidence(self):
        manifest = self.application.publish_dataset("batch-a", ["healthy", "isolated"])
        usable_sessions = {item["session_id"] for item in manifest["items"] if not item["quarantined"]}
        self.assertEqual(usable_sessions, {"healthy"})
        self.assertEqual(manifest["usable_item_count"], len(usable_sessions))
        self.assertEqual(manifest["coverage"]["usable_count"], float(len(usable_sessions)))

    def test_unadmitted_session_cannot_be_sealed(self):
        pending = DomainRecord("pending", dict(self.good.payload) | {"robot_id": "r2"})
        self.application.repository.save_record(pending)  # stays in planned
        with self.assertRaisesRegex(ContractError, "admission"):
            self.application.publish_dataset("invalid", ["healthy", "pending"])

    def test_seal_immutability_and_corrected_quality_history(self):
        manifest = self.application.publish_dataset("batch-a", ["healthy", "isolated"])
        self.assertEqual(manifest["coverage"]["usable_count"], 1.0)
        stored_isolated = self.application.repository.get_record("isolated")
        corrected = stored_isolated.with_payload({"clock_skew_ms": 0})
        self.application.repository.save_record(corrected, expected_version=stored_isolated.version)
        with self.assertRaisesRegex(ContractError, "cannot change"):
            self.application.publish_dataset("batch-a", ["healthy", "isolated"])
        admitted = admit(self.application, corrected)
        self.assertIn(admitted.state, ("curated", "sealed"))
        current = self.application.publish_dataset("batch-b", ["healthy", "isolated"])
        isolated_item = next(item for item in current["items"] if item["session_id"] == "isolated")
        self.assertGreater(isolated_item["session_version"], stored_isolated.version)
        self.assertFalse(isolated_item["quarantined"])
        self.assertEqual(current["coverage"]["usable_count"], 2.0)
        # The original sealed dataset keeps the quality basis adopted at publication.
        reread = self.application.dataset_manifest("batch-a")
        self.assertEqual(reread, manifest)
        self.assertEqual(reread["coverage"]["usable_count"], 1.0)
        self.assertIsNotNone(reread["quality_basis"])

    def test_review_opinion_is_distinguishable_from_sealed_basis(self):
        self.application.publish_dataset("batch-a", ["healthy", "isolated"])
        stored_isolated = self.application.repository.get_record("isolated")
        corrected = stored_isolated.with_payload({"clock_skew_ms": 0})
        self.application.repository.save_record(corrected, expected_version=stored_isolated.version)
        opinion = self.application.review_dataset("batch-a")
        self.assertIn("review", opinion["review_kind"])
        self.assertEqual(opinion["sealed_snapshot_hash"],
                         self.application.dataset_manifest("batch-a")["snapshot_hash"])
        review = next(item for item in opinion["session_reviews"] if item["session_id"] == "isolated")
        self.assertEqual(review["status"], "recovered")
        self.assertFalse(review["current_quarantined"])
        self.assertIn("isolated", opinion["recovered_sessions"])
        # The sealed manifest itself is untouched by the review.
        sealed = self.application.dataset_manifest("batch-a")
        isolated_item = next(item for item in sealed["items"] if item["session_id"] == "isolated")
        self.assertTrue(isolated_item["quarantined"])

    def test_unknown_session_cannot_be_sealed(self):
        with self.assertRaisesRegex(ContractError, "unknown"):
            self.application.publish_dataset("invalid", ["healthy", "missing"])


class CoverageGapTests(unittest.TestCase):
    def _record(self, key, robot="r1", part="axle", angle=0, skew=0):
        return DomainRecord(key, {"robot_id": robot, "part_family": part,
            "grip_angle": angle, "deformation": 0, "illumination": 100, "dust_level": 0,
            "camera_fps": 30, "force_hz": 30, "clock_skew_ms": skew, "dropped_frames": 0})

    def test_quarantined_only_cell_stays_an_open_gap(self):
        healthy = self._record("ok", angle=0)
        isolated = self._record("bad", robot="r2", angle=60, skew=250)
        report = coverage_gap_report([healthy, isolated])
        self.assertEqual(report["open_gap_cells"], 1)
        open_unit = report["open_gaps"][0]
        self.assertEqual(open_unit["isolated_sessions"], ["bad"])
        self.assertEqual(open_unit["usable_sessions"], [])
        # The same isolated session must not count toward usable coverage.
        lattice = coverage_lattice([healthy, isolated])
        self.assertEqual(lattice["usable_cell_count"], 1.0)
        self.assertEqual(lattice["audit_cell_count"], 2.0)

    def test_partial_recovery_fills_the_cell_without_dropping_audit_evidence(self):
        healthy = self._record("ok", angle=0)
        isolated_a = self._record("iso-a", robot="r2", angle=60, skew=250)
        isolated_b = self._record("iso-b", robot="r2", angle=60, skew=220)
        before = coverage_gap_report([healthy, isolated_a, isolated_b])
        self.assertEqual(before["open_gap_cells"], 1)
        # One duplicate recovers; the other remains isolated.
        recovered = isolated_a.with_payload({"clock_skew_ms": 0})
        after = coverage_gap_report([healthy, recovered, isolated_b])
        self.assertEqual(after["open_gap_cells"], 0)
        filled = next(unit for unit in after["units"] if tuple(unit["condition"]) == condition_cell(recovered))
        self.assertEqual(filled["usable_sessions"], ["iso-a"])
        self.assertEqual(filled["isolated_sessions"], ["iso-b"])

    def test_multi_robot_report_names_filled_and_unfilled_units(self):
        rows = [self._record("a", robot="r1", angle=0),
                self._record("b", robot="r2", angle=15),
                self._record("c", robot="r3", angle=30, skew=260)]
        report = coverage_gap_report(rows)
        self.assertEqual(report["filled_cells"], 2)
        self.assertEqual(report["open_gap_cells"], 1)
        self.assertEqual(report["open_gaps"][0]["isolated_sessions"], ["c"])
        self.assertTrue(quarantine_reasons(rows[2]))
        self.assertFalse(quarantine_reasons(rows[0]))


if __name__ == "__main__":
    unittest.main()
