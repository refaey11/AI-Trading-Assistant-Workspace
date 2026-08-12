"""Reproducible candidate-only run for Murphy 0006/0007.

Expected workspace root contains:
PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv
TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv
DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv

This runner does not implement PASS/FAIL or a successful-touch threshold.
The historical QA population is explicitly capped to candidate timestamps
between 2016-01-01 and 2024-12-31 inclusive. 2025+ observations are excluded.
"""
from pathlib import Path
import argparse
import pandas as pd

START = pd.Timestamp("2016-01-01")
END = pd.Timestamp("2024-12-31 23:59:59")


def run(root: Path, output: Path) -> pd.DataFrame:
    piv = pd.read_csv(root / "PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv")
    geo = pd.read_csv(root / "TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv")
    ohlc = pd.read_csv(root / "DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv")

    for df in (piv, geo, ohlc):
        for c in [x for x in df.columns if "timestamp" in x or x == "availability_timestamp"]:
            df[c] = pd.to_datetime(df[c])

    piv = piv.sort_values("pivot_timestamp")
    ohlc_idx = ohlc.set_index(ohlc["timestamp"].dt.normalize())
    rows = []

    for _, g in geo.iterrows():
        mapping = {("LOW", "UP"): ("MURPHY_0006", "UP"),
                   ("HIGH", "DOWN"): ("MURPHY_0007", "DOWN")}
        if (g.line_type, g.direction) not in mapping:
            continue
        rule_id, expected_reaction = mapping[(g.line_type, g.direction)]
        candidates = piv[(piv.pivot_type == g.line_type)
                         & (piv.pivot_timestamp > g.point_2_timestamp)
                         & (piv.availability_timestamp >= g.availability_timestamp)
                         & (piv.pivot_timestamp >= START)
                         & (piv.pivot_timestamp <= END)]
        if candidates.empty:
            continue
        c = candidates.iloc[0]
        line_price = float(g.point_1_price) + float(g.slope_price_per_second) * (
            c.pivot_timestamp - g.point_1_timestamp
        ).total_seconds()
        bar = ohlc_idx.loc[c.pivot_timestamp.normalize()] if c.pivot_timestamp.normalize() in ohlc_idx.index else None
        high = float(bar.high) if bar is not None else None
        low = float(bar.low) if bar is not None else None
        intersects = (low <= line_price <= high) if bar is not None else None

        opposite = "HIGH" if g.line_type == "LOW" else "LOW"
        reactions = piv[(piv.pivot_type == opposite)
                        & (piv.pivot_timestamp > c.pivot_timestamp)
                        & (piv.availability_timestamp >= c.availability_timestamp)
                        & (piv.pivot_timestamp >= START)
                        & (piv.pivot_timestamp <= END)]
        r = reactions.iloc[0] if not reactions.empty else None
        consistent = None if r is None else (
            r.pivot_price > c.pivot_price if expected_reaction == "UP"
            else r.pivot_price < c.pivot_price
        )
        rows.append({
            "rule_id": rule_id,
            "line_id": g.line_id,
            "line_type": g.line_type,
            "direction": g.direction,
            "anchor_1_timestamp": g.point_1_timestamp.date().isoformat(),
            "anchor_1_price": g.point_1_price,
            "anchor_2_timestamp": g.point_2_timestamp.date().isoformat(),
            "anchor_2_price": g.point_2_price,
            "line_availability_timestamp": g.availability_timestamp.date().isoformat(),
            "candidate_timestamp": c.pivot_timestamp.date().isoformat(),
            "candidate_pivot_type": c.pivot_type,
            "candidate_pivot_price": c.pivot_price,
            "line_price_at_candidate": line_price,
            "signed_distance": c.pivot_price - line_price,
            "absolute_distance": abs(c.pivot_price - line_price),
            "daily_high": high,
            "daily_low": low,
            "daily_range_intersects_line": intersects,
            "reaction_candidate_timestamp": None if r is None else r.pivot_timestamp.date().isoformat(),
            "reaction_candidate_type": None if r is None else r.pivot_type,
            "reaction_directionally_consistent": consistent,
            "no_break_observation": "OBSERVATION_ONLY",
            "evidence_status": "CANDIDATE_ONLY",
        })

    result = pd.DataFrame(rows)
    if not result.empty:
        result = result[(pd.to_datetime(result["candidate_timestamp"]) >= START)
                        & (pd.to_datetime(result["candidate_timestamp"]) <= END)].copy()
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    df = run(args.workspace_root, args.output)
    print(df.groupby("rule_id").agg(
        candidate_lines=("rule_id", "size"),
        daily_range_intersections=("daily_range_intersects_line", "sum"),
        reaction_candidates=("reaction_candidate_timestamp", lambda s: s.notna().sum()),
        reaction_directionally_consistent=("reaction_directionally_consistent", lambda s: (s == True).sum()),
        exact_zero_distance=("absolute_distance", lambda s: (s == 0).sum()),
    ).to_string())
