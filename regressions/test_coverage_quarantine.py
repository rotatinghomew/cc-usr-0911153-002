import unittest

from robot_corpus.session.contracts import DomainRecord
from robot_corpus.synchronization.timeline import alignment, coverage_lattice


class CoverageQuarantineTests(unittest.TestCase):
    def test_quarantined_condition_does_not_fill_training_cell(self):
        good = DomainRecord("good", {
            "robot_id": "robot-a", "part_family": "part-a", "clock_skew_ms": 0,
            "camera_fps": 30, "force_hz": 30, "dropped_frames": 0,
            "grip_angle": 0, "deformation": 5, "illumination": 100, "dust_level": 1,
        }, "planned")
        late = DomainRecord("late", {
            **good.payload, "clock_skew_ms": 250, "grip_angle": 60,
        }, "planned")
        self.assertTrue(alignment(late).quarantine)
        self.assertEqual(coverage_lattice([good, late])["coverage"],
                         coverage_lattice([good])["coverage"])
        self.assertEqual(coverage_lattice([good, late])["quarantine_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
