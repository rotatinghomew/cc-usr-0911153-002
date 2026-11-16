from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from robot_corpus.session.contracts import ContractError, Decision, DomainRecord, records_from_fixture, stable_hash
from robot_corpus.lineage.evidence_store import Repository
from robot_corpus.orchestration.session_lifecycle import advance_for_outcome, decide
from robot_corpus.delivery.dataset_manifest import export_bundle, verify_bundle
from robot_corpus.synchronization.timeline import coverage_gap_report, coverage_lattice, derive_context, quarantine_reasons


class Application:
    def __init__(self, database: str | Path, context: Mapping[str, Any] | None = None):
        self.repository = Repository(database)
        self.context = dict(context or {})

    def ingest(self, record: DomainRecord) -> DomainRecord:
        current = self.repository.get_record(record.record_id)
        if current is None:
            self.repository.save_record(record)
            return record
        if current.fingerprint == record.fingerprint:
            return current
        replacement = DomainRecord(record.record_id, record.payload, current.state,
                                   current.version + 1, record.occurred_at, record.source)
        self.repository.save_record(replacement, expected_version=current.version)
        return replacement

    def process(self, record: DomainRecord) -> tuple[DomainRecord, Decision]:
        stored = self.ingest(record)
        context = dict(self.context)
        context.update(derive_context(stored, self.repository))
        decision = decide(stored, context)
        self.repository.save_decision(decision)
        advanced = advance_for_outcome(stored, decision)
        if advanced.fingerprint != stored.fingerprint:
            self.repository.save_record(advanced, expected_version=stored.version)
        return advanced, decision

    def run_fixture(self, fixture: Mapping[str, Any], output: str | Path) -> dict[str, Any]:
        records = records_from_fixture(fixture)
        fixture_hash = stable_hash(fixture)
        run_id = self.repository.begin_run(fixture_hash, len(records))
        completed = self.repository.completed_run(run_id)
        if completed is not None:
            return completed
        decisions: dict[str, Decision] = {}
        final_records: list[DomainRecord] = []
        for record in records:
            final_record, decision = self.process(record)
            final_records.append(final_record)
            decisions[record.record_id] = decision
        snapshot = self.repository.snapshot()
        if snapshot["chain_errors"]:
            raise ContractError("audit chain verification failed")
        manifest = export_bundle(output, final_records, decisions, snapshot, self.repository.event_rows())
        result = {"run_id": run_id, "fixture_hash": fixture_hash, "records": len(final_records),
                  "decisions": len(decisions), "manifest": manifest, "snapshot": snapshot}
        self.repository.finish_run(run_id, result)
        return result

    def inspect(self) -> dict[str, Any]:
        return {"snapshot": self.repository.snapshot(), "records": [record.__dict__ for record in self.repository.list_records()],
                "decisions": self.repository.decision_rows()}

    def publish_dataset(self, dataset_id: str, session_ids: list[str]) -> dict[str, Any]:
        return self.repository.publish_dataset(dataset_id, session_ids)

    def dataset_manifest(self, dataset_id: str) -> dict[str, Any]:
        return self.repository.dataset_manifest(dataset_id)

    def review_dataset(self, dataset_id: str) -> dict[str, Any]:
        """Read-only post-seal review opinion; the sealed manifest stays unchanged."""
        return self.repository.review_dataset(dataset_id)

    def coverage_report(self) -> dict[str, Any]:
        """Current usable coverage plus per-cell gap and quarantine evidence."""
        records = self.repository.list_records()
        gaps = coverage_gap_report(records)
        return {"coverage": coverage_lattice(records), "gaps": gaps,
                "quarantine_evidence": [
                    {"record_id": record.record_id, "state": record.state, "version": record.version,
                     "reasons": list(quarantine_reasons(record))}
                    for record in records if quarantine_reasons(record)]}

    def reevaluate(self, record_ids: list[str] | None = None) -> dict[str, Any]:
        """Re-run quality admission after corrections, then recompute affected coverage.

        Correcting a fragment is not "lowering a total score": each affected session is
        re-adjudicated against the authoritative alignment quarantine, its workflow state
        advances or stays isolated, and the coverage gaps / unsealed sessions are
        recomputed from the resulting usable evidence.
        """
        targets = record_ids or [record.record_id for record in self.repository.list_records()]
        outcomes: dict[str, str] = {}
        for record_id in targets:
            stored = self.repository.get_record(record_id)
            if stored is None:
                raise ContractError(f"unknown capture session: {record_id}")
            context = dict(self.context)
            context.update(derive_context(stored, self.repository))
            decision = decide(stored, context)
            self.repository.save_decision(decision)
            advanced = advance_for_outcome(stored, decision)
            if advanced.fingerprint != stored.fingerprint:
                self.repository.save_record(advanced, expected_version=stored.version)
            outcomes[record_id] = decision.outcome
        before = self.coverage_report()
        return {"reevaluated": outcomes, "coverage": before["coverage"], "gaps": before["gaps"],
                "quarantine_evidence": before["quarantine_evidence"]}


def load_fixture(path: str | Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read fixture: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("fixture root must be an object")
    return value


def run(fixture_path: str | Path, database: str | Path, output: str | Path,
        context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return Application(database, context).run_fixture(load_fixture(fixture_path), output)


def verify(database: str | Path, output: str | Path) -> dict[str, Any]:
    repository = Repository(database)
    chain_errors = repository.verify_chain()
    bundle_errors = verify_bundle(output)
    return {"ok": not chain_errors and not bundle_errors, "chain_errors": chain_errors,
            "bundle_errors": bundle_errors, "snapshot": repository.snapshot()}
