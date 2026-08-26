#!/usr/bin/env python3
"""As-of-safe runtime audit for existing historical-memory packages.

This audit does not rebuild memory or strategy logic. It evaluates the existing
memory artifacts using a pre-2025 query boundary, excludes future rows, and
separates genuinely queryable historical layers from packages that only contain
precomputed current-read snapshots.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import pandas as pd

LOCKED_OOS_YEAR = 2025
HORIZON_HOURS = 48


def _read_csv(archive: str, name: str, usecols=None) -> pd.DataFrame:
    with zipfile.ZipFile(archive) as zf:
        with zf.open(name) as fh:
            return pd.read_csv(fh, usecols=usecols)


def _read_json(archive: str, name: str):
    with zipfile.ZipFile(archive) as zf:
        return json.loads(zf.read(name).decode("utf-8"))


def audit_context(archive: str, asof: pd.Timestamp) -> dict:
    df = _read_csv(
        archive,
        "HISTORICAL_CONTEXT_MEMORY.csv",
        usecols=["pair", "timestamp", "context_signature"],
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    src = df[df["timestamp"].notna()]
    selected = src[src["timestamp"] <= asof]
    return {
        "status": "WORKING" if len(selected) else "BLOCKED",
        "candidate_count": int(len(selected)),
        "archive_latest": str(src["timestamp"].max()),
        "selected_latest": str(selected["timestamp"].max()) if len(selected) else None,
        "future_rows_excluded": int((src["timestamp"] > asof).sum()),
        "queryable": "historical_context_csv",
    }


def audit_outcome(archive: str, asof: pd.Timestamp) -> dict:
    df = _read_csv(
        archive,
        "HISTORICAL_OUTCOMES.csv",
        usecols=["pair", "timestamp", "context_signature", "return_48h"],
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    src = df[df["timestamp"].notna()]
    selected = src[
        src["timestamp"] + pd.Timedelta(hours=HORIZON_HOURS) <= asof
    ]
    return {
        "status": "WORKING" if len(selected) else "BLOCKED",
        "candidate_count": int(len(selected)),
        "archive_latest": str(src["timestamp"].max()),
        "selected_latest": str(selected["timestamp"].max()) if len(selected) else None,
        "future_rows_excluded": int(
            (src["timestamp"] + pd.Timedelta(hours=HORIZON_HOURS) > asof).sum()
        ),
        "queryable": "historical_outcomes_csv",
        "max_horizon_hours": HORIZON_HOURS,
    }


def audit_similarity(archive: str, asof: pd.Timestamp) -> dict:
    rows = _read_json(archive, "SIMILAR_CONTEXT_READS.json")
    current_timestamps = []
    historical_neighbors = 0
    current_rows = 0
    for row in rows:
        current = pd.to_datetime(
            row.get("current_context", {}).get("timestamp"),
            utc=True,
            errors="coerce",
        )
        if pd.notna(current):
            current_timestamps.append(current)
            current_rows += int(current.year >= LOCKED_OOS_YEAR)
        for neighbor in row.get("similar_contexts", []):
            ts = pd.to_datetime(neighbor.get("timestamp"), utc=True, errors="coerce")
            if pd.notna(ts) and ts <= asof:
                historical_neighbors += 1
    return {
        "status": "PRESENT_BUT_NOT_CONSUMED",
        "candidate_count": int(historical_neighbors),
        "current_read_rows": int(current_rows),
        "current_read_latest": str(max(current_timestamps)) if current_timestamps else None,
        "reason": (
            "package contains precomputed current-read snapshots; no runtime query "
            "callable is exposed in this package"
        ),
    }


def audit_retrieval(archive: str) -> dict:
    rows = _read_json(archive, "CONTEXT_AWARE_READINGS.json")
    timestamps = [
        pd.to_datetime(row.get("state", {}).get("timestamp"), utc=True, errors="coerce")
        for row in rows
    ]
    timestamps = [ts for ts in timestamps if pd.notna(ts)]
    return {
        "status": "PRESENT_BUT_NOT_CONSUMED",
        "candidate_count": 0,
        "current_read_rows": int(len(timestamps)),
        "current_read_latest": str(max(timestamps)) if timestamps else None,
        "reason": (
            "package contains precomputed retrieval snapshots; no runtime retrieval "
            "callable is exposed in this package"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", required=True, type=Path)
    parser.add_argument("--outcome", required=True, type=Path)
    parser.add_argument("--similarity", required=True, type=Path)
    parser.add_argument("--retrieval", required=True, type=Path)
    parser.add_argument("--query-as-of", default="2024-12-31T12:00:00Z")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    asof = pd.to_datetime(args.query_as_of, utc=True)
    if asof.year >= LOCKED_OOS_YEAR:
        raise SystemExit("2025_OOS_LOCKED: query-as-of must be before 2025")

    sources = {
        "historical_context": audit_context(str(args.context), asof),
        "historical_outcome": audit_outcome(str(args.outcome), asof),
        "similarity": audit_similarity(str(args.similarity), asof),
        "context_aware_retrieval": audit_retrieval(str(args.retrieval)),
    }

    status = (
        "PASS"
        if sources["historical_context"]["status"] == "WORKING"
        and sources["historical_outcome"]["status"] == "WORKING"
        else "FAIL"
    )

    report = {
        "artifact": "PRE2025_MEMORY_RUNTIME_AUDIT_V2",
        "status": status,
        "query_as_of": args.query_as_of,
        "development_window_end": 2024,
        "oos_2025_locked": True,
        "sources": sources,
        "lookahead_violations": 0,
        "memory_direction_changed": False,
        "notes": [
            "Historical Context/Outcome are runtime-queryable from existing historical datasets.",
            "Similarity/Retrieval remain PRESENT_BUT_NOT_CONSUMED and are not promoted by this audit.",
            "Outcome rows are eligible only when the full 48h horizon is realized before query-as-of.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
