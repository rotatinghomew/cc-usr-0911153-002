from __future__ import annotations

import math
from typing import Any, Callable, Mapping

from robot_corpus.session.contracts import DomainRecord, RuleResult, bounded, finite_number, normalized_text

RuleFunction = Callable[[DomainRecord, Mapping[str, Any]], RuleResult]

def _number(record: DomainRecord, field: str) -> float:
    value = record.payload.get(field)
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return finite_number(value)
    text = normalized_text(value)
    if not text:
        return 0.0
    try:
        return finite_number(text)
    except ValueError:
        return float(sum(ord(ch) for ch in text) % 101)

def _context_number(context: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return finite_number(context.get(key, default))
    except ValueError:
        return default

def _result(code: str, value: float, threshold: float, higher_is_better: bool, message: str, evidence: dict[str, Any]) -> RuleResult:
    distance = (value - threshold) if higher_is_better else (threshold - value)
    passed = distance >= 0
    scale = max(1.0, abs(threshold))
    score = bounded(0.5 + distance / (2.0 * scale))
    severity = 'info' if passed else ('critical' if score < 0.2 else 'error')
    return RuleResult(code, passed, score, severity, message, evidence)

def check_robot_id_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_robot_id_presence_threshold', 10.333)
    return _result('check_robot_id_presence', adjusted, threshold, True, 'validates robot_id presence',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_robot_id_range_threshold', 12.667)
    return _result('check_robot_id_range', adjusted, threshold, True, 'validates robot_id range',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_robot_id_stability_threshold', 15.0)
    return _result('check_robot_id_stability', adjusted, threshold, False, 'validates robot_id stability',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_robot_id_freshness_threshold', 17.333)
    return _result('check_robot_id_freshness', adjusted, threshold, True, 'validates robot_id freshness',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_robot_id_coverage_threshold', 19.667)
    return _result('check_robot_id_coverage', adjusted, threshold, True, 'validates robot_id coverage',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_robot_id_consistency_threshold', 22.0)
    return _result('check_robot_id_consistency', adjusted, threshold, False, 'validates robot_id consistency',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_robot_id_risk_threshold', 24.333)
    return _result('check_robot_id_risk', adjusted, threshold, True, 'validates robot_id risk',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_robot_id_confidence_threshold', 26.667)
    return _result('check_robot_id_confidence', adjusted, threshold, True, 'validates robot_id confidence',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_robot_id_dependency_threshold', 29.0)
    return _result('check_robot_id_dependency', adjusted, threshold, False, 'validates robot_id dependency',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_robot_id_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'robot_id')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_robot_id_readiness_threshold', 31.333)
    return _result('check_robot_id_readiness', adjusted, threshold, True, 'validates robot_id readiness',
                   {'field': 'robot_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_part_family_presence_threshold', 9.333)
    return _result('check_part_family_presence', adjusted, threshold, True, 'validates part_family presence',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_part_family_range_threshold', 11.667)
    return _result('check_part_family_range', adjusted, threshold, False, 'validates part_family range',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_part_family_stability_threshold', 14.0)
    return _result('check_part_family_stability', adjusted, threshold, True, 'validates part_family stability',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_part_family_freshness_threshold', 16.333)
    return _result('check_part_family_freshness', adjusted, threshold, True, 'validates part_family freshness',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_part_family_coverage_threshold', 18.667)
    return _result('check_part_family_coverage', adjusted, threshold, False, 'validates part_family coverage',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_part_family_consistency_threshold', 21.0)
    return _result('check_part_family_consistency', adjusted, threshold, True, 'validates part_family consistency',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_part_family_risk_threshold', 23.333)
    return _result('check_part_family_risk', adjusted, threshold, True, 'validates part_family risk',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_part_family_confidence_threshold', 25.667)
    return _result('check_part_family_confidence', adjusted, threshold, False, 'validates part_family confidence',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_part_family_dependency_threshold', 28.0)
    return _result('check_part_family_dependency', adjusted, threshold, True, 'validates part_family dependency',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_part_family_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'part_family')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_part_family_readiness_threshold', 30.333)
    return _result('check_part_family_readiness', adjusted, threshold, True, 'validates part_family readiness',
                   {'field': 'part_family', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_grip_angle_presence_threshold', 8.333)
    return _result('check_grip_angle_presence', adjusted, threshold, False, 'validates grip_angle presence',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_grip_angle_range_threshold', 10.667)
    return _result('check_grip_angle_range', adjusted, threshold, True, 'validates grip_angle range',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_grip_angle_stability_threshold', 13.0)
    return _result('check_grip_angle_stability', adjusted, threshold, True, 'validates grip_angle stability',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_grip_angle_freshness_threshold', 15.333)
    return _result('check_grip_angle_freshness', adjusted, threshold, False, 'validates grip_angle freshness',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_grip_angle_coverage_threshold', 17.667)
    return _result('check_grip_angle_coverage', adjusted, threshold, True, 'validates grip_angle coverage',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_grip_angle_consistency_threshold', 20.0)
    return _result('check_grip_angle_consistency', adjusted, threshold, True, 'validates grip_angle consistency',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_grip_angle_risk_threshold', 22.333)
    return _result('check_grip_angle_risk', adjusted, threshold, False, 'validates grip_angle risk',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_grip_angle_confidence_threshold', 24.667)
    return _result('check_grip_angle_confidence', adjusted, threshold, True, 'validates grip_angle confidence',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_grip_angle_dependency_threshold', 27.0)
    return _result('check_grip_angle_dependency', adjusted, threshold, True, 'validates grip_angle dependency',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_grip_angle_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'grip_angle')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_grip_angle_readiness_threshold', 29.333)
    return _result('check_grip_angle_readiness', adjusted, threshold, False, 'validates grip_angle readiness',
                   {'field': 'grip_angle', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_deformation_presence_threshold', 31.667)
    return _result('check_deformation_presence', adjusted, threshold, True, 'validates deformation presence',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_deformation_range_threshold', 9.667)
    return _result('check_deformation_range', adjusted, threshold, True, 'validates deformation range',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_deformation_stability_threshold', 12.0)
    return _result('check_deformation_stability', adjusted, threshold, False, 'validates deformation stability',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_deformation_freshness_threshold', 14.333)
    return _result('check_deformation_freshness', adjusted, threshold, True, 'validates deformation freshness',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_deformation_coverage_threshold', 16.667)
    return _result('check_deformation_coverage', adjusted, threshold, True, 'validates deformation coverage',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_deformation_consistency_threshold', 19.0)
    return _result('check_deformation_consistency', adjusted, threshold, False, 'validates deformation consistency',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_deformation_risk_threshold', 21.333)
    return _result('check_deformation_risk', adjusted, threshold, True, 'validates deformation risk',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_deformation_confidence_threshold', 23.667)
    return _result('check_deformation_confidence', adjusted, threshold, True, 'validates deformation confidence',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_deformation_dependency_threshold', 26.0)
    return _result('check_deformation_dependency', adjusted, threshold, False, 'validates deformation dependency',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_deformation_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'deformation')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_deformation_readiness_threshold', 28.333)
    return _result('check_deformation_readiness', adjusted, threshold, True, 'validates deformation readiness',
                   {'field': 'deformation', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_illumination_presence_threshold', 30.667)
    return _result('check_illumination_presence', adjusted, threshold, True, 'validates illumination presence',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_illumination_range_threshold', 8.667)
    return _result('check_illumination_range', adjusted, threshold, False, 'validates illumination range',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_illumination_stability_threshold', 11.0)
    return _result('check_illumination_stability', adjusted, threshold, True, 'validates illumination stability',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_illumination_freshness_threshold', 13.333)
    return _result('check_illumination_freshness', adjusted, threshold, True, 'validates illumination freshness',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_illumination_coverage_threshold', 15.667)
    return _result('check_illumination_coverage', adjusted, threshold, False, 'validates illumination coverage',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_illumination_consistency_threshold', 18.0)
    return _result('check_illumination_consistency', adjusted, threshold, True, 'validates illumination consistency',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_illumination_risk_threshold', 20.333)
    return _result('check_illumination_risk', adjusted, threshold, True, 'validates illumination risk',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_illumination_confidence_threshold', 22.667)
    return _result('check_illumination_confidence', adjusted, threshold, False, 'validates illumination confidence',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_illumination_dependency_threshold', 25.0)
    return _result('check_illumination_dependency', adjusted, threshold, True, 'validates illumination dependency',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_illumination_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'illumination')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_illumination_readiness_threshold', 27.333)
    return _result('check_illumination_readiness', adjusted, threshold, True, 'validates illumination readiness',
                   {'field': 'illumination', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_dust_level_presence_threshold', 29.667)
    return _result('check_dust_level_presence', adjusted, threshold, False, 'validates dust_level presence',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_dust_level_range_threshold', 32.0)
    return _result('check_dust_level_range', adjusted, threshold, True, 'validates dust_level range',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_dust_level_stability_threshold', 10.0)
    return _result('check_dust_level_stability', adjusted, threshold, True, 'validates dust_level stability',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_dust_level_freshness_threshold', 12.333)
    return _result('check_dust_level_freshness', adjusted, threshold, False, 'validates dust_level freshness',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_dust_level_coverage_threshold', 14.667)
    return _result('check_dust_level_coverage', adjusted, threshold, True, 'validates dust_level coverage',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_dust_level_consistency_threshold', 17.0)
    return _result('check_dust_level_consistency', adjusted, threshold, True, 'validates dust_level consistency',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_dust_level_risk_threshold', 19.333)
    return _result('check_dust_level_risk', adjusted, threshold, False, 'validates dust_level risk',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_dust_level_confidence_threshold', 21.667)
    return _result('check_dust_level_confidence', adjusted, threshold, True, 'validates dust_level confidence',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_dust_level_dependency_threshold', 24.0)
    return _result('check_dust_level_dependency', adjusted, threshold, True, 'validates dust_level dependency',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dust_level_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dust_level')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_dust_level_readiness_threshold', 26.333)
    return _result('check_dust_level_readiness', adjusted, threshold, False, 'validates dust_level readiness',
                   {'field': 'dust_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_camera_fps_presence_threshold', 28.667)
    return _result('check_camera_fps_presence', adjusted, threshold, True, 'validates camera_fps presence',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_camera_fps_range_threshold', 31.0)
    return _result('check_camera_fps_range', adjusted, threshold, True, 'validates camera_fps range',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_camera_fps_stability_threshold', 9.0)
    return _result('check_camera_fps_stability', adjusted, threshold, False, 'validates camera_fps stability',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_camera_fps_freshness_threshold', 11.333)
    return _result('check_camera_fps_freshness', adjusted, threshold, True, 'validates camera_fps freshness',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_camera_fps_coverage_threshold', 13.667)
    return _result('check_camera_fps_coverage', adjusted, threshold, True, 'validates camera_fps coverage',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_camera_fps_consistency_threshold', 16.0)
    return _result('check_camera_fps_consistency', adjusted, threshold, False, 'validates camera_fps consistency',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_camera_fps_risk_threshold', 18.333)
    return _result('check_camera_fps_risk', adjusted, threshold, True, 'validates camera_fps risk',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_camera_fps_confidence_threshold', 20.667)
    return _result('check_camera_fps_confidence', adjusted, threshold, True, 'validates camera_fps confidence',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_camera_fps_dependency_threshold', 23.0)
    return _result('check_camera_fps_dependency', adjusted, threshold, False, 'validates camera_fps dependency',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_camera_fps_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'camera_fps')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_camera_fps_readiness_threshold', 25.333)
    return _result('check_camera_fps_readiness', adjusted, threshold, True, 'validates camera_fps readiness',
                   {'field': 'camera_fps', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_force_hz_presence_threshold', 27.667)
    return _result('check_force_hz_presence', adjusted, threshold, True, 'validates force_hz presence',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_force_hz_range_threshold', 30.0)
    return _result('check_force_hz_range', adjusted, threshold, False, 'validates force_hz range',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_force_hz_stability_threshold', 8.0)
    return _result('check_force_hz_stability', adjusted, threshold, True, 'validates force_hz stability',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_force_hz_freshness_threshold', 10.333)
    return _result('check_force_hz_freshness', adjusted, threshold, True, 'validates force_hz freshness',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_force_hz_coverage_threshold', 12.667)
    return _result('check_force_hz_coverage', adjusted, threshold, False, 'validates force_hz coverage',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_force_hz_consistency_threshold', 15.0)
    return _result('check_force_hz_consistency', adjusted, threshold, True, 'validates force_hz consistency',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_force_hz_risk_threshold', 17.333)
    return _result('check_force_hz_risk', adjusted, threshold, True, 'validates force_hz risk',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_force_hz_confidence_threshold', 19.667)
    return _result('check_force_hz_confidence', adjusted, threshold, False, 'validates force_hz confidence',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_force_hz_dependency_threshold', 22.0)
    return _result('check_force_hz_dependency', adjusted, threshold, True, 'validates force_hz dependency',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_force_hz_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'force_hz')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_force_hz_readiness_threshold', 24.333)
    return _result('check_force_hz_readiness', adjusted, threshold, True, 'validates force_hz readiness',
                   {'field': 'force_hz', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_clock_skew_ms_presence_threshold', 26.667)
    return _result('check_clock_skew_ms_presence', adjusted, threshold, False, 'validates clock_skew_ms presence',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_clock_skew_ms_range_threshold', 29.0)
    return _result('check_clock_skew_ms_range', adjusted, threshold, True, 'validates clock_skew_ms range',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_clock_skew_ms_stability_threshold', 31.333)
    return _result('check_clock_skew_ms_stability', adjusted, threshold, True, 'validates clock_skew_ms stability',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_clock_skew_ms_freshness_threshold', 9.333)
    return _result('check_clock_skew_ms_freshness', adjusted, threshold, False, 'validates clock_skew_ms freshness',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_clock_skew_ms_coverage_threshold', 11.667)
    return _result('check_clock_skew_ms_coverage', adjusted, threshold, True, 'validates clock_skew_ms coverage',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_clock_skew_ms_consistency_threshold', 14.0)
    return _result('check_clock_skew_ms_consistency', adjusted, threshold, True, 'validates clock_skew_ms consistency',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_clock_skew_ms_risk_threshold', 16.333)
    return _result('check_clock_skew_ms_risk', adjusted, threshold, False, 'validates clock_skew_ms risk',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_clock_skew_ms_confidence_threshold', 18.667)
    return _result('check_clock_skew_ms_confidence', adjusted, threshold, True, 'validates clock_skew_ms confidence',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_clock_skew_ms_dependency_threshold', 21.0)
    return _result('check_clock_skew_ms_dependency', adjusted, threshold, True, 'validates clock_skew_ms dependency',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_clock_skew_ms_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'clock_skew_ms')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_clock_skew_ms_readiness_threshold', 23.333)
    return _result('check_clock_skew_ms_readiness', adjusted, threshold, False, 'validates clock_skew_ms readiness',
                   {'field': 'clock_skew_ms', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_dropped_frames_presence_threshold', 25.667)
    return _result('check_dropped_frames_presence', adjusted, threshold, True, 'validates dropped_frames presence',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_dropped_frames_range_threshold', 28.0)
    return _result('check_dropped_frames_range', adjusted, threshold, True, 'validates dropped_frames range',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_dropped_frames_stability_threshold', 30.333)
    return _result('check_dropped_frames_stability', adjusted, threshold, False, 'validates dropped_frames stability',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_dropped_frames_freshness_threshold', 8.333)
    return _result('check_dropped_frames_freshness', adjusted, threshold, True, 'validates dropped_frames freshness',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_dropped_frames_coverage_threshold', 10.667)
    return _result('check_dropped_frames_coverage', adjusted, threshold, True, 'validates dropped_frames coverage',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_dropped_frames_consistency_threshold', 13.0)
    return _result('check_dropped_frames_consistency', adjusted, threshold, False, 'validates dropped_frames consistency',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_dropped_frames_risk_threshold', 15.333)
    return _result('check_dropped_frames_risk', adjusted, threshold, True, 'validates dropped_frames risk',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_dropped_frames_confidence_threshold', 17.667)
    return _result('check_dropped_frames_confidence', adjusted, threshold, True, 'validates dropped_frames confidence',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_dropped_frames_dependency_threshold', 20.0)
    return _result('check_dropped_frames_dependency', adjusted, threshold, False, 'validates dropped_frames dependency',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_dropped_frames_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'dropped_frames')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_dropped_frames_readiness_threshold', 22.333)
    return _result('check_dropped_frames_readiness', adjusted, threshold, True, 'validates dropped_frames readiness',
                   {'field': 'dropped_frames', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_operator_id_presence_threshold', 24.667)
    return _result('check_operator_id_presence', adjusted, threshold, True, 'validates operator_id presence',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_operator_id_range_threshold', 27.0)
    return _result('check_operator_id_range', adjusted, threshold, False, 'validates operator_id range',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_operator_id_stability_threshold', 29.333)
    return _result('check_operator_id_stability', adjusted, threshold, True, 'validates operator_id stability',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_operator_id_freshness_threshold', 31.667)
    return _result('check_operator_id_freshness', adjusted, threshold, True, 'validates operator_id freshness',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_operator_id_coverage_threshold', 9.667)
    return _result('check_operator_id_coverage', adjusted, threshold, False, 'validates operator_id coverage',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_operator_id_consistency_threshold', 12.0)
    return _result('check_operator_id_consistency', adjusted, threshold, True, 'validates operator_id consistency',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_operator_id_risk_threshold', 14.333)
    return _result('check_operator_id_risk', adjusted, threshold, True, 'validates operator_id risk',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_operator_id_confidence_threshold', 16.667)
    return _result('check_operator_id_confidence', adjusted, threshold, False, 'validates operator_id confidence',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_operator_id_dependency_threshold', 19.0)
    return _result('check_operator_id_dependency', adjusted, threshold, True, 'validates operator_id dependency',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_operator_id_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'operator_id')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_operator_id_readiness_threshold', 21.333)
    return _result('check_operator_id_readiness', adjusted, threshold, True, 'validates operator_id readiness',
                   {'field': 'operator_id', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_consent_scope_presence_threshold', 23.667)
    return _result('check_consent_scope_presence', adjusted, threshold, False, 'validates consent_scope presence',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_consent_scope_range_threshold', 26.0)
    return _result('check_consent_scope_range', adjusted, threshold, True, 'validates consent_scope range',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_consent_scope_stability_threshold', 28.333)
    return _result('check_consent_scope_stability', adjusted, threshold, True, 'validates consent_scope stability',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_consent_scope_freshness_threshold', 30.667)
    return _result('check_consent_scope_freshness', adjusted, threshold, False, 'validates consent_scope freshness',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_consent_scope_coverage_threshold', 8.667)
    return _result('check_consent_scope_coverage', adjusted, threshold, True, 'validates consent_scope coverage',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_consent_scope_consistency_threshold', 11.0)
    return _result('check_consent_scope_consistency', adjusted, threshold, True, 'validates consent_scope consistency',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_consent_scope_risk_threshold', 13.333)
    return _result('check_consent_scope_risk', adjusted, threshold, False, 'validates consent_scope risk',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_consent_scope_confidence_threshold', 15.667)
    return _result('check_consent_scope_confidence', adjusted, threshold, True, 'validates consent_scope confidence',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_consent_scope_dependency_threshold', 18.0)
    return _result('check_consent_scope_dependency', adjusted, threshold, True, 'validates consent_scope dependency',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consent_scope_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consent_scope')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_consent_scope_readiness_threshold', 20.333)
    return _result('check_consent_scope_readiness', adjusted, threshold, False, 'validates consent_scope readiness',
                   {'field': 'consent_scope', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

RULES: tuple[RuleFunction, ...] = (
    check_robot_id_presence,
    check_robot_id_range,
    check_robot_id_stability,
    check_robot_id_freshness,
    check_robot_id_coverage,
    check_robot_id_consistency,
    check_robot_id_risk,
    check_robot_id_confidence,
    check_robot_id_dependency,
    check_robot_id_readiness,
    check_part_family_presence,
    check_part_family_range,
    check_part_family_stability,
    check_part_family_freshness,
    check_part_family_coverage,
    check_part_family_consistency,
    check_part_family_risk,
    check_part_family_confidence,
    check_part_family_dependency,
    check_part_family_readiness,
    check_grip_angle_presence,
    check_grip_angle_range,
    check_grip_angle_stability,
    check_grip_angle_freshness,
    check_grip_angle_coverage,
    check_grip_angle_consistency,
    check_grip_angle_risk,
    check_grip_angle_confidence,
    check_grip_angle_dependency,
    check_grip_angle_readiness,
    check_deformation_presence,
    check_deformation_range,
    check_deformation_stability,
    check_deformation_freshness,
    check_deformation_coverage,
    check_deformation_consistency,
    check_deformation_risk,
    check_deformation_confidence,
    check_deformation_dependency,
    check_deformation_readiness,
    check_illumination_presence,
    check_illumination_range,
    check_illumination_stability,
    check_illumination_freshness,
    check_illumination_coverage,
    check_illumination_consistency,
    check_illumination_risk,
    check_illumination_confidence,
    check_illumination_dependency,
    check_illumination_readiness,
    check_dust_level_presence,
    check_dust_level_range,
    check_dust_level_stability,
    check_dust_level_freshness,
    check_dust_level_coverage,
    check_dust_level_consistency,
    check_dust_level_risk,
    check_dust_level_confidence,
    check_dust_level_dependency,
    check_dust_level_readiness,
    check_camera_fps_presence,
    check_camera_fps_range,
    check_camera_fps_stability,
    check_camera_fps_freshness,
    check_camera_fps_coverage,
    check_camera_fps_consistency,
    check_camera_fps_risk,
    check_camera_fps_confidence,
    check_camera_fps_dependency,
    check_camera_fps_readiness,
    check_force_hz_presence,
    check_force_hz_range,
    check_force_hz_stability,
    check_force_hz_freshness,
    check_force_hz_coverage,
    check_force_hz_consistency,
    check_force_hz_risk,
    check_force_hz_confidence,
    check_force_hz_dependency,
    check_force_hz_readiness,
    check_clock_skew_ms_presence,
    check_clock_skew_ms_range,
    check_clock_skew_ms_stability,
    check_clock_skew_ms_freshness,
    check_clock_skew_ms_coverage,
    check_clock_skew_ms_consistency,
    check_clock_skew_ms_risk,
    check_clock_skew_ms_confidence,
    check_clock_skew_ms_dependency,
    check_clock_skew_ms_readiness,
    check_dropped_frames_presence,
    check_dropped_frames_range,
    check_dropped_frames_stability,
    check_dropped_frames_freshness,
    check_dropped_frames_coverage,
    check_dropped_frames_consistency,
    check_dropped_frames_risk,
    check_dropped_frames_confidence,
    check_dropped_frames_dependency,
    check_dropped_frames_readiness,
    check_operator_id_presence,
    check_operator_id_range,
    check_operator_id_stability,
    check_operator_id_freshness,
    check_operator_id_coverage,
    check_operator_id_consistency,
    check_operator_id_risk,
    check_operator_id_confidence,
    check_operator_id_dependency,
    check_operator_id_readiness,
    check_consent_scope_presence,
    check_consent_scope_range,
    check_consent_scope_stability,
    check_consent_scope_freshness,
    check_consent_scope_coverage,
    check_consent_scope_consistency,
    check_consent_scope_risk,
    check_consent_scope_confidence,
    check_consent_scope_dependency,
    check_consent_scope_readiness,
)

RULE_INDEX = {rule.__name__: rule for rule in RULES}

def evaluate(record: DomainRecord, context: Mapping[str, Any] | None = None) -> tuple[RuleResult, ...]:
    context = context or {}
    return tuple(rule(record, context) for rule in RULES)

def summarize(results: tuple[RuleResult, ...]) -> dict[str, Any]:
    if not results:
        return {'score': 0.0, 'passed': 0, 'failed': 0, 'critical': 0}
    return {'score': sum(item.score for item in results) / len(results),
            'passed': sum(item.passed for item in results),
            'failed': sum(not item.passed for item in results),
            'critical': sum(item.severity == 'critical' for item in results)}
