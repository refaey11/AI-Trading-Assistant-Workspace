#!/usr/bin/env python3
"""Frozen 2025 OOS candidate gate.

Evaluates PRE-SPECIFIED candidates only. It must never tune thresholds, infer
signals, or use 2025 to select candidates. Inputs are governed producer/event
streams plus already-produced as-of context and realized outcomes.

Candidates frozen from 2016-2024 discovery:
  1) volatility_state=HIGH AND mtf_context=strong_bearish
  2) volatility_state=HIGH AND H4_trend_regime=-1
  3) direction=SELL AND volatility_state=HIGH

The script fails closed if 2025 is absent, required context/outcome columns are
missing, timestamps are invalid, or any candidate is redefined at runtime.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

CANDIDATES = {
    "C1_HIGH_STRONG_BEARISH_MTF": {"volatility_state": "HIGH", "mtf_context": "strong_bearish"},
    "C2_HIGH_H4_BEARISH": {"volatility_state": "HIGH", "H4_trend_regime": "-1"},
    "C3_SELL_HIGH": {"direction": "SELL", "volatility_state": "HIGH"},
}

REQUIRED = {"event_time", "direction", "net_R", "volatility_state", "mtf_context", "H4_trend_regime"}

def stats(g: pd.DataFrame) -> dict:
    r = pd.to_numeric(g["net_R"], errors="coerce").dropna()
    wins = float(r[r > 0].sum())
    losses = float(-r[r < 0].sum())
    return {
        "trades": int(len(r)),
        "wins": int((r > 0).sum()),
        "losses": int((r < 0).sum()),
        "win_rate": float((r > 0).mean()) if len(r) else None,
        "expectancy_R": float(r.mean()) if len(r) else None,
        "profit_factor": (wins / losses) if losses else (float("inf") if wins else None),
        "total_net_R": float(r.sum()) if len(r) else 0.0,
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("EDGE_DISCOVERY/out/oos_2025"))
    args = ap.parse_args()
    df = pd.read_csv(args.input_csv)
    missing = sorted(REQUIRED - set(df.columns))
    if missing:
        raise SystemExit(f"FAIL_CLOSED missing columns: {missing}")
    df["event_time"] = pd.to_datetime(df["event_time"], utc=True, errors="coerce")
    if df["event_time"].isna().any():
        raise SystemExit("FAIL_CLOSED invalid event_time")
    years = set(df["event_time"].dt.year.astype(int))
    if years != {2025}:
        raise SystemExit(f"FAIL_CLOSED expected ONLY 2025 input, got years={sorted(years)}")
    df["direction"] = df["direction"].astype(str).str.upper()
    df["volatility_state"] = df["volatility_state"].astype(str).str.upper()
    df["mtf_context"] = df["mtf_context"].astype(str).str.lower()
    df["H4_trend_regime"] = df["H4_trend_regime"].astype(str)
    rows = []
    for cid, cond in CANDIDATES.items():
        mask = pd.Series(True, index=df.index)
        for col, val in cond.items():
            mask &= df[col].eq(val)
        g = df.loc[mask]
        rows.append({"candidate_id": cid, **cond, **stats(g)})
    out = pd.DataFrame(rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out_dir / "oos_2025_candidate_results.csv", index=False)
    manifest = {
        "window": "2025-only",
        "candidate_set": list(CANDIDATES),
        "candidate_set_frozen": True,
        "tuning_applied": False,
        "threshold_sweep": False,
        "future_data_used": False,
        "input_years": sorted(years),
        "status": "OOS_2025_EVALUATION",
    }
    (args.out_dir / "oos_2025_candidate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(out.to_string(index=False))
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    raise SystemExit(main())
