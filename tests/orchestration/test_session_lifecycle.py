from __future__ import annotations

import math
import tempfile
import unittest
from pathlib import Path

from robot_corpus.session.contracts import ContractError, DomainRecord, RuleResult, bounded, stable_hash
from robot_corpus.synchronization.quality_gates import RULE_INDEX, evaluate, summarize
from robot_corpus.curation.coverage_map import METRICS, compare, grouped_metrics, metric_vector, portfolio, record_score

FIELDS = ['robot_id', 'part_family', 'grip_angle', 'deformation', 'illumination', 'dust_level', 'camera_fps', 'force_hz', 'clock_skew_ms', 'dropped_frames', 'operator_id', 'consent_scope']

def make_record(seed: int = 1, state: str | None = None) -> DomainRecord:
    payload = {}
    for index, field in enumerate(FIELDS):
        selector = (seed + index) % 4
        if selector == 0:
            payload[field] = seed * 9.5 + index * 1.25
        elif selector == 1:
            payload[field] = f'{field}-{seed % 5}'
        elif selector == 2:
            payload[field] = (seed + index) / 10.0
        else:
            payload[field] = (seed + index) % 2 == 0
    return DomainRecord(f'capture_session-{seed:03d}', payload, state or 'planned')

class RuleGroup3Tests(unittest.TestCase):
    def test_evaluate_returns_complete_catalog(self):
        record = make_record()
        results = evaluate(record, {})
        self.assertEqual(len(results), len(RULE_INDEX))
        self.assertTrue(all(isinstance(item, RuleResult) for item in results))
        self.assertTrue(all(0.0 <= item.score <= 1.0 for item in results))

    def test_summary_is_conservative_and_counted(self):
        results = evaluate(make_record(2), {'risk_weight': 0.8})
        summary = summarize(results)
        self.assertEqual(summary['passed'] + summary['failed'], len(results))
        self.assertGreaterEqual(summary['critical'], 0)
        self.assertGreaterEqual(summary['score'], 0.0)
        self.assertLessEqual(summary['score'], 1.0)

    def test_check_camera_fps_presence_03_01(self):
        record = make_record(5)
        result = RULE_INDEX['check_camera_fps_presence'](record, {'check_camera_fps_presence_threshold': 1.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_presence')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_range_03_02(self):
        record = make_record(6)
        result = RULE_INDEX['check_camera_fps_range'](record, {'check_camera_fps_range_threshold': 2.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_range')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_stability_03_03(self):
        record = make_record(7)
        result = RULE_INDEX['check_camera_fps_stability'](record, {'check_camera_fps_stability_threshold': 3.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_stability')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_freshness_03_04(self):
        record = make_record(8)
        result = RULE_INDEX['check_camera_fps_freshness'](record, {'check_camera_fps_freshness_threshold': 4.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_freshness')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_coverage_03_05(self):
        record = make_record(9)
        result = RULE_INDEX['check_camera_fps_coverage'](record, {'check_camera_fps_coverage_threshold': 5.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_coverage')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_consistency_03_06(self):
        record = make_record(10)
        result = RULE_INDEX['check_camera_fps_consistency'](record, {'check_camera_fps_consistency_threshold': 6.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_consistency')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_risk_03_07(self):
        record = make_record(11)
        result = RULE_INDEX['check_camera_fps_risk'](record, {'check_camera_fps_risk_threshold': 7.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_risk')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_confidence_03_08(self):
        record = make_record(12)
        result = RULE_INDEX['check_camera_fps_confidence'](record, {'check_camera_fps_confidence_threshold': 8.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_confidence')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_dependency_03_09(self):
        record = make_record(13)
        result = RULE_INDEX['check_camera_fps_dependency'](record, {'check_camera_fps_dependency_threshold': 9.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_dependency')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_camera_fps_readiness_03_10(self):
        record = make_record(14)
        result = RULE_INDEX['check_camera_fps_readiness'](record, {'check_camera_fps_readiness_threshold': 1.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_camera_fps_readiness')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_presence_03_11(self):
        record = make_record(15)
        result = RULE_INDEX['check_force_hz_presence'](record, {'check_force_hz_presence_threshold': 2.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_presence')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_range_03_12(self):
        record = make_record(16)
        result = RULE_INDEX['check_force_hz_range'](record, {'check_force_hz_range_threshold': 3.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_range')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_stability_03_13(self):
        record = make_record(17)
        result = RULE_INDEX['check_force_hz_stability'](record, {'check_force_hz_stability_threshold': 4.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_stability')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_freshness_03_14(self):
        record = make_record(18)
        result = RULE_INDEX['check_force_hz_freshness'](record, {'check_force_hz_freshness_threshold': 5.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_freshness')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_coverage_03_15(self):
        record = make_record(19)
        result = RULE_INDEX['check_force_hz_coverage'](record, {'check_force_hz_coverage_threshold': 6.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_coverage')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_consistency_03_16(self):
        record = make_record(20)
        result = RULE_INDEX['check_force_hz_consistency'](record, {'check_force_hz_consistency_threshold': 7.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_consistency')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_risk_03_17(self):
        record = make_record(21)
        result = RULE_INDEX['check_force_hz_risk'](record, {'check_force_hz_risk_threshold': 8.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_risk')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_confidence_03_18(self):
        record = make_record(22)
        result = RULE_INDEX['check_force_hz_confidence'](record, {'check_force_hz_confidence_threshold': 9.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_confidence')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_dependency_03_19(self):
        record = make_record(23)
        result = RULE_INDEX['check_force_hz_dependency'](record, {'check_force_hz_dependency_threshold': 1.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_dependency')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_force_hz_readiness_03_20(self):
        record = make_record(24)
        result = RULE_INDEX['check_force_hz_readiness'](record, {'check_force_hz_readiness_threshold': 2.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_force_hz_readiness')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_presence_03_21(self):
        record = make_record(25)
        result = RULE_INDEX['check_clock_skew_ms_presence'](record, {'check_clock_skew_ms_presence_threshold': 3.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_presence')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_range_03_22(self):
        record = make_record(26)
        result = RULE_INDEX['check_clock_skew_ms_range'](record, {'check_clock_skew_ms_range_threshold': 4.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_range')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_stability_03_23(self):
        record = make_record(27)
        result = RULE_INDEX['check_clock_skew_ms_stability'](record, {'check_clock_skew_ms_stability_threshold': 5.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_stability')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_freshness_03_24(self):
        record = make_record(28)
        result = RULE_INDEX['check_clock_skew_ms_freshness'](record, {'check_clock_skew_ms_freshness_threshold': 6.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_freshness')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_coverage_03_25(self):
        record = make_record(29)
        result = RULE_INDEX['check_clock_skew_ms_coverage'](record, {'check_clock_skew_ms_coverage_threshold': 7.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_coverage')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_consistency_03_26(self):
        record = make_record(30)
        result = RULE_INDEX['check_clock_skew_ms_consistency'](record, {'check_clock_skew_ms_consistency_threshold': 8.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_consistency')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_risk_03_27(self):
        record = make_record(31)
        result = RULE_INDEX['check_clock_skew_ms_risk'](record, {'check_clock_skew_ms_risk_threshold': 9.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_risk')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_confidence_03_28(self):
        record = make_record(32)
        result = RULE_INDEX['check_clock_skew_ms_confidence'](record, {'check_clock_skew_ms_confidence_threshold': 1.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_confidence')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_dependency_03_29(self):
        record = make_record(33)
        result = RULE_INDEX['check_clock_skew_ms_dependency'](record, {'check_clock_skew_ms_dependency_threshold': 2.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_dependency')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

    def test_check_clock_skew_ms_readiness_03_30(self):
        record = make_record(34)
        result = RULE_INDEX['check_clock_skew_ms_readiness'](record, {'check_clock_skew_ms_readiness_threshold': 3.0})
        self.assertIsInstance(result, RuleResult)
        self.assertEqual(result.code, 'check_clock_skew_ms_readiness')
        self.assertIn(result.severity, {'info', 'warning', 'error', 'critical'})
        self.assertTrue(math.isfinite(result.score))
        self.assertIn('field', result.evidence)
        self.assertIn('threshold', result.evidence)

class MetricGroup3Tests(unittest.TestCase):
    def test_metric_vector_is_deterministic(self):
        record = make_record(11)
        first = metric_vector(record, {})
        second = metric_vector(record, {})
        self.assertEqual(first, second)
        self.assertEqual(set(first), set(METRICS))
        self.assertTrue(all(0.0 <= value <= 1.0 for value in first.values()))

    def test_grouped_metrics_match_business_catalog(self):
        grouped = grouped_metrics(make_record(4), {})
        self.assertEqual(set(grouped), {'dataset_novelty', 'reuse_readiness', 'quarantine_pressure', 'condition_coverage', 'sequence_integrity', 'operator_balance', 'sensor_alignment', 'lineage_completeness'})
        self.assertTrue(all(math.isfinite(value) for value in grouped.values()))

    def test_portfolio_orders_by_descending_score(self):
        result = portfolio([make_record(2), make_record(3), make_record(4)])
        scores = [row['score'] for row in result['rows']]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertEqual(result['count'], 3)
        self.assertGreaterEqual(result['maximum'], result['minimum'])

    def test_compare_has_all_metric_deltas(self):
        result = compare(make_record(5), make_record(6))
        self.assertEqual(set(result['delta']), {'dataset_novelty', 'reuse_readiness', 'quarantine_pressure', 'condition_coverage', 'sequence_integrity', 'operator_balance', 'sensor_alignment', 'lineage_completeness'})
        self.assertIn(result['winner'], {make_record(5).record_id, make_record(6).record_id})

    def test_score_fingerprint_changes_with_payload(self):
        left = record_score(make_record(7))
        right = record_score(make_record(8))
        self.assertNotEqual(left['fingerprint'], right['fingerprint'])
        self.assertNotEqual(stable_hash(left['metrics']), stable_hash(right['metrics']))

if __name__ == '__main__':
    unittest.main()
