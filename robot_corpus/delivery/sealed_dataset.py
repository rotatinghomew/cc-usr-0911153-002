from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable

from robot_corpus.session.contracts import ContractError, DomainRecord, canonical_json, stable_hash, utc_now
from robot_corpus.synchronization.timeline import alignment, condition_cell, coverage_gap_report, coverage_lattice, quarantine_reasons


def prepare_datasets(connection: sqlite3.Connection) -> None:
    connection.execute("""CREATE TABLE IF NOT EXISTS sealed_datasets(
        dataset_id TEXT PRIMARY KEY, snapshot_hash TEXT NOT NULL, item_count INTEGER NOT NULL,
        usable_item_count INTEGER NOT NULL DEFAULT 0, quarantined_item_count INTEGER NOT NULL DEFAULT 0,
        quality_basis_json TEXT NOT NULL DEFAULT '{}', gap_report_json TEXT NOT NULL DEFAULT '{}',
        coverage_json TEXT NOT NULL, created_at TEXT NOT NULL
    )""")
    connection.execute("""CREATE TABLE IF NOT EXISTS sealed_dataset_items(
        dataset_id TEXT NOT NULL, session_id TEXT NOT NULL, session_version INTEGER NOT NULL,
        record_fingerprint TEXT NOT NULL, robot_id TEXT NOT NULL, part_family TEXT NOT NULL,
        condition_json TEXT NOT NULL, quarantined INTEGER NOT NULL,
        quarantine_reasons_json TEXT NOT NULL DEFAULT '[]',
        PRIMARY KEY(dataset_id, session_id),
        FOREIGN KEY(dataset_id) REFERENCES sealed_datasets(dataset_id)
    )""")
    # Migrate databases created before the quarantine-evidence split.
    existing = {row[1] for row in connection.execute("PRAGMA table_info(sealed_datasets)")}
    if "usable_item_count" not in existing:
        connection.execute("ALTER TABLE sealed_datasets ADD COLUMN usable_item_count INTEGER NOT NULL DEFAULT 0")
    if "quarantined_item_count" not in existing:
        connection.execute("ALTER TABLE sealed_datasets ADD COLUMN quarantined_item_count INTEGER NOT NULL DEFAULT 0")
    if "quality_basis_json" not in existing:
        connection.execute("ALTER TABLE sealed_datasets ADD COLUMN quality_basis_json TEXT NOT NULL DEFAULT '{}'")
    if "gap_report_json" not in existing:
        connection.execute("ALTER TABLE sealed_datasets ADD COLUMN gap_report_json TEXT NOT NULL DEFAULT '{}'")
    item_columns = {row[1] for row in connection.execute("PRAGMA table_info(sealed_dataset_items)")}
    if "quarantine_reasons_json" not in item_columns:
        connection.execute("ALTER TABLE sealed_dataset_items ADD COLUMN quarantine_reasons_json TEXT NOT NULL DEFAULT '[]'")


def assemble_dataset(records: Iterable[DomainRecord]) -> dict[str, Any]:
    rows = list(records)
    if not rows or len({row.record_id for row in rows}) != len(rows):
        raise ContractError("dataset requires unique capture sessions")
    items = [{"session_id": row.record_id, "session_version": row.version,
              "record_fingerprint": row.fingerprint,
              "robot_id": str(row.payload.get("robot_id", "unknown")),
              "part_family": str(row.payload.get("part_family", "unknown")),
              "condition": list(condition_cell(row)),
              "quarantined": alignment(row).quarantine,
              "quarantine_reasons": list(quarantine_reasons(row))} for row in rows]
    items.sort(key=lambda item: item["session_id"])
    usable_items = [item for item in items if not item["quarantined"]]
    # Coverage must reflect usable evidence only; isolated items stay attached for
    # audit but can never claim a condition cell.
    coverage = coverage_lattice(rows)
    return {"items": items,
            "usable_item_count": len(usable_items),
            "quarantined_item_count": len(items) - len(usable_items),
            "quality_basis": "alignment quarantine floor (quality>=0.55 and |clock_skew_ms|<=150); "
                             "quarantined sessions retained for audit only",
            "coverage": coverage,
            "coverage_gaps": coverage_gap_report(rows)}


def seal_dataset(connection: sqlite3.Connection, dataset_id: str, records: Iterable[DomainRecord]) -> dict[str, Any]:
    prepare_datasets(connection)
    assembled = assemble_dataset(records)
    identity = stable_hash(assembled)
    existing = connection.execute("SELECT snapshot_hash FROM sealed_datasets WHERE dataset_id=?", (dataset_id,)).fetchone()
    if existing:
        if existing[0] != identity:
            raise ContractError("a sealed dataset cannot change after publication")
        return read_dataset(connection, dataset_id)
    connection.execute(
        "INSERT INTO sealed_datasets(dataset_id,snapshot_hash,item_count,usable_item_count,"
        "quarantined_item_count,quality_basis_json,gap_report_json,coverage_json,created_at) "
        "VALUES(?,?,?,?,?,?,?,?,?)",
        (dataset_id, identity, len(assembled["items"]), assembled["usable_item_count"],
         assembled["quarantined_item_count"], canonical_json(assembled["quality_basis"]),
         canonical_json(assembled["coverage_gaps"]), canonical_json(assembled["coverage"]), utc_now()))
    for item in assembled["items"]:
        connection.execute(
            "INSERT INTO sealed_dataset_items(dataset_id,session_id,session_version,record_fingerprint,"
            "robot_id,part_family,condition_json,quarantined,quarantine_reasons_json) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (dataset_id, item["session_id"], item["session_version"], item["record_fingerprint"],
             item["robot_id"], item["part_family"], canonical_json(item["condition"]),
             int(item["quarantined"]), canonical_json(item["quarantine_reasons"])))
    return read_dataset(connection, dataset_id)


def read_dataset(connection: sqlite3.Connection, dataset_id: str) -> dict[str, Any]:
    prepare_datasets(connection)
    header = connection.execute("SELECT * FROM sealed_datasets WHERE dataset_id=?", (dataset_id,)).fetchone()
    if header is None:
        raise ContractError("unknown sealed dataset")
    items = [dict(row) for row in connection.execute(
        "SELECT * FROM sealed_dataset_items WHERE dataset_id=? ORDER BY session_id", (dataset_id,))]
    for item in items:
        item["condition"] = json.loads(item.pop("condition_json"))
        item["quarantined"] = bool(item["quarantined"])
        item["quarantine_reasons"] = json.loads(item.pop("quarantine_reasons_json", "[]"))
    keys = set(header.keys())
    result = {"dataset_id": dataset_id, "snapshot_hash": header["snapshot_hash"],
              "created_at": header["created_at"], "coverage": json.loads(header["coverage_json"]),
              "item_count": header["item_count"], "items": items}
    if "usable_item_count" in keys:
        result["usable_item_count"] = header["usable_item_count"]
        result["quarantined_item_count"] = header["quarantined_item_count"]
        result["quality_basis"] = json.loads(header["quality_basis_json"])
        result["coverage_gaps"] = json.loads(header["gap_report_json"])
    else:
        result["usable_item_count"] = sum(not item["quarantined"] for item in items)
        result["quarantined_item_count"] = sum(item["quarantined"] for item in items)
        result["quality_basis"] = None
        result["coverage_gaps"] = None
    return result


def review_dataset(connection: sqlite3.Connection, dataset_id: str, current_records: Iterable[DomainRecord]) -> dict[str, Any]:
    """Build a distinguishable review opinion without mutating the sealed dataset.

    The sealed manifest keeps the quality basis adopted at publication time. This
    opinion re-evaluates the *current* record versions against the same quarantine
    rule and reports which units were genuinely recovered, which remain without a
    usable sample and which sealed sessions have drifted from the sealed fingerprint.
    """
    sealed = read_dataset(connection, dataset_id)
    current_rows = list(current_records)
    current_by_id = {row.record_id: row for row in current_rows}
    session_reviews: list[dict[str, Any]] = []
    for sealed_item in sealed["items"]:
        session_id = sealed_item["session_id"]
        current = current_by_id.get(session_id)
        if current is None:
            session_reviews.append({"session_id": session_id, "status": "missing-current-record",
                                    "sealed_version": sealed_item["session_version"],
                                    "sealed_quarantined": sealed_item["quarantined"],
                                    "current_quarantined": None, "fingerprint_match": False,
                                    "quarantine_reasons": sealed_item.get("quarantine_reasons", [])})
            continue
        current_quarantined = alignment(current).quarantine
        sealed_quarantined = sealed_item["quarantined"]
        if sealed_quarantined and not current_quarantined:
            status = "recovered"
        elif not sealed_quarantined and current_quarantined:
            status = "regressed"
        elif current_quarantined:
            status = "still-quarantined"
        else:
            status = "still-usable"
        session_reviews.append({
            "session_id": session_id, "status": status,
            "sealed_version": sealed_item["session_version"],
            "current_version": current.version,
            "sealed_quarantined": sealed_quarantined,
            "current_quarantined": current_quarantined,
            "fingerprint_match": current.fingerprint == sealed_item["record_fingerprint"],
            "quarantine_reasons": list(quarantine_reasons(current))})
    current_gaps = coverage_gap_report(current_rows)
    current_coverage = coverage_lattice(current_rows)
    recovered = [item["session_id"] for item in session_reviews if item["status"] == "recovered"]
    still_open = [unit["condition"] for unit in current_gaps["open_gaps"]]
    opinion_hash = stable_hash({"dataset_id": dataset_id, "sealed_snapshot": sealed["snapshot_hash"],
                                "session_reviews": session_reviews, "current_coverage": current_coverage,
                                "open_gaps": still_open})
    return {"review_kind": "post-seal quality review (does not alter the sealed dataset)",
            "dataset_id": dataset_id, "sealed_snapshot_hash": sealed["snapshot_hash"],
            "sealed_quality_basis": sealed.get("quality_basis"),
            "sealed_coverage": sealed["coverage"],
            "reviewed_at": utc_now(), "opinion_hash": opinion_hash,
            "current_coverage": current_coverage, "coverage_gaps": current_gaps,
            "recovered_sessions": recovered, "still_open_gap_cells": still_open,
            "session_reviews": sorted(session_reviews, key=lambda item: item["session_id"])}
