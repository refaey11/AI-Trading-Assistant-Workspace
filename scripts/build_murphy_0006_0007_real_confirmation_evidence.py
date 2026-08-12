"""Build candidate-only Murphy 0006/0007 confirmation evidence from canonical D1 files.

Inputs are the existing Trendline Geometry V1 CSV and D1 OHLC evidence CSV.
The third-pivot candidate is derived from consecutive same-type Geometry V1
lines: the next line's point-2 is the next confirmed same-type pivot.

This script emits observations only. It does not implement a successful-touch,
reaction, or no-break PASS/FAIL rule.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import pandas as pd


def line_price(row: pd.Series, ts: pd.Timestamp) -> float:
    t1 = pd.Timestamp(row.point_1_timestamp)
    t2 = pd.Timestamp(row.point_2_timestamp)
    tx = pd.Timestamp(ts)
    dt = (t2 - t1).total_seconds()
    if dt == 0:
        raise ValueError("geometry anchor timestamps must differ")
    return float(row.point_1_price) + (
        float(row.point_2_price) - float(row.point_1_price)
    ) * ((tx - t1).total_seconds() / dt)


def build(geometry_csv: Path, ohlc_csv: Path) -> pd.DataFrame:
    geom = pd.read_csv(
        geometry_csv,
        parse_dates=[
            "point_1_timestamp",
            "point_2_timestamp",
            "availability_timestamp",
        ],
    )
    ohlc = pd.read_csv(ohlc_csv, parse_dates=["timestamp"]).set_index("timestamp").sort_index()
    geom = geom.sort_values(["line_type", "point_1_timestamp", "point_2_timestamp"]).reset_index(drop=True)

    nodes = []
    for _, row in geom.iterrows():
        nodes.append((pd.Timestamp(row.point_2_timestamp), row.line_type, float(row.point_2_price)))
    node_df = (
        pd.DataFrame(nodes, columns=["ts", "ptype", "price"])
        .drop_duplicates(["ts", "ptype"])
        .sort_values("ts")
    )

    out = []
    for line_type, group in geom.groupby("line_type", sort=False):
        group = group.sort_values("point_1_timestamp").reset_index(drop=False)
        for i in range(len(group) - 1):
            a = group.iloc[i]
            b = group.iloc[i + 1]
            if pd.Timestamp(a.point_2_timestamp) != pd.Timestamp(b.point_1_timestamp):
                continue
            if line_type == "LOW" and a.direction == "UP":
                rule_id, opposite = "MURPHY_0006", "HIGH"
            elif line_type == "HIGH" and a.direction == "DOWN":
                rule_id, opposite = "MURPHY_0007", "LOW"
            else:
                continue

            candidate_ts = pd.Timestamp(b.point_2_timestamp)
            if candidate_ts not in ohlc.index:
                continue
            candidate_price = float(b.point_2_price)
            candidate_line = line_price(a, candidate_ts)
            bar = ohlc.loc[candidate_ts]

            future = node_df[(node_df.ts > candidate_ts) & (node_df.ptype == opposite)]
            reaction_ts: Optional[pd.Timestamp] = None
            reaction_price: Optional[float] = None
            reaction_consistent: Optional[bool] = None
            if not future.empty:
                reaction_ts = pd.Timestamp(future.iloc[0].ts)
                reaction_price = float(future.iloc[0].price)
                reaction_line = line_price(a, reaction_ts)
                reaction_consistent = (
                    reaction_price > reaction_line if rule_id == "MURPHY_0006" else reaction_price < reaction_line
                )

            end = reaction_ts or candidate_ts
            window = ohlc.loc[(ohlc.index > candidate_ts) & (ohlc.index <= end)]
            close_above = close_below = range_intersection = 0
            for ts, r in window.iterrows():
                lp = line_price(a, ts)
                close = float(r.close)
                close_above += int(close > lp)
                close_below += int(close < lp)
                range_intersection += int(float(r.low) <= lp <= float(r.high))

            out.append({
                "rule_id": rule_id,
                "line_id": a.line_id,
                "line_type": a.line_type,
                "direction": a.direction,
                "anchor_1_timestamp": pd.Timestamp(a.point_1_timestamp).date().isoformat(),
                "anchor_1_price": float(a.point_1_price),
                "anchor_2_timestamp": pd.Timestamp(a.point_2_timestamp).date().isoformat(),
                "anchor_2_price": float(a.point_2_price),
                "line_availability_timestamp": pd.Timestamp(a.availability_timestamp).date().isoformat(),
                "candidate_timestamp": candidate_ts.date().isoformat(),
                "candidate_pivot_type": a.line_type,
                "candidate_pivot_price": candidate_price,
                "line_price_at_candidate": candidate_line,
                "signed_distance": candidate_price - candidate_line,
                "absolute_distance": abs(candidate_price - candidate_line),
                "daily_high": float(bar.high),
                "daily_low": float(bar.low),
                "daily_range_intersects_line": bool(float(bar.low) <= candidate_line <= float(bar.high)),
                "reaction_candidate_timestamp": reaction_ts.date().isoformat() if reaction_ts is not None else None,
                "reaction_candidate_type": opposite if reaction_ts is not None else None,
                "reaction_directionally_consistent": reaction_consistent,
                "raw_post_touch_close_above_line_bars": close_above,
                "raw_post_touch_close_below_line_bars": close_below,
                "raw_post_touch_range_intersection_bars": range_intersection,
                "no_break_observation": "RAW_ONLY",
                "evidence_status": "CANDIDATE_ONLY",
            })

    return pd.DataFrame(out).sort_values(["rule_id", "candidate_timestamp"]).reset_index(drop=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--geometry", required=True, type=Path)
    ap.add_argument("--ohlc", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    df = build(args.geometry, args.ohlc)
    if df.empty:
        raise SystemExit("No eligible Murphy 0006/0007 candidates produced.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(df.groupby("rule_id").size().to_dict())
    print({"rows": len(df), "status": sorted(df["evidence_status"].unique())})


if __name__ == "__main__":
    main()
