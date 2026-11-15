from __future__ import annotations

import unittest
from robot_corpus.session.contracts import DomainRecord
from robot_corpus.synchronization.timeline import alignment, condition_cell, coverage_lattice, sequence_health


class TimelineTests(unittest.TestCase):
    def record(self, key, skew=5, drops=0):
        return DomainRecord(key, {"robot_id": "r1", "part_family": "axle", "grip_angle": 32, "deformation": 4,
            "illumination": 500, "dust_level": 8, "camera_fps": 30, "force_hz": 100,
            "clock_skew_ms": skew, "dropped_frames": drops, "operator_id": "op", "consent_scope": "training"})

    def test_large_skew_quarantines(self):
        self.assertFalse(alignment(self.record("a")).quarantine)
        self.assertTrue(alignment(self.record("b", skew=220)).quarantine)

    def test_lattice_and_sequence_health(self):
        rows = [self.record("a"), self.record("b", drops=900)]
        self.assertEqual(len(condition_cell(rows[0])), 4)
        self.assertGreater(coverage_lattice(rows)["cell_count"], 0)
        self.assertEqual(sequence_health(rows)["quarantined"], 1.0)
