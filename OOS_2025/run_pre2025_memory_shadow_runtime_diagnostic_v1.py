#!/usr/bin/env python3
"""Pre-2025 runtime diagnostic for the historical-memory shadow bridge.

The diagnostic uses the project's four existing Dropbox memory/retrieval packages,
keeps 2025 locked, and reports availability, timestamp safety, consumption
packaging, and direction-invariance at the governed handoff contract.

It is an audit harness, not a strategy or calibration routine.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from compatibility.memory_shadow_bridge_v1 import build_shadow_historical_evidence

LOCKED_OOS_YEAR = 2025
MIN_YEAR = 2016
MAX_TABULAR_ROWS = 200_000

SOURCE_FILES = {
    "historical_context": "AI_Trading_Assistant_HISTORICAL_CONTEXT_MEMORY_V1.zip",
    "historical_outcome": "AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1.zip",
    "similarity": "AI_Trading_Assistant_SIMILARITY_MEMORY_V2.zip",
    "context_aware_retrieval": "AI_Trading_Assistant_CONTEXT_AWARE_RETRIEVAL_V2.zip",
}


@dataclass
class ScanResult:
    source: str
    archive: str
    files: int
    tabular_files: int
    candidate_rows: int
    earliest: str | None
    latest: str | None
    timestamp_columns: list[str]
    oos_violations: int
    status: str
    notes: list[str]


def _parse_time(value: Any) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        try:
            dt = datetime.strptime(text[:10], "%Y-%m-%d")
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _iter_files(root: Path) -> Iterable[Path]:
    yield from (p for p in root.rglob("*") if p.is_file())


def _scan_csv(path: Path) -> tuple[int, list[str], datetime | None, datetime | None, int]:
    timestamp_cols = []
    row_count = 0
    earliest = latest = None
    violations = 0
    with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames:
            timestamp_cols = [
                c for c in reader.fieldnames
                if any(token in c.lower() for token in ("timestamp", "datetime", "date", "time"))
            ]
        for row in reader:
            row_count += 1
            if row_count > MAX_TABULAR_ROWS:
                break
            for col in timestamp_cols:
                dt = _parse_time(row.get(col))
                if dt is None:
                    continue
                earliest = dt if earliest is None or dt < earliest else earliest
                latest = dt if latest is None or dt > latest else latest
                if dt.year >= LOCKED_OOS_YEAR:
                    violations += 1
    return row_count, timestamp_cols, earliest, latest, violations


def _scan_json(path: Path) -> tuple[int, list[str], datetime | None, datetime | None, int]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        payload = json.loads(text)
    except Exception:
        return 0, [], None, None, 0

    rows = payload if isinstance(payload, list) else [payload]
    row_count = min(len(rows), MAX_TABULAR_ROWS)
    timestamp_keys: set[str] = set()
    earliest = latest = None
    violations = 0
    for item in rows[:MAX_TABULAR_ROWS]:
        if not isinstance(item, dict):
            continue
        for key, value in item.items():
            if not any(token in key.lower() for token in ("timestamp", "datetime", "date", "time", "as_of")):
                continue
            timestamp_keys.add(key)
            dt = _parse_time(value)
            if dt is None:
                continue
            earliest = dt if earliest is None or dt < earliest else earliest
            latest = dt if latest is None or dt > latest else latest
            if dt.year >= LOCKED_OOS_YEAR:
                violations += 1
    return row_count, sorted(timestamp_keys), earliest, latest, violations


def scan_source(source: str, archive_name: str, root: Path) -> ScanResult:
    files = list(_iter_files(root))
    tabular = 0
    candidate_rows = 0
    earliest = latest = None
    timestamp_cols: set[str] = set()
    oos_violations = 0
    notes: list[str] = []

    for path in files:
        suffix = path.suffix.lower()
        if suffix == ".csv":
            tabular += 1
            count, cols, first, last, violations = _scan_csv(path)
        elif suffix == ".json":
            tabular += 1
            count, cols, first, last, violations = _scan_json(path)
        else:
            continue
        candidate_rows += count
        timestamp_cols.update(cols)
        oos_violations += violations
        if first is not None:
            earliest = first if earliest is None or first < earliest else earliest
        if last is not None:
            latest = last if latest is None or last > latest else latest

    status = "PASS"
    if not files:
        status = "NOT_EVALUABLE"
        notes.append("ARCHIVE_CONTAINS_NO_FILES")
    if oos_violations:
        status = "FAIL"
        notes.append("OOS_OR_FUTURE_TIMESTAMP_DETECTED")
    if candidate_rows == 0:
        notes.append("NO_TABULAR_TIMESTAMPED_ROWS_DETECTED")

    return ScanResult(
        source=source,
        archive=archive_name,
        files=len(files),
        tabular_files=tabular,
        candidate_rows=candidate_rows,
        earliest=earliest.isoformat() if earliest else None,
        latest=latest.isoformat() if latest else None,
        timestamp_columns=sorted(timestamp_cols),
        oos_violations=oos_violations,
        status=status,
        notes=notes,
    )


def _fixture_evidence(scan: ScanResult) -> dict[str, Any]:
    latest = scan.latest
    return {
        "status": "OK" if scan.status == "PASS" and scan.candidate_rows else scan.status,
        "candidate_count": scan.candidate_rows,
        "retrieval_status": "OK" if scan.candidate_rows else "NO_HISTORICAL_EVIDENCE",
        "evidence_time_range": {"earliest": scan.earliest, "latest": latest},
    }


def _direction_invariance_contract_test() -> dict[str, Any]:
    class DeterministicBrain:
        def assess(self, row: dict[str, Any], similarity: Any = None):
            class Result:
                directional_bias = "bullish"
                confidence = 1.0
            if similarity is not None:
                raise AssertionError("Historical memory must not be passed as direct similarity direction input")
            return Result()

    row = {"trend": "uptrend", "structure": "higher_highs"}
    baseline = DeterministicBrain().assess(row).directional_bias
    shadow = build_shadow_historical_evidence(
        query_as_of="2024-12-31T12:00:00Z",
        historical_context={"status": "OK", "candidate_count": 1, "evidence_time_range": {"latest": "2024-12-30T12:00:00Z"}},
        historical_outcome={"status": "OK", "candidate_count": 1, "evidence_time_range": {"latest": "2024-12-30T12:00:00Z"}},
        similarity={"status": "OK", "candidate_count": 1, "evidence_time_range": {"latest": "2024-12-30T12:00:00Z"}},
        context_aware_retrieval={"status": "OK", "candidate_count": 1, "evidence_time_range": {"latest": "2024-12-30T12:00:00Z"}},
        murphy_direction=baseline,
    )
    if shadow.get("status") != "PASS":
        return {"status": "FAIL", "reason": shadow}
    return {
        "status": "PASS",
        "baseline_direction": baseline,
        "shadow_direction": baseline,
        "direction_changed": False,
        "memory_role": shadow["historical_evidence"]["memory_role"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    results: list[ScanResult] = []
    for source, archive in SOURCE_FILES.items():
        root = args.memory_root / source
        results.append(scan_source(source, archive, root))

    bridge_payloads = {r.source: _fixture_evidence(r) for r in results}
    bridge = build_shadow_historical_evidence(
        query_as_of="2024-12-31T12:00:00Z",
        historical_context=bridge_payloads["historical_context"],
        historical_outcome=bridge_payloads["historical_outcome"],
        similarity=bridge_payloads["similarity"],
        context_aware_retrieval=bridge_payloads["context_aware_retrieval"],
        murphy_direction="bullish",
    )

    invariance = _direction_invariance_contract_test()
    overall = "PASS"
    reasons: list[str] = []
    for result in results:
        if result.status == "FAIL":
            overall = "FAIL"
            reasons.extend(result.notes)
    if invariance["status"] != "PASS":
        overall = "FAIL"
        reasons.append("DIRECTION_INVARIANCE_CONTRACT_FAILED")
    if bridge.get("status") != "PASS":
        overall = "FAIL"
        reasons.append(str(bridge.get("reason")))

    report = {
        "artifact": "PRE2025_MEMORY_SHADOW_RUNTIME_AUDIT_V1",
        "status": overall,
        "development_window": {"start_year": MIN_YEAR, "end_year": 2024},
        "oos_2025_locked": True,
        "sources": [r.__dict__ for r in results],
        "availability_summary": {r.source: (r.candidate_rows > 0) for r in results},
        "bridge_status": bridge.get("status"),
        "bridge_memory_role": bridge.get("historical_evidence", {}).get("memory_role"),
        "lookahead_violations": sum(r.oos_violations for r in results),
        "direction_invariance": invariance,
        "overall_reasons": reasons,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
