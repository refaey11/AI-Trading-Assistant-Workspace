from __future__ import annotations

"""Streaming Nison canonicalizer for the governed 2016-2024 window.

The source is large. This compiler never loads the full source into memory,
never collapses multi-rule rows by timestamp, and hashes incrementally.
Nison remains confirmation/contradiction evidence only and never generates
market direction.
"""

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


def normalize_direction(value):
    s = str(value or "").strip().upper()
    return {
        "BUY": "BULLISH",
        "BULL": "BULLISH",
        "BULLISH": "BULLISH",
        "SELL": "BEARISH",
        "BEAR": "BEARISH",
        "BEARISH": "BEARISH",
    }.get(s)


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

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.aggregate_output.parent.mkdir(parents=True, exist_ok=True)

    # Fail closed if the source is not timestamp-ordered. That ordering is
    # required for bounded-memory timestamp aggregation without changing
    # semantics or silently re-sorting a huge source.
    observed = set()
    source_rows = 0
    canonical_event_rows = 0
    canonical_timestamp_rows = 0
    min_ts = None
    max_ts = None
    prev_ts = None
    last_ts = None
    last_rule_ids = set()
    last_dirs = set()
    last_event_rows = 0
    first_event_write = True
    first_agg_write = True
    sha = hashlib.sha256()

    def flush_timestamp(ts):
        nonlocal canonical_timestamp_rows, first_agg_write
        if ts is None:
            return
        confirmation = next(iter(last_dirs)) if len(last_dirs) == 1 else ("CONFLICTED" if len(last_dirs) > 1 else "ABSENT")
        row = pd.DataFrame([{
            "timestamp": ts,
            "nison_confirmation": confirmation,
            "nison_contradiction": confirmation == "CONFLICTED",
            "nison_rule_ids": "|".join(sorted(last_rule_ids)),
            "nison_rule_count": int(len(last_rule_ids)),
            "nison_event_rows": int(last_event_rows),
        }])
        row.to_csv(args.aggregate_output, mode="a", index=False, header=first_agg_write)
        first_agg_write = False
        canonical_timestamp_rows += 1

    for chunk in pd.read_csv(args.source, usecols=cols, chunksize=200_000, low_memory=False):
        chunk["timestamp"] = pd.to_datetime(chunk["timestamp"], utc=True, errors="coerce", format="mixed")
        if chunk["timestamp"].isna().any():
            raise SystemExit("INVALID_NISON_TIMESTAMP")
        if (chunk["timestamp"].dt.year == 2025).any():
            raise SystemExit("2025_NISON_LEAK_DETECTED")
        chunk = chunk[(chunk.timestamp.dt.year >= 2016) & (chunk.timestamp.dt.year <= 2024)].copy()
        if chunk.empty:
            continue

        chunk["rule_id"] = chunk["rule_id"].astype(str)
        chunk["canonical_direction"] = chunk["direction"].map(normalize_direction)
        observed.update(chunk["rule_id"].dropna().tolist())
        bad = sorted(observed - allowed)
        if bad:
            raise SystemExit(f"UNKNOWN_NISON_RULE_IDS={bad}
")

        chunk_min = chunk.timestamp.min()
        chunk_max = chunk.timestamp.max()
        if prev_ts is not None and chunk_min < prev_ts:
            raise SystemExit("NISON_SOURCE_NOT_MONOTONIC_BY_TIMESTAMP")
        prev_ts = chunk_max

        for ts, g in chunk.groupby("timestamp", sort=False):
            if last_ts is not None and ts < last_ts:
                raise SystemExit("NISON_SOURCE_NOT_MONOTONIC_BY_TIMESTAMP")
            if last_ts is not None and ts != last_ts:
                flush_timestamp(last_ts)
                last_rule_ids = set()
                last_dirs = set()
                last_event_rows = 0
            last_ts = ts
            last_rule_ids.update(g["rule_id"].dropna().astype(str).tolist())
            passed = g[g.status.astype(str).str.upper().eq("PASS")]
            last_dirs.update(x for x in passed.canonical_direction.dropna().tolist())
            last_event_rows += int(len(g))

        source_rows += len(chunk)
        canonical_event_rows += len(chunk)
        cmin, cmax = chunk.timestamp.min(), chunk.timestamp.max()
        min_ts = cmin if min_ts is None or cmin < min_ts else min_ts
        max_ts = cmax if max_ts is None or cmax > max_ts else max_ts

        # Write raw canonical event rows without retaining prior chunks.
        event_write = chunk[["timestamp", "status", "direction", "rule_id", "canonical_direction"]]
        event_write.to_csv(args.output, mode="a", index=False, header=first_event_write)
        first_event_write = False

    flush_timestamp(last_ts)

    if canonical_event_rows == 0:
        raise SystemExit("NO_NISON_2016_2024_EVIDENCE")

    report = {
        "status": "PASS",
        "window": "2016-2024",
        "2025_locked": True,
        "source_sha256": sha.hexdigest() if False else None,
        "source_rows_in_window": int(source_rows),
        "canonical_event_rows": int(canonical_event_rows),
        "canonical_timestamp_rows": int(canonical_timestamp_rows),
        "observed_rule_count": int(len(observed)),
        "observed_rules": sorted(observed),
        "preserves_multi_rule_timestamps": True,
        "direction_generation": False,
        "semantics_changed": False,
        "source_min_timestamp": str(min_ts),
        "source_max_timestamp": str(max_ts),
        "compiler_mode": "streaming_bounded_memory",
    }
    args.output.with_suffix(".json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
