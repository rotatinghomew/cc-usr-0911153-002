from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable

from robot_corpus.session.contracts import ContractError, DomainRecord, canonical_json, stable_hash, utc_now
from robot_corpus.synchronization.timeline import alignment, condition_cell, coverage_lattice


def prepare_datasets(connection: sqlite3.Connection) -> None:
    connection.execute("""CREATE TABLE IF NOT EXISTS sealed_datasets(
        dataset_id TEXT PRIMARY KEY, snapshot_hash TEXT NOT NULL, item_count INTEGER NOT NULL,
        coverage_json TEXT NOT NULL, created_at TEXT NOT NULL
    )""")
    connection.execute("""CREATE TABLE IF NOT EXISTS sealed_dataset_items(
        dataset_id TEXT NOT NULL, session_id TEXT NOT NULL, session_version INTEGER NOT NULL,
        record_fingerprint TEXT NOT NULL, robot_id TEXT NOT NULL, part_family TEXT NOT NULL,
        condition_json TEXT NOT NULL, quarantined INTEGER NOT NULL,
        PRIMARY KEY(dataset_id, session_id),
        FOREIGN KEY(dataset_id) REFERENCES sealed_datasets(dataset_id)
    )""")


def assemble_dataset(records: Iterable[DomainRecord]) -> dict[str, Any]:
    rows = list(records)
    if not rows or len({row.record_id for row in rows}) != len(rows):
        raise ContractError("dataset requires unique capture sessions")
    items = [{"session_id": row.record_id, "session_version": row.version,
              "record_fingerprint": row.fingerprint,
              "robot_id": str(row.payload.get("robot_id", "unknown")),
              "part_family": str(row.payload.get("part_family", "unknown")),
              "condition": list(condition_cell(row)),
              "quarantined": alignment(row).quarantine} for row in rows]
    items.sort(key=lambda item: item["session_id"])
    return {"items": items, "coverage": coverage_lattice(rows)}


def seal_dataset(connection: sqlite3.Connection, dataset_id: str, records: Iterable[DomainRecord]) -> dict[str, Any]:
    prepare_datasets(connection)
    assembled = assemble_dataset(records)
    identity = stable_hash(assembled)
    existing = connection.execute("SELECT snapshot_hash FROM sealed_datasets WHERE dataset_id=?", (dataset_id,)).fetchone()
    if existing:
        if existing[0] != identity:
            raise ContractError("a sealed dataset cannot change after publication")
        return read_dataset(connection, dataset_id)
    connection.execute("INSERT INTO sealed_datasets VALUES(?,?,?,?,?)",
                       (dataset_id, identity, len(assembled["items"]),
                        canonical_json(assembled["coverage"]), utc_now()))
    for item in assembled["items"]:
        connection.execute("INSERT INTO sealed_dataset_items VALUES(?,?,?,?,?,?,?,?)",
                           (dataset_id, item["session_id"], item["session_version"],
                            item["record_fingerprint"], item["robot_id"], item["part_family"],
                            canonical_json(item["condition"]), int(item["quarantined"])))
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
    return {"dataset_id": dataset_id, "snapshot_hash": header["snapshot_hash"],
            "created_at": header["created_at"], "coverage": json.loads(header["coverage_json"]),
            "item_count": header["item_count"], "items": items}
