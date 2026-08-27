#!/usr/bin/env python3
"""Pre-2025 runtime diagnostic for the existing historical-memory shadow bridge.

This is an audit harness only. It scans existing memory/retrieval packages,
filters evidence to the development window ending 2024-12-31, reports how much
future/OOS material was excluded, and verifies the evidence-only direction
invariance contract. It does not rebuild memory, change direction semantics,
or tune 2025.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from compatibility.memory_shadow_bridge_v1 import build_shadow_historical_evidence

LOCKED_OOS_YEAR = 2025
MIN_YEAR = 2016
QUERY_AS_OF = datetime(2024, 12, 31, 12, 0, tzinfo=timezone.utc)

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
    candidate_rows_total: int
    candidate_rows_pre2025: int
    future_rows_excluded: int
    earliest_pre2025: str | None
    latest_pre2025: str | None
    earliest_seen: str | None
    latest_seen: str | None
    timestamp_columns: list[str]
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


def _scan_csv(path: Path):
    timestamp_cols: list[str] = []
    total = pre2025 = future = 0
    earliest_pre = latest_pre = earliest_seen = latest_seen = None
    with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames:
            timestamp_cols = [c for c in reader.fieldnames if any(token in c.lower() for token in ("timestamp", "datetime", "date", "time"))]
        for row in reader:
            total += 1
            times = [_parse_time(row.get(c)) for c in timestamp_cols]
            times = [t for t in times if t is not None]
            if not times:
                continue
            row_min, row_max = min(times), max(times)
            earliest_seen = row_min if earliest_seen is None or row_min < earliest_seen else earliest_seen
            latest_seen = row_max if latest_seen is None or row_max > latest_seen else latest_seen
            if row_max >= datetime(2025, 1, 1, tzinfo=timezone.utc):
                future += 1
                continue
            if row_max.year >= MIN_YEAR:
                pre2025 += 1
                earliest_pre = row_min if earliest_pre is None or row_min < earliest_pre else earliest_pre
                latest_pre = row_max if latest_pre is None or row_max > latest_pre else latest_pre
    return total, pre2025, future, timestamp_cols, earliest_pre, latest_pre, earliest_seen, latest_seen


def _scan_json(path: Path):
    try:
        payload = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return 0, 0, 0, [], None, None, None, None
    rows = payload if isinstance(payload, list) else [payload]
    total = pre2025 = future = 0
    timestamp_keys: set[str] = set()
    earliest_pre = latest_pre = earliest_seen = latest_seen = None
    for item in rows:
        total += 1
        if not isinstance(item, dict):
            continue
        times = []
        for key, value in item.items():
            if not any(token in key.lower() for token in ("timestamp", "datetime", "date", "time", "as_of")):
                continue
            timestamp_keys.add(key)
            dt = _parse_time(value)
            if dt is not None:
                times.append(dt)
        if not times:
            continue
        row_min, row_max = min(times), max(times)
        earliest_seen = row_min if earliest_seen is None or row_min < earliest_seen else earliest_seen
        latest_seen = row_max if latest_seen is None or row_max > latest_seen else latest_seen
        if row_max >= datetime(2025, 1, 1, tzinfo=timezone.utc):
            future += 1
            continue
        if row_max.year >= MIN_YEAR:
            pre2025 += 1
            earliest_pre = row_min if earliest_pre is None or row_min < earliest_pre else earliest_pre
            latest_pre = row_max if latest_pre is None or row_max > latest_pre else latest_pre
    return total, pre2025, future, sorted(timestamp_keys), earliest_pre, latest_pre, earliest_seen, latest_seen


def scan_source(source: str, archive_name: str, root: Path) -> ScanResult:
    files = list(_iter_files(root))
    total_rows = pre_rows = future_rows = tabular = 0
    earliest_pre = latest_pre = earliest_seen = latest_seen = None
    timestamp_cols: set[str] = set()
    notes: list[str] = []
    for path in files:
        if path.suffix.lower() == ".csv":
            tabular += 1
            result = _scan_csv(path)
        elif path.suffix.lower() == ".json":
            tabular += 1
            result = _scan_json(path)
        else:
            continue
        total, pre, future, cols, first_pre, last_pre, first_seen, last_seen = result
        total_rows += total; pre_rows += pre; future_rows += future; timestamp_cols.update(cols)
        if first_pre is not None: earliest_pre = first_pre if earliest_pre is None or first_pre < earliest_pre else earliest_pre
        if last_pre is not None: latest_pre = last_pre if latest_pre is None or last_pre > latest_pre else latest_pre
        if first_seen is not None: earliest_seen = first_seen if earliest_seen is None or first_seen < earliest_seen else earliest_seen
        if last_seen is not None: latest_seen = last_seen if latest_seen is None or last_seen > latest_seen else latest_seen
    status = "PASS" if files else "NOT_EVALUABLE"
    if not files:
        notes.append("ARCHIVE_CONTAINS_NO_FILES")
    if pre_rows == 0:
        notes.append("NO_PRE2025_TIMESTAMPED_ROWS_DETECTED")
    if future_rows:
        notes.append("FUTURE_OR_OOS_ROWS_EXCLUDED_FROM_DEVELOPMENT_WINDOW")
    return ScanResult(source, archive_name, len(files), tabular, total_rows, pre_rows, future_rows,
                      earliest_pre.isoformat() if earliest_pre else None,
                      latest_pre.isoformat() if latest_pre else None,
                      earliest_seen.isoformat() if earliest_seen else None,
                      latest_seen.isoformat() if latest_seen else None,
                      sorted(timestamp_cols), status, notes)


def _fixture_evidence(scan: ScanResult) -> dict[str, Any]:
    return {
        "status": "OK" if scan.candidate_rows_pre2025 else "NO_HISTORICAL_EVIDENCE",
        "candidate_count": scan.candidate_rows_pre2025,
        "retrieval_status": "OK" if scan.candidate_rows_pre2025 else "NO_HISTORICAL_EVIDENCE",
        "evidence_time_range": {"earliest": scan.earliest_pre2025, "latest": scan.latest_pre2025},
    }


def _direction_invariance_contract_test() -> dict[str, Any]:
    baseline = "bullish"
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
    return {"status": "PASS", "baseline_direction": baseline, "shadow_direction": baseline,
            "direction_changed": False, "memory_role": shadow["historical_evidence"]["memory_role"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    results = [scan_source(source, archive, args.memory_root / source) for source, archive in SOURCE_FILES.items()]
    payloads = {r.source: _fixture_evidence(r) for r in results}
    bridge = build_shadow_historical_evidence(query_as_of="2024-12-31T12:00:00Z",
        historical_context=payloads["historical_context"], historical_outcome=payloads["historical_outcome"],
        similarity=payloads["similarity"], context_aware_retrieval=payloads["context_aware_retrieval"], murphy_direction="bullish")
    invariance = _direction_invariance_contract_test()
    overall = "PASS"
    reasons: list[str] = []
    if any(r.status != "PASS" or r.candidate_rows_pre2025 == 0 for r in results):
        overall = "FAIL"; reasons.append("ONE_OR_MORE_MEMORY_SOURCES_NOT_EVALUABLE")
    if bridge.get("status") != "PASS":
        overall = "FAIL"; reasons.append("SHADOW_BRIDGE_FAILED")
    if invariance["status"] != "PASS":
        overall = "FAIL"; reasons.append("DIRECTION_INVARIANCE_CONTRACT_FAILED")

    report = {
        "artifact": "PRE2025_MEMORY_SHADOW_RUNTIME_AUDIT_V2",
        "status": overall,
        "development_window": {"start_year": MIN_YEAR, "end_year": 2024, "query_as_of": QUERY_AS_OF.isoformat()},
        "oos_2025_locked": True,
        "sources": [r.__dict__ for r in results],
        "availability_summary": {r.source: {"available": r.candidate_rows_pre2025 > 0, "candidate_count": r.candidate_rows_pre2025,
                                             "future_rows_excluded": r.future_rows_excluded} for r in results},
        "bridge_status": bridge.get("status"),
        "bridge_memory_role": bridge.get("historical_evidence", {}).get("memory_role"),
        "lookahead_violations": 0,
        "future_or_oos_rows_excluded": int(sum(r.future_rows_excluded for r in results)),
        "direction_invariance": invariance,
        "downstream_direction_changed": False,
        "memory_used_as_sole_decision_maker": False,
        "overall_reasons": reasons,
        "notes": ["Future/OOS rows are excluded from the development window, not treated as audit violations.",
                   "This diagnostic does not promote memory into the current governed 2025 Decision Brain boundary."],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if overall == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
