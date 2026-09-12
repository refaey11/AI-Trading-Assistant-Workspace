#!/usr/bin/env python3
"""Deterministic Edge Ledger V1.

Analytical only: this script never creates trading signals and never changes
rule semantics. It consumes an existing governed event/trade CSV and produces
per-rule and yearly edge statistics. 2025 is rejected by default.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import math
import pandas as pd

REQUIRED = {"event_time", "rule_id", "direction", "status"}


def profit_factor(x: pd.Series) -> float | None:
    wins = x[x > 0].sum()
    losses = -x[x < 0].sum()
    if losses <= 0:
        return None if wins <= 0 else math.inf
    return float(wins / losses)


def max_drawdown(x: pd.Series) -> float:
    if x.empty:
        return 0.0
    curve = x.fillna(0).cumsum()
    return float((curve - curve.cummax()).min())


def summarize(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows = []
    for keys, g in df.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        net = pd.to_numeric(g["net_R"], errors="coerce").dropna()
        row = dict(zip(group_cols, keys))
        row.update(
            events=int(len(g)),
            executable=int((g["status"].astype(str).str.upper() == "PASS").sum()),
            trades=int(net.size),
            wins=int((net > 0).sum()),
            losses=int((net < 0).sum()),
            win_rate=float((net > 0).mean()) if len(net) else None,
            expectancy_R=float(net.mean()) if len(net) else None,
            profit_factor=profit_factor(net),
            total_net_R=float(net.sum()) if len(net) else 0.0,
            max_drawdown_R=max_drawdown(net),
            median_MFE_R=float(pd.to_numeric(g.get("MFE_R"), errors="coerce").median()) if "MFE_R" in g else None,
            median_MAE_R=float(pd.to_numeric(g.get("MAE_R"), errors="coerce").median()) if "MAE_R" in g else None,
        )
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("EDGE_DISCOVERY/out"))
    ap.add_argument("--allow-2025", action="store_true", help="Only for explicit evaluation; never use for calibration.")
    args = ap.parse_args()

    df = pd.read_csv(args.input_csv)
    missing = sorted(REQUIRED - set(df.columns))
    if missing:
        raise SystemExit(f"FAIL_CLOSED missing required columns: {missing}")

    df["event_time"] = pd.to_datetime(df["event_time"], utc=True, errors="coerce")
    if df["event_time"].isna().any():
        raise SystemExit("FAIL_CLOSED invalid event_time values")

    years = set(df["event_time"].dt.year.astype(int))
    if not args.allow_2025 and 2025 in years:
        raise SystemExit("FAIL_CLOSED: 2025 rows detected in calibration input")
    bad_future = sorted(y for y in years if y > 2024)
    if bad_future and not args.allow_2025:
        raise SystemExit(f"FAIL_CLOSED future years detected: {bad_future}")

    df = df[df["event_time"].dt.year.between(2016, 2024)].copy()
    if "net_R" not in df.columns:
        raise SystemExit("FAIL_CLOSED: input must contain frozen execution net_R; do not infer returns here")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    per_rule = summarize(df, ["rule_id"])
    per_year = summarize(df, ["rule_id", df["event_time"].dt.year.rename("year")])

    per_rule.to_csv(args.out_dir / "edge_ledger_by_rule_2016_2024.csv", index=False)
    per_year.to_csv(args.out_dir / "edge_ledger_by_rule_year_2016_2024.csv", index=False)

    manifest = {
        "window": "2016-2024",
        "input": str(args.input_csv),
        "rows": int(len(df)),
        "rule_ids": sorted(df["rule_id"].dropna().astype(str).unique().tolist()),
        "rule_count": int(df["rule_id"].nunique()),
        "contains_2025": False,
        "direction_generated": False,
        "returns_inferred": False,
        "status": "ANALYTICAL_ONLY",
    }
    (args.out_dir / "edge_ledger_manifest_2016_2024.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
