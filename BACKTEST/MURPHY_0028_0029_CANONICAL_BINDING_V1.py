from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

RULE_BEAR = "MURPHY_0028"
RULE_BULL = "MURPHY_0029"
ALLOWED_YEARS = set(range(2020, 2025))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--report", required=True, type=Path)
    args = ap.parse_args()

    sources = sorted(args.root.rglob("GBPUSD_*_STRUCTURE_RSI_DIVERGENCE_V1.csv"))
    frames = []
    source_stats = []
    for p in sources:
        df = pd.read_csv(p, low_memory=False)
        required = {
            "timeframe", "divergence_type", "pivot_type", "pivot_1_timestamp",
            "pivot_2_timestamp", "availability_timestamp", "status",
        }
        if not required.issubset(df.columns):
            continue
        df["availability_timestamp"] = pd.to_datetime(df["availability_timestamp"], utc=True, errors="coerce")
        df["pivot_1_timestamp"] = pd.to_datetime(df["pivot_1_timestamp"], utc=True, errors="coerce")
        df["pivot_2_timestamp"] = pd.to_datetime(df["pivot_2_timestamp"], utc=True, errors="coerce")
        df = df[df["availability_timestamp"].notna()].copy()
        df = df[df["availability_timestamp"].dt.year.isin(ALLOWED_YEARS)].copy()
        df = df[df["status"].astype(str).eq("CONFIRMED_DIVERGENCE")].copy()
        if df.empty:
            continue
        # Strict source-order checks: both pivots must be known no later than availability.
        if (df["pivot_1_timestamp"] > df["availability_timestamp"]).any() or (df["pivot_2_timestamp"] > df["availability_timestamp"]).any():
            raise SystemExit(f"BLOCKED_FUTURE_PIVOT_AFTER_AVAILABILITY:{p}")
        df["source_artifact"] = str(p)
        frames.append(df)
        source_stats.append({"source": str(p), "rows": int(len(df)), "min_year": int(df["availability_timestamp"].dt.year.min()), "max_year": int(df["availability_timestamp"].dt.year.max())})

    if not frames:
        raise SystemExit("BLOCKED_NO_CONFIRMED_DIVERGENCE_SOURCES")

    src = pd.concat(frames, ignore_index=True, sort=False)
    rows = []
    for r in src.itertuples(index=False):
        div = str(r.divergence_type).upper()
        pivot = str(r.pivot_type).upper()
        if div == "BEARISH" and pivot == "HIGH":
            rule = RULE_BEAR
            direction = "BEARISH"
            opposite = RULE_BULL
        elif div == "BULLISH" and pivot == "LOW":
            rule = RULE_BULL
            direction = "BULLISH"
            opposite = RULE_BEAR
        else:
            continue
        common = {
            "timestamp": r.availability_timestamp,
            "rule_id": rule,
            "source_rule_id": rule,
            "status": "PASS",
            "direction": direction,
            "timeframe": r.timeframe,
            "evidence_status": r.status,
            "availability_timestamp": r.availability_timestamp,
            "pivot_1_timestamp": r.pivot_1_timestamp,
            "pivot_2_timestamp": r.pivot_2_timestamp,
            "divergence_type": div,
            "pivot_type": pivot,
            "source_artifact": r.source_artifact,
            "source_oscillator": getattr(r, "source_oscillator", ""),
        }
        rows.append(common)
        rows.append({**common, "rule_id": opposite, "source_rule_id": opposite, "status": "FAIL", "direction": "NONE"})

    out = pd.DataFrame(rows).drop_duplicates().sort_values(["timestamp", "rule_id", "source_artifact"], kind="mergesort")
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S%z")
    out["availability_timestamp"] = pd.to_datetime(out["availability_timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S%z")
    out["pivot_1_timestamp"] = pd.to_datetime(out["pivot_1_timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S%z")
    out["pivot_2_timestamp"] = pd.to_datetime(out["pivot_2_timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S%z")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    report = {
        "status": "PASS",
        "rules": [RULE_BEAR, RULE_BULL],
        "source_files": len(source_stats),
        "rows": int(len(out)),
        "availability_is_event_timestamp": True,
        "strict_future_pivot_check": True,
        "scope_years": [2020, 2021, 2022, 2023, 2024],
        "2025_used": False,
        "synthetic_evidence_generated": False,
        "thresholds_invented": False,
        "decision_brain_promotion": False,
        "note": "Canonical normalization only. Uses the existing confirmed-divergence artifact and its availability_timestamp; does not invent divergence logic or promote Decision Brain eligibility.",
        "source_stats": source_stats,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
