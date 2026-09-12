#!/usr/bin/env python3
"""Opportunity Funnel V1: analytical discovery over an existing governed event stream.

This module does NOT create signals, alter rule semantics, or infer returns.
It converts already-produced evidence into a funnel and evaluates existing
categorical evidence combinations against frozen execution outcomes.
Calibration is 2016-2024 only; 2025 is rejected unless explicitly allowed.

Design goal: stop requiring every rule to be historically evaluable before
measuring whether the existing stack contains a useful subset of opportunities.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import math
import pandas as pd

BASE_REQUIRED = {"event_time", "direction", "status", "net_R"}
EVIDENCE_ALIASES = {
    "murphy": ["murphy_direction", "murphy_signal", "murphy_status", "rule_id"],
    "nison": ["nison_direction", "nison_confirmation", "nison_status"],
    "mtf": ["mtf_trend_regime", "mtf_trend_score", "mtf_alignment", "mtf_status"],
    "regime": ["market_regime", "regime", "market_state", "trend_regime"],
    "risk": ["risk_pass", "risk_status", "trade_allowed"],
}


def first_existing(df: pd.DataFrame, names: list[str]) -> str | None:
    return next((x for x in names if x in df.columns), None)


def pf(x: pd.Series) -> float | None:
    wins = float(x[x > 0].sum())
    losses = float(-x[x < 0].sum())
    if losses == 0:
        return math.inf if wins > 0 else None
    return wins / losses


def max_dd(x: pd.Series) -> float:
    if x.empty:
        return 0.0
    curve = x.cumsum()
    return float((curve - curve.cummax()).min())


def stats(g: pd.DataFrame) -> dict:
    r = pd.to_numeric(g["net_R"], errors="coerce").dropna()
    return {
        "events": int(len(g)),
        "trades": int(len(r)),
        "wins": int((r > 0).sum()),
        "losses": int((r < 0).sum()),
        "win_rate": float((r > 0).mean()) if len(r) else None,
        "expectancy_R": float(r.mean()) if len(r) else None,
        "profit_factor": pf(r),
        "total_net_R": float(r.sum()) if len(r) else 0.0,
        "max_drawdown_R": max_dd(r),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("EDGE_DISCOVERY/out"))
    ap.add_argument("--min-events", type=int, default=50)
    ap.add_argument("--allow-2025", action="store_true")
    args = ap.parse_args()

    df = pd.read_csv(args.input_csv)
    missing = sorted(BASE_REQUIRED - set(df.columns))
    if missing:
        raise SystemExit(f"FAIL_CLOSED missing required columns: {missing}")
    df["event_time"] = pd.to_datetime(df["event_time"], utc=True, errors="coerce")
    if df["event_time"].isna().any():
        raise SystemExit("FAIL_CLOSED invalid event_time")
    years = set(df["event_time"].dt.year.astype(int))
    if not args.allow_2025 and any(y >= 2025 for y in years):
        raise SystemExit("FAIL_CLOSED: 2025+ rows detected in calibration input")
    df = df[df["event_time"].dt.year.between(2016, 2024)].copy()

    cols: dict[str, str] = {}
    for key, aliases in EVIDENCE_ALIASES.items():
        col = first_existing(df, aliases)
        if col:
            cols[key] = col

    # Canonical execution funnel. We only classify fields already present.
    direction = df["direction"].astype(str).str.upper()
    status = df["status"].astype(str).str.upper()
    funnel = pd.DataFrame({
        "stage": [
            "events", "direction_available", "evidence_status_pass",
            "risk_pass", "trade_allowed", "realized_outcome"
        ],
        "count": [
            len(df),
            int(direction.isin(["BUY", "SELL", "BULLISH", "BEARISH"]).sum()),
            int(status.eq("PASS").sum()),
            int(df[cols["risk"]].astype(str).str.upper().isin(["TRUE", "PASS", "1"]).sum()) if "risk" in cols else 0,
            int(df[cols["risk"]].astype(str).str.upper().isin(["TRUE", "PASS", "1"]).sum()) if "risk" in cols else 0,
            int(pd.to_numeric(df["net_R"], errors="coerce").notna().sum()),
        ],
    })

    # Build a small, auditable discovery matrix from evidence already produced.
    candidate_dims = [x for x in ("murphy", "nison", "mtf", "regime") if x in cols]
    rows: list[dict] = []
    for dim in candidate_dims:
        c = cols[dim]
        temp = df.copy()
        temp["value"] = temp[c].astype(str).fillna("NA")
        for value, g in temp.groupby("value", dropna=False):
            if len(g) < args.min_events:
                continue
            row = {"dimensions": dim, "condition": f"{c}={value}", **stats(g)}
            rows.append(row)

    # Two-way combinations are deliberately limited to evidence dimensions,
    # not numeric parameter sweeps. This is discovery, not optimization.
    for i, a in enumerate(candidate_dims):
        for b in candidate_dims[i + 1:]:
            ca, cb = cols[a], cols[b]
            temp = df.copy()
            temp["_a"] = temp[ca].astype(str).fillna("NA")
            temp["_b"] = temp[cb].astype(str).fillna("NA")
            for (va, vb), g in temp.groupby(["_a", "_b"], dropna=False):
                if len(g) < args.min_events:
                    continue
                row = {"dimensions": f"{a}+{b}", "condition": f"{ca}={va} AND {cb}={vb}", **stats(g)}
                rows.append(row)

    result = pd.DataFrame(rows)
    if not result.empty:
        result = result.sort_values(["expectancy_R", "profit_factor", "trades"], ascending=[False, False, False])

    args.out_dir.mkdir(parents=True, exist_ok=True)
    funnel.to_csv(args.out_dir / "opportunity_funnel_2016_2024.csv", index=False)
    result.to_csv(args.out_dir / "opportunity_discovery_matrix_2016_2024.csv", index=False)

    manifest = {
        "window": "2016-2024",
        "rows": int(len(df)),
        "evidence_columns_used": cols,
        "candidate_dimensions": candidate_dims,
        "min_events": args.min_events,
        "direction_generated": False,
        "returns_inferred": False,
        "parameter_optimization": False,
        "contains_2025": False,
        "status": "ANALYTICAL_DISCOVERY_ONLY",
    }
    (args.out_dir / "opportunity_funnel_manifest_2016_2024.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
