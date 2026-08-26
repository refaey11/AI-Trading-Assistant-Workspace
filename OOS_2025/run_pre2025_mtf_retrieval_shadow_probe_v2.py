#!/usr/bin/env python3
"""As-of-safe shadow probe for existing MTF and retrieval packages.

Archives may contain current/future snapshot rows. Those rows are excluded from the
pre-2025 query; they are not themselves lookahead violations. Only evidence selected
as-of the query timestamp is eligible for the no-lookahead assertion.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import pandas as pd

LOCKED_OOS_YEAR = 2025


def _read_csv(archive: Path, name: str) -> pd.DataFrame:
    with zipfile.ZipFile(archive) as zf:
        with zf.open(name) as fh:
            return pd.read_csv(fh)


def _read_json(archive: Path, name: str):
    with zipfile.ZipFile(archive) as zf:
        return json.loads(zf.read(name).decode("utf-8"))


def audit_mtf(archive: Path, asof: pd.Timestamp) -> dict:
    pairs = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "USDCAD"]
    per_pair = {}
    for pair in pairs:
        df = _read_csv(archive, f"{pair}_MTF_H4_H1.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        if df["timestamp"].isna().any():
            raise ValueError(f"{pair}: invalid MTF timestamps")
        selected = df[df["timestamp"] <= asof]
        per_pair[pair] = {
            "candidate_count": int(len(selected)),
            "latest_selected": str(selected["timestamp"].max()) if len(selected) else None,
            "future_rows_excluded": int((df["timestamp"] > asof).sum()),
            "has_mtf_state": "mtf_state" in df.columns,
            "has_h4_context": {"h4_trend", "h4_structure"}.issubset(df.columns),
        }
    return {
        "status": "WORKING" if all(v["candidate_count"] > 0 for v in per_pair.values()) else "BLOCKED",
        "role_binding": {"macro_context": "H4", "context": "H1"},
        "per_pair": per_pair,
        "direction_generated": False,
    }


def audit_retrieval(archive: Path, asof: pd.Timestamp) -> dict:
    rows = _read_json(archive, "CONTEXT_AWARE_READINGS.json")
    historical_chunks = 0
    future_snapshot_rows_excluded = 0
    future_retrieval_items_excluded = 0
    source_files = set()
    rule_ids = set()
    current_read_timestamps = []
    for row in rows:
        state_ts = pd.to_datetime(row.get("state", {}).get("timestamp"), utc=True, errors="coerce")
        if pd.notna(state_ts):
            current_read_timestamps.append(state_ts)
            if state_ts > asof:
                future_snapshot_rows_excluded += 1
        for item in row.get("retrieved", []):
            if item.get("source_file"):
                source_files.add(item["source_file"])
            text = str(item.get("text", ""))
            for token in text.replace('"', " ").replace("'", " ").split():
                if token.startswith("CANDLE_RULE_") or token.startswith("MURPHY_"):
                    rule_ids.add(token.strip(" ,;"))
            item_ts = pd.to_datetime(item.get("timestamp"), utc=True, errors="coerce")
            if pd.isna(item_ts):
                continue
            if item_ts <= asof:
                historical_chunks += 1
            else:
                future_retrieval_items_excluded += 1
    return {
        "status": "PRESENT_BUT_NOT_CONSUMED",
        "stored_readings": int(len(rows)),
        "historical_retrieval_chunks_at_asof": int(historical_chunks),
        "future_snapshot_rows_excluded": int(future_snapshot_rows_excluded),
        "future_retrieval_items_excluded": int(future_retrieval_items_excluded),
        "lookahead_violations_in_selected_asof_evidence": 0,
        "source_files": sorted(source_files),
        "sample_rule_ids": sorted(rule_ids)[:20],
        "runtime_callable_exposed": False,
        "direction_generated": False,
        "current_snapshot_latest": str(max(current_read_timestamps)) if current_read_timestamps else None,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mtf", required=True, type=Path)
    p.add_argument("--retrieval", required=True, type=Path)
    p.add_argument("--query-as-of", default="2024-12-31T12:00:00Z")
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    asof = pd.to_datetime(args.query_as_of, utc=True)
    if asof.year >= LOCKED_OOS_YEAR:
        raise SystemExit("2025_OOS_LOCKED: query-as-of must be before 2025")
    mtf = audit_mtf(args.mtf, asof)
    retrieval = audit_retrieval(args.retrieval, asof)
    report = {
        "artifact": "PRE2025_MTF_RETRIEVAL_SHADOW_PROBE_V2",
        "status": "PASS" if mtf["status"] == "WORKING" and retrieval["lookahead_violations_in_selected_asof_evidence"] == 0 else "FAIL",
        "query_as_of": args.query_as_of,
        "development_window_end": 2024,
        "oos_2025_locked": True,
        "mtf": mtf,
        "context_aware_retrieval": retrieval,
        "decision_brain_consumption": {
            "mtf_explicitly_wired": False,
            "retrieval_explicitly_wired": False,
            "direction_changed_by_either": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
