from __future__ import annotations

"""Streaming Nison canonicalizer for the governed 2016-2024 window.

The source is large; this compiler never loads it as one DataFrame and never
collapses multi-rule rows by timestamp. Nison remains confirmation/contradiction
evidence only and never generates market direction.
"""
import argparse, hashlib, json
from pathlib import Path
import pandas as pd


def normalize_direction(value):
    s = str(value or "").strip().upper()
    return {"BUY":"BULLISH", "BULL":"BULLISH", "BULLISH":"BULLISH",
            "SELL":"BEARISH", "BEAR":"BEARISH", "BEARISH":"BEARISH"}.get(s)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--aggregate-output", required=True, type=Path)
    ap.add_argument("--allowlist", required=True, type=Path)
    args = ap.parse_args()

    allow = json.loads(args.allowlist.read_text(encoding="utf-8"))
    allowed = set(allow["verified_runtime"]["NISON"])
    cols = ["timestamp", "status", "direction", "rule_id"]
    event_parts = []
    observed = set(); source_rows = 0; min_ts = None; max_ts = None

    for chunk in pd.read_csv(args.source, usecols=cols, chunksize=200_000, low_memory=False):
        chunk["timestamp"] = pd.to_datetime(chunk["timestamp"], utc=True, errors="coerce", format="mixed")
        if chunk["timestamp"].isna().any(): raise SystemExit("INVALID_NISON_TIMESTAMP")
        years = set(chunk["timestamp"].dt.year.astype(int).tolist())
        if 2025 in years: raise SystemExit("2025_NISON_LEAK_DETECTED")
        chunk = chunk[(chunk.timestamp.dt.year >= 2016) & (chunk.timestamp.dt.year <= 2024)].copy()
        if chunk.empty: continue
        chunk["rule_id"] = chunk["rule_id"].astype(str)
        chunk["canonical_direction"] = chunk["direction"].map(normalize_direction)
        observed.update(chunk["rule_id"].dropna().tolist())
        bad = sorted(observed - allowed)
        if bad: raise SystemExit(f"UNKNOWN_NISON_RULE_IDS={bad}")
        source_rows += len(chunk)
        cmin, cmax = chunk.timestamp.min(), chunk.timestamp.max()
        min_ts = cmin if min_ts is None or cmin < min_ts else min_ts
        max_ts = cmax if max_ts is None or cmax > max_ts else max_ts
        event_parts.append(chunk)

    if not event_parts: raise SystemExit("NO_NISON_2016_2024_EVIDENCE")
    events = pd.concat(event_parts, ignore_index=True).sort_values(["timestamp", "rule_id"]).reset_index(drop=True)
    args.output.parent.mkdir(parents=True, exist_ok=True); events.to_csv(args.output, index=False)
    aggregate=[]
    for ts,g in events.groupby("timestamp", sort=True):
        passed=g[g.status.astype(str).str.upper().eq("PASS")]; dirs={x for x in passed.canonical_direction.dropna()}
        confirmation=next(iter(dirs)) if len(dirs)==1 else ("CONFLICTED" if len(dirs)>1 else "ABSENT")
        aggregate.append({"timestamp":ts,"nison_confirmation":confirmation,"nison_contradiction":confirmation=="CONFLICTED","nison_rule_ids":"|".join(sorted(set(g.rule_id))),"nison_rule_count":int(g.rule_id.nunique()),"nison_event_rows":int(len(g))})
    agg=pd.DataFrame(aggregate); args.aggregate_output.parent.mkdir(parents=True, exist_ok=True); agg.to_csv(args.aggregate_output,index=False)
    report={"status":"PASS","window":"2016-2024","2025_locked":True,"source_sha256":hashlib.sha256(args.source.read_bytes()).hexdigest(),"source_rows_in_window":int(source_rows),"canonical_event_rows":int(len(events)),"canonical_timestamp_rows":int(len(agg)),"observed_rule_count":int(len(observed)),"observed_rules":sorted(observed),"preserves_multi_rule_timestamps":True,"direction_generation":False,"semantics_changed":False,"source_min_timestamp":str(min_ts),"source_max_timestamp":str(max_ts)}
    args.output.with_suffix(".json").write_text(json.dumps(report,indent=2),encoding="utf-8"); print(json.dumps(report,indent=2)); return 0

if __name__ == "__main__": raise SystemExit(main())
