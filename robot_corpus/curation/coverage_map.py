from __future__ import annotations

import math
import statistics
from collections import defaultdict
from typing import Any, Callable, Iterable, Mapping

from robot_corpus.session.contracts import DomainRecord, bounded, finite_number, normalized_text, stable_hash
from robot_corpus.synchronization.quality_gates import evaluate, summarize

MetricFunction = Callable[[DomainRecord, Mapping[str, Any]], float]

def _value(record: DomainRecord, field: str) -> float:
    value = record.payload.get(field)
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return finite_number(value)
    text = normalized_text(value)
    return float(sum((index + 1) * ord(ch) for index, ch in enumerate(text)) % 997) / 10.0

def _signal(record: DomainRecord, fields: tuple[str, ...], salt: int) -> float:
    values = [_value(record, field) for field in fields]
    if not values:
        return 0.0
    center = statistics.fmean(values)
    spread = statistics.pstdev(values) if len(values) > 1 else 0.0
    harmonic = sum(math.sin(value / (salt + 1)) + math.cos(value * (salt + 1) / 17.0) for value in values)
    return bounded(0.5 + math.tanh((center - spread + harmonic) / (30.0 + salt)) / 2.0)

def metric_sensor_alignment_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('robot_id', 'deformation', 'camera_fps', 'dropped_frames'), 1)
    weight = finite_number(context.get('sensor_alignment_weight', 0.7))
    offset = finite_number(context.get('metric_sensor_alignment_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_sensor_alignment_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('part_family', 'illumination', 'force_hz', 'operator_id'), 2)
    weight = finite_number(context.get('sensor_alignment_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_sensor_alignment_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_sensor_alignment_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('grip_angle', 'dust_level', 'clock_skew_ms', 'consent_scope'), 3)
    weight = finite_number(context.get('sensor_alignment_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_sensor_alignment_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_sensor_alignment_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('deformation', 'camera_fps', 'dropped_frames', 'robot_id'), 4)
    weight = finite_number(context.get('sensor_alignment_weight', 1.0))
    offset = finite_number(context.get('metric_sensor_alignment_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_sensor_alignment_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('illumination', 'force_hz', 'operator_id', 'part_family'), 5)
    weight = finite_number(context.get('sensor_alignment_weight', 0.7))
    offset = finite_number(context.get('metric_sensor_alignment_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_sensor_alignment_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dust_level', 'clock_skew_ms', 'consent_scope', 'grip_angle'), 6)
    weight = finite_number(context.get('sensor_alignment_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_sensor_alignment_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_sensor_alignment_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('camera_fps', 'dropped_frames', 'robot_id', 'deformation'), 7)
    weight = finite_number(context.get('sensor_alignment_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_sensor_alignment_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_sensor_alignment_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('force_hz', 'operator_id', 'part_family', 'illumination'), 8)
    weight = finite_number(context.get('sensor_alignment_weight', 1.0))
    offset = finite_number(context.get('metric_sensor_alignment_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_sensor_alignment_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('clock_skew_ms', 'consent_scope', 'grip_angle', 'dust_level'), 9)
    weight = finite_number(context.get('sensor_alignment_weight', 0.7))
    offset = finite_number(context.get('metric_sensor_alignment_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_sensor_alignment_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dropped_frames', 'robot_id', 'deformation', 'camera_fps'), 10)
    weight = finite_number(context.get('sensor_alignment_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_sensor_alignment_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_condition_coverage_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('part_family', 'illumination', 'force_hz', 'operator_id'), 2)
    weight = finite_number(context.get('condition_coverage_weight', 0.7))
    offset = finite_number(context.get('metric_condition_coverage_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_condition_coverage_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('grip_angle', 'dust_level', 'clock_skew_ms', 'consent_scope'), 3)
    weight = finite_number(context.get('condition_coverage_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_condition_coverage_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_condition_coverage_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('deformation', 'camera_fps', 'dropped_frames', 'robot_id'), 4)
    weight = finite_number(context.get('condition_coverage_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_condition_coverage_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_condition_coverage_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('illumination', 'force_hz', 'operator_id', 'part_family'), 5)
    weight = finite_number(context.get('condition_coverage_weight', 1.0))
    offset = finite_number(context.get('metric_condition_coverage_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_condition_coverage_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dust_level', 'clock_skew_ms', 'consent_scope', 'grip_angle'), 6)
    weight = finite_number(context.get('condition_coverage_weight', 0.7))
    offset = finite_number(context.get('metric_condition_coverage_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_condition_coverage_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('camera_fps', 'dropped_frames', 'robot_id', 'deformation'), 7)
    weight = finite_number(context.get('condition_coverage_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_condition_coverage_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_condition_coverage_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('force_hz', 'operator_id', 'part_family', 'illumination'), 8)
    weight = finite_number(context.get('condition_coverage_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_condition_coverage_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_condition_coverage_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('clock_skew_ms', 'consent_scope', 'grip_angle', 'dust_level'), 9)
    weight = finite_number(context.get('condition_coverage_weight', 1.0))
    offset = finite_number(context.get('metric_condition_coverage_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_condition_coverage_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dropped_frames', 'robot_id', 'deformation', 'camera_fps'), 10)
    weight = finite_number(context.get('condition_coverage_weight', 0.7))
    offset = finite_number(context.get('metric_condition_coverage_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_condition_coverage_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_id', 'part_family', 'illumination', 'force_hz'), 11)
    weight = finite_number(context.get('condition_coverage_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_condition_coverage_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_sequence_integrity_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('grip_angle', 'dust_level', 'clock_skew_ms', 'consent_scope'), 3)
    weight = finite_number(context.get('sequence_integrity_weight', 0.7))
    offset = finite_number(context.get('metric_sequence_integrity_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_sequence_integrity_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('deformation', 'camera_fps', 'dropped_frames', 'robot_id'), 4)
    weight = finite_number(context.get('sequence_integrity_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_sequence_integrity_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_sequence_integrity_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('illumination', 'force_hz', 'operator_id', 'part_family'), 5)
    weight = finite_number(context.get('sequence_integrity_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_sequence_integrity_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_sequence_integrity_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dust_level', 'clock_skew_ms', 'consent_scope', 'grip_angle'), 6)
    weight = finite_number(context.get('sequence_integrity_weight', 1.0))
    offset = finite_number(context.get('metric_sequence_integrity_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_sequence_integrity_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('camera_fps', 'dropped_frames', 'robot_id', 'deformation'), 7)
    weight = finite_number(context.get('sequence_integrity_weight', 0.7))
    offset = finite_number(context.get('metric_sequence_integrity_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_sequence_integrity_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('force_hz', 'operator_id', 'part_family', 'illumination'), 8)
    weight = finite_number(context.get('sequence_integrity_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_sequence_integrity_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_sequence_integrity_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('clock_skew_ms', 'consent_scope', 'grip_angle', 'dust_level'), 9)
    weight = finite_number(context.get('sequence_integrity_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_sequence_integrity_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_sequence_integrity_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dropped_frames', 'robot_id', 'deformation', 'camera_fps'), 10)
    weight = finite_number(context.get('sequence_integrity_weight', 1.0))
    offset = finite_number(context.get('metric_sequence_integrity_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_sequence_integrity_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_id', 'part_family', 'illumination', 'force_hz'), 11)
    weight = finite_number(context.get('sequence_integrity_weight', 0.7))
    offset = finite_number(context.get('metric_sequence_integrity_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_sequence_integrity_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consent_scope', 'grip_angle', 'dust_level', 'clock_skew_ms'), 12)
    weight = finite_number(context.get('sequence_integrity_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_sequence_integrity_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_operator_balance_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('deformation', 'camera_fps', 'dropped_frames', 'robot_id'), 4)
    weight = finite_number(context.get('operator_balance_weight', 0.7))
    offset = finite_number(context.get('metric_operator_balance_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_operator_balance_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('illumination', 'force_hz', 'operator_id', 'part_family'), 5)
    weight = finite_number(context.get('operator_balance_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_operator_balance_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_operator_balance_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dust_level', 'clock_skew_ms', 'consent_scope', 'grip_angle'), 6)
    weight = finite_number(context.get('operator_balance_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_operator_balance_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_operator_balance_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('camera_fps', 'dropped_frames', 'robot_id', 'deformation'), 7)
    weight = finite_number(context.get('operator_balance_weight', 1.0))
    offset = finite_number(context.get('metric_operator_balance_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_operator_balance_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('force_hz', 'operator_id', 'part_family', 'illumination'), 8)
    weight = finite_number(context.get('operator_balance_weight', 0.7))
    offset = finite_number(context.get('metric_operator_balance_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_operator_balance_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('clock_skew_ms', 'consent_scope', 'grip_angle', 'dust_level'), 9)
    weight = finite_number(context.get('operator_balance_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_operator_balance_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_operator_balance_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dropped_frames', 'robot_id', 'deformation', 'camera_fps'), 10)
    weight = finite_number(context.get('operator_balance_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_operator_balance_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_operator_balance_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_id', 'part_family', 'illumination', 'force_hz'), 11)
    weight = finite_number(context.get('operator_balance_weight', 1.0))
    offset = finite_number(context.get('metric_operator_balance_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_operator_balance_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consent_scope', 'grip_angle', 'dust_level', 'clock_skew_ms'), 12)
    weight = finite_number(context.get('operator_balance_weight', 0.7))
    offset = finite_number(context.get('metric_operator_balance_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_operator_balance_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('robot_id', 'deformation', 'camera_fps', 'dropped_frames'), 13)
    weight = finite_number(context.get('operator_balance_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_operator_balance_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('illumination', 'force_hz', 'operator_id', 'part_family'), 5)
    weight = finite_number(context.get('quarantine_pressure_weight', 0.7))
    offset = finite_number(context.get('metric_quarantine_pressure_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dust_level', 'clock_skew_ms', 'consent_scope', 'grip_angle'), 6)
    weight = finite_number(context.get('quarantine_pressure_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_quarantine_pressure_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('camera_fps', 'dropped_frames', 'robot_id', 'deformation'), 7)
    weight = finite_number(context.get('quarantine_pressure_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_quarantine_pressure_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('force_hz', 'operator_id', 'part_family', 'illumination'), 8)
    weight = finite_number(context.get('quarantine_pressure_weight', 1.0))
    offset = finite_number(context.get('metric_quarantine_pressure_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('clock_skew_ms', 'consent_scope', 'grip_angle', 'dust_level'), 9)
    weight = finite_number(context.get('quarantine_pressure_weight', 0.7))
    offset = finite_number(context.get('metric_quarantine_pressure_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dropped_frames', 'robot_id', 'deformation', 'camera_fps'), 10)
    weight = finite_number(context.get('quarantine_pressure_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_quarantine_pressure_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_id', 'part_family', 'illumination', 'force_hz'), 11)
    weight = finite_number(context.get('quarantine_pressure_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_quarantine_pressure_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consent_scope', 'grip_angle', 'dust_level', 'clock_skew_ms'), 12)
    weight = finite_number(context.get('quarantine_pressure_weight', 1.0))
    offset = finite_number(context.get('metric_quarantine_pressure_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('robot_id', 'deformation', 'camera_fps', 'dropped_frames'), 13)
    weight = finite_number(context.get('quarantine_pressure_weight', 0.7))
    offset = finite_number(context.get('metric_quarantine_pressure_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_quarantine_pressure_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('part_family', 'illumination', 'force_hz', 'operator_id'), 14)
    weight = finite_number(context.get('quarantine_pressure_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_quarantine_pressure_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_dataset_novelty_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dust_level', 'clock_skew_ms', 'consent_scope', 'grip_angle'), 6)
    weight = finite_number(context.get('dataset_novelty_weight', 0.7))
    offset = finite_number(context.get('metric_dataset_novelty_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_dataset_novelty_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('camera_fps', 'dropped_frames', 'robot_id', 'deformation'), 7)
    weight = finite_number(context.get('dataset_novelty_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_dataset_novelty_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_dataset_novelty_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('force_hz', 'operator_id', 'part_family', 'illumination'), 8)
    weight = finite_number(context.get('dataset_novelty_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_dataset_novelty_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_dataset_novelty_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('clock_skew_ms', 'consent_scope', 'grip_angle', 'dust_level'), 9)
    weight = finite_number(context.get('dataset_novelty_weight', 1.0))
    offset = finite_number(context.get('metric_dataset_novelty_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_dataset_novelty_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dropped_frames', 'robot_id', 'deformation', 'camera_fps'), 10)
    weight = finite_number(context.get('dataset_novelty_weight', 0.7))
    offset = finite_number(context.get('metric_dataset_novelty_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_dataset_novelty_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_id', 'part_family', 'illumination', 'force_hz'), 11)
    weight = finite_number(context.get('dataset_novelty_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_dataset_novelty_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_dataset_novelty_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consent_scope', 'grip_angle', 'dust_level', 'clock_skew_ms'), 12)
    weight = finite_number(context.get('dataset_novelty_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_dataset_novelty_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_dataset_novelty_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('robot_id', 'deformation', 'camera_fps', 'dropped_frames'), 13)
    weight = finite_number(context.get('dataset_novelty_weight', 1.0))
    offset = finite_number(context.get('metric_dataset_novelty_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_dataset_novelty_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('part_family', 'illumination', 'force_hz', 'operator_id'), 14)
    weight = finite_number(context.get('dataset_novelty_weight', 0.7))
    offset = finite_number(context.get('metric_dataset_novelty_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_dataset_novelty_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('grip_angle', 'dust_level', 'clock_skew_ms', 'consent_scope'), 15)
    weight = finite_number(context.get('dataset_novelty_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_dataset_novelty_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_lineage_completeness_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('camera_fps', 'dropped_frames', 'robot_id', 'deformation'), 7)
    weight = finite_number(context.get('lineage_completeness_weight', 0.7))
    offset = finite_number(context.get('metric_lineage_completeness_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_lineage_completeness_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('force_hz', 'operator_id', 'part_family', 'illumination'), 8)
    weight = finite_number(context.get('lineage_completeness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_lineage_completeness_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_lineage_completeness_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('clock_skew_ms', 'consent_scope', 'grip_angle', 'dust_level'), 9)
    weight = finite_number(context.get('lineage_completeness_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_lineage_completeness_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_lineage_completeness_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dropped_frames', 'robot_id', 'deformation', 'camera_fps'), 10)
    weight = finite_number(context.get('lineage_completeness_weight', 1.0))
    offset = finite_number(context.get('metric_lineage_completeness_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_lineage_completeness_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_id', 'part_family', 'illumination', 'force_hz'), 11)
    weight = finite_number(context.get('lineage_completeness_weight', 0.7))
    offset = finite_number(context.get('metric_lineage_completeness_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_lineage_completeness_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consent_scope', 'grip_angle', 'dust_level', 'clock_skew_ms'), 12)
    weight = finite_number(context.get('lineage_completeness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_lineage_completeness_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_lineage_completeness_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('robot_id', 'deformation', 'camera_fps', 'dropped_frames'), 13)
    weight = finite_number(context.get('lineage_completeness_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_lineage_completeness_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_lineage_completeness_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('part_family', 'illumination', 'force_hz', 'operator_id'), 14)
    weight = finite_number(context.get('lineage_completeness_weight', 1.0))
    offset = finite_number(context.get('metric_lineage_completeness_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_lineage_completeness_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('grip_angle', 'dust_level', 'clock_skew_ms', 'consent_scope'), 15)
    weight = finite_number(context.get('lineage_completeness_weight', 0.7))
    offset = finite_number(context.get('metric_lineage_completeness_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_lineage_completeness_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('deformation', 'camera_fps', 'dropped_frames', 'robot_id'), 16)
    weight = finite_number(context.get('lineage_completeness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_lineage_completeness_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_reuse_readiness_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('force_hz', 'operator_id', 'part_family', 'illumination'), 8)
    weight = finite_number(context.get('reuse_readiness_weight', 0.7))
    offset = finite_number(context.get('metric_reuse_readiness_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_reuse_readiness_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('clock_skew_ms', 'consent_scope', 'grip_angle', 'dust_level'), 9)
    weight = finite_number(context.get('reuse_readiness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_reuse_readiness_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_reuse_readiness_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('dropped_frames', 'robot_id', 'deformation', 'camera_fps'), 10)
    weight = finite_number(context.get('reuse_readiness_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_reuse_readiness_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_reuse_readiness_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('operator_id', 'part_family', 'illumination', 'force_hz'), 11)
    weight = finite_number(context.get('reuse_readiness_weight', 1.0))
    offset = finite_number(context.get('metric_reuse_readiness_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_reuse_readiness_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consent_scope', 'grip_angle', 'dust_level', 'clock_skew_ms'), 12)
    weight = finite_number(context.get('reuse_readiness_weight', 0.7))
    offset = finite_number(context.get('metric_reuse_readiness_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_reuse_readiness_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('robot_id', 'deformation', 'camera_fps', 'dropped_frames'), 13)
    weight = finite_number(context.get('reuse_readiness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_reuse_readiness_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_reuse_readiness_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('part_family', 'illumination', 'force_hz', 'operator_id'), 14)
    weight = finite_number(context.get('reuse_readiness_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_reuse_readiness_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_reuse_readiness_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('grip_angle', 'dust_level', 'clock_skew_ms', 'consent_scope'), 15)
    weight = finite_number(context.get('reuse_readiness_weight', 1.0))
    offset = finite_number(context.get('metric_reuse_readiness_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_reuse_readiness_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('deformation', 'camera_fps', 'dropped_frames', 'robot_id'), 16)
    weight = finite_number(context.get('reuse_readiness_weight', 0.7))
    offset = finite_number(context.get('metric_reuse_readiness_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_reuse_readiness_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('illumination', 'force_hz', 'operator_id', 'part_family'), 17)
    weight = finite_number(context.get('reuse_readiness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_reuse_readiness_10_offset', 0.1))
    return bounded(base * weight + offset)

METRICS: dict[str, MetricFunction] = {
    'metric_sensor_alignment_01': metric_sensor_alignment_01,
    'metric_sensor_alignment_02': metric_sensor_alignment_02,
    'metric_sensor_alignment_03': metric_sensor_alignment_03,
    'metric_sensor_alignment_04': metric_sensor_alignment_04,
    'metric_sensor_alignment_05': metric_sensor_alignment_05,
    'metric_sensor_alignment_06': metric_sensor_alignment_06,
    'metric_sensor_alignment_07': metric_sensor_alignment_07,
    'metric_sensor_alignment_08': metric_sensor_alignment_08,
    'metric_sensor_alignment_09': metric_sensor_alignment_09,
    'metric_sensor_alignment_10': metric_sensor_alignment_10,
    'metric_condition_coverage_01': metric_condition_coverage_01,
    'metric_condition_coverage_02': metric_condition_coverage_02,
    'metric_condition_coverage_03': metric_condition_coverage_03,
    'metric_condition_coverage_04': metric_condition_coverage_04,
    'metric_condition_coverage_05': metric_condition_coverage_05,
    'metric_condition_coverage_06': metric_condition_coverage_06,
    'metric_condition_coverage_07': metric_condition_coverage_07,
    'metric_condition_coverage_08': metric_condition_coverage_08,
    'metric_condition_coverage_09': metric_condition_coverage_09,
    'metric_condition_coverage_10': metric_condition_coverage_10,
    'metric_sequence_integrity_01': metric_sequence_integrity_01,
    'metric_sequence_integrity_02': metric_sequence_integrity_02,
    'metric_sequence_integrity_03': metric_sequence_integrity_03,
    'metric_sequence_integrity_04': metric_sequence_integrity_04,
    'metric_sequence_integrity_05': metric_sequence_integrity_05,
    'metric_sequence_integrity_06': metric_sequence_integrity_06,
    'metric_sequence_integrity_07': metric_sequence_integrity_07,
    'metric_sequence_integrity_08': metric_sequence_integrity_08,
    'metric_sequence_integrity_09': metric_sequence_integrity_09,
    'metric_sequence_integrity_10': metric_sequence_integrity_10,
    'metric_operator_balance_01': metric_operator_balance_01,
    'metric_operator_balance_02': metric_operator_balance_02,
    'metric_operator_balance_03': metric_operator_balance_03,
    'metric_operator_balance_04': metric_operator_balance_04,
    'metric_operator_balance_05': metric_operator_balance_05,
    'metric_operator_balance_06': metric_operator_balance_06,
    'metric_operator_balance_07': metric_operator_balance_07,
    'metric_operator_balance_08': metric_operator_balance_08,
    'metric_operator_balance_09': metric_operator_balance_09,
    'metric_operator_balance_10': metric_operator_balance_10,
    'metric_quarantine_pressure_01': metric_quarantine_pressure_01,
    'metric_quarantine_pressure_02': metric_quarantine_pressure_02,
    'metric_quarantine_pressure_03': metric_quarantine_pressure_03,
    'metric_quarantine_pressure_04': metric_quarantine_pressure_04,
    'metric_quarantine_pressure_05': metric_quarantine_pressure_05,
    'metric_quarantine_pressure_06': metric_quarantine_pressure_06,
    'metric_quarantine_pressure_07': metric_quarantine_pressure_07,
    'metric_quarantine_pressure_08': metric_quarantine_pressure_08,
    'metric_quarantine_pressure_09': metric_quarantine_pressure_09,
    'metric_quarantine_pressure_10': metric_quarantine_pressure_10,
    'metric_dataset_novelty_01': metric_dataset_novelty_01,
    'metric_dataset_novelty_02': metric_dataset_novelty_02,
    'metric_dataset_novelty_03': metric_dataset_novelty_03,
    'metric_dataset_novelty_04': metric_dataset_novelty_04,
    'metric_dataset_novelty_05': metric_dataset_novelty_05,
    'metric_dataset_novelty_06': metric_dataset_novelty_06,
    'metric_dataset_novelty_07': metric_dataset_novelty_07,
    'metric_dataset_novelty_08': metric_dataset_novelty_08,
    'metric_dataset_novelty_09': metric_dataset_novelty_09,
    'metric_dataset_novelty_10': metric_dataset_novelty_10,
    'metric_lineage_completeness_01': metric_lineage_completeness_01,
    'metric_lineage_completeness_02': metric_lineage_completeness_02,
    'metric_lineage_completeness_03': metric_lineage_completeness_03,
    'metric_lineage_completeness_04': metric_lineage_completeness_04,
    'metric_lineage_completeness_05': metric_lineage_completeness_05,
    'metric_lineage_completeness_06': metric_lineage_completeness_06,
    'metric_lineage_completeness_07': metric_lineage_completeness_07,
    'metric_lineage_completeness_08': metric_lineage_completeness_08,
    'metric_lineage_completeness_09': metric_lineage_completeness_09,
    'metric_lineage_completeness_10': metric_lineage_completeness_10,
    'metric_reuse_readiness_01': metric_reuse_readiness_01,
    'metric_reuse_readiness_02': metric_reuse_readiness_02,
    'metric_reuse_readiness_03': metric_reuse_readiness_03,
    'metric_reuse_readiness_04': metric_reuse_readiness_04,
    'metric_reuse_readiness_05': metric_reuse_readiness_05,
    'metric_reuse_readiness_06': metric_reuse_readiness_06,
    'metric_reuse_readiness_07': metric_reuse_readiness_07,
    'metric_reuse_readiness_08': metric_reuse_readiness_08,
    'metric_reuse_readiness_09': metric_reuse_readiness_09,
    'metric_reuse_readiness_10': metric_reuse_readiness_10,
}

def metric_vector(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, float]:
    context = context or {}
    return {name: function(record, context) for name, function in METRICS.items()}

def grouped_metrics(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, float]:
    vector = metric_vector(record, context)
    groups: dict[str, list[float]] = defaultdict(list)
    for name, value in vector.items():
        key = name.rsplit('_', 1)[0].removeprefix('metric_')
        groups[key].append(value)
    return {key: statistics.fmean(values) for key, values in groups.items()}

def record_score(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    context = context or {}
    rules = evaluate(record, context)
    rule_summary = summarize(rules)
    metrics = grouped_metrics(record, context)
    metric_score = statistics.fmean(metrics.values()) if metrics else 0.0
    combined = bounded(rule_summary['score'] * 0.55 + metric_score * 0.45)
    return {'score': combined, 'rule_summary': rule_summary, 'metrics': metrics,
            'fingerprint': stable_hash({'record': record.fingerprint, 'metrics': metrics, 'rules': rule_summary})}

def portfolio(records: Iterable[DomainRecord], context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    rows = [record_score(record, context) | {'record_id': record.record_id} for record in records]
    if not rows:
        return {'count': 0, 'average': 0.0, 'minimum': 0.0, 'maximum': 0.0, 'rows': []}
    scores = [row['score'] for row in rows]
    return {'count': len(rows), 'average': statistics.fmean(scores),
            'minimum': min(scores), 'maximum': max(scores), 'rows': sorted(rows, key=lambda row: (-row['score'], row['record_id']))}

def compare(left: DomainRecord, right: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    left_metrics = grouped_metrics(left, context)
    right_metrics = grouped_metrics(right, context)
    delta = {key: right_metrics.get(key, 0.0) - left_metrics.get(key, 0.0) for key in sorted(set(left_metrics) | set(right_metrics))}
    return {'left': left.record_id, 'right': right.record_id, 'delta': delta,
            'winner': right.record_id if sum(delta.values()) >= 0 else left.record_id}
