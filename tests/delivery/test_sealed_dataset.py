from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from robot_corpus.control_plane import Application
from robot_corpus.session.contracts import ContractError, DomainRecord
from robot_corpus.synchronization.timeline import coverage_lattice


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

    def test_seal_preserves_quality_provenance_and_coverage_snapshot(self):
        manifest = self.application.publish_dataset("batch-a", ["isolated", "healthy"])
        self.assertEqual(manifest["item_count"], 2)
        self.assertEqual([item["quarantined"] for item in manifest["items"]], [False, True])
        self.assertEqual(manifest["coverage"], coverage_lattice([self.good, self.bad]))
        self.assertEqual(self.application.publish_dataset("batch-a", ["healthy", "isolated"]), manifest)

    def test_seal_immutability_and_corrected_quality_history(self):
        manifest = self.application.publish_dataset("batch-a", ["healthy", "isolated"])
        corrected = self.bad.with_payload({"clock_skew_ms": 0})
        self.application.repository.save_record(corrected, expected_version=1)
        with self.assertRaisesRegex(ContractError, "cannot change"):
            self.application.publish_dataset("batch-a", ["healthy", "isolated"])
        current = self.application.publish_dataset("batch-b", ["healthy", "isolated"])
        self.assertEqual(current["items"][1]["session_version"], 2)
        self.assertFalse(current["items"][1]["quarantined"])
        self.assertEqual(self.application.dataset_manifest("batch-a"), manifest)

    def test_unknown_session_cannot_be_sealed(self):
        with self.assertRaisesRegex(ContractError, "unknown"):
            self.application.publish_dataset("invalid", ["healthy", "missing"])
