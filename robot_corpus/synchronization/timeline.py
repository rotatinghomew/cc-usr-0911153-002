from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Any, Iterable

from robot_corpus.session.contracts import DomainRecord, bounded, finite_number


@dataclass(frozen=True)
class AlignmentWindow:
    session_id: str
    skew_ms: float
    frame_loss: float
    quality: float
    quarantine: bool


def alignment(record: DomainRecord) -> AlignmentWindow:
    skew = abs(finite_number(record.payload.get("clock_skew_ms", 0.0)))
    drops = max(0.0, finite_number(record.payload.get("dropped_frames", 0.0)))
    camera_rate = max(1.0, finite_number(record.payload.get("camera_fps", 1.0)))
    force_rate = max(1.0, finite_number(record.payload.get("force_hz", 1.0)))
    normalized_skew = bounded(skew / 250.0)
    loss = bounded(drops / (camera_rate * 30.0))
    rate_fit = bounded(min(camera_rate, force_rate) / max(camera_rate, force_rate))
    quality = bounded(rate_fit * 0.45 + (1.0 - normalized_skew) * 0.35 + (1.0 - loss) * 0.20)
    return AlignmentWindow(record.record_id, skew, loss, quality, quality < 0.55 or skew > 150.0)


def condition_cell(record: DomainRecord) -> tuple[int, int, int, int]:
    angle = int(finite_number(record.payload.get("grip_angle", 0.0)) // 15)
    deformation = int(finite_number(record.payload.get("deformation", 0.0)) // 5)
    illumination = int(finite_number(record.payload.get("illumination", 0.0)) // 100)
    dust = int(finite_number(record.payload.get("dust_level", 0.0)) // 10)
    return angle, deformation, illumination, dust


def coverage_lattice(records: Iterable[DomainRecord]) -> dict[str, float]:
    rows = list(records)
    cells = {condition_cell(row) for row in rows}
    robots = {str(row.payload.get("robot_id", "unknown")) for row in rows}
    parts = {str(row.payload.get("part_family", "unknown")) for row in rows}
    quarantined = sum(alignment(row).quarantine for row in rows)
    theoretical = max(1, len(robots) * len(parts) * 4)
    return {"cell_count": float(len(cells)), "robot_count": float(len(robots)), "part_count": float(len(parts)),
            "coverage": bounded(len(cells) / theoretical), "quarantine_rate": quarantined / max(1, len(rows))}


def sequence_health(records: Iterable[DomainRecord]) -> dict[str, float]:
    windows = [alignment(row) for row in records]
    qualities = [window.quality for window in windows]
    return {"mean_alignment": statistics.fmean(qualities) if qualities else 0.0,
            "alignment_jitter": statistics.pstdev(qualities) if len(qualities) > 1 else 0.0,
            "quarantined": float(sum(window.quarantine for window in windows))}


def derive_context(record: DomainRecord, repository: Any) -> dict[str, float]:
    rows = repository.list_records() or [record]
    window = alignment(record)
    coverage = coverage_lattice(rows)
    health = sequence_health(rows)
    return {"sensor_alignment_weight": 0.6 + window.quality * 0.6,
            "condition_coverage_weight": 0.7 + coverage["coverage"] * 0.5,
            "sequence_integrity_weight": 0.7 + health["mean_alignment"] * 0.4,
            "quarantine_pressure_weight": 0.7 + coverage["quarantine_rate"] * 0.8,
            "reuse_readiness_weight": 0.6 + (1.0 - health["alignment_jitter"]) * 0.5}
