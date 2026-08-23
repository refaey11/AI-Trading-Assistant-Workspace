from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from risk_engine.risk_execution_runtime_v1 import RiskRequest, evaluate_risk


def build(*, context: Path, murphy: Path, output: Path, year: int, equity: float = 10000.0) -> dict:
    ctx = pd.read_csv(context)
    murphy_df = pd.read_csv(murphy)
    for name, df, cols in [
        ("context", ctx, {"timestamp", "entry_price", "atr"}),
        ("murphy", murphy_df, {"timestamp", "direction"}),
    ]:
        missing = sorted(cols - set(df.columns))
        if missing:
            raise ValueError(f"{name}: missing required columns {missing}")
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        if df["timestamp"].isna().any():
            raise ValueError(f"{name}: invalid timestamps")
        if df["timestamp"].duplicated().any():
            raise ValueError(f"{name}: duplicate timestamps")

    ctx = ctx.loc[ctx["timestamp"].dt.year == year].copy()
    murphy_df = murphy_df.loc[murphy_df["timestamp"].dt.year == year].copy()
    merged = ctx.merge(murphy_df[["timestamp", "direction"]], on="timestamp", how="inner")
    if merged.empty:
        raise ValueError(f"No joinable Murphy/context timestamps for {year}")

    rows = []
    for _, row in merged.sort_values("timestamp").iterrows():
        direction = str(row["direction"]).upper()
        entry = float(row["entry_price"])
        atr = float(row["atr"])
        if direction not in {"BUY", "SELL"}:
            rows.append({"timestamp": row["timestamp"], "risk_status": "FAIL", "reason": "INVALID_DIRECTION"})
            continue
        stop_distance = 0.75 * atr
        take_profit_distance = 2.0 * stop_distance
        result = evaluate_risk(
            RiskRequest(
                equity=equity,
                risk_percent=0.005,
                entry_price=entry,
                stop_distance=stop_distance,
                take_profit_distance=take_profit_distance,
                stop_mode="structure",
                risk_budget_locked=True,
            ),
            direction,
            atr,
        )
        rows.append({
            "timestamp": row["timestamp"],
            "risk_status": "PASS" if result.risk_pass else "FAIL",
            "reason": result.reason,
            "stop_loss": result.stop_loss,
            "take_profit": result.take_profit,
            "risk_money": result.risk_money,
            "position_size": result.position_size,
        })

    out = pd.DataFrame(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    manifest = {
        "status": "PASS",
        "evaluation_year": year,
        "rows": int(len(out)),
        "risk_profile": 0.005,
        "stop_atr": 0.75,
        "target_r": 2.0,
        "source_backed_inputs_only": True,
        "new_strategy_semantics": False,
    }
    return manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    args = p.parse_args()
    report = build(context=args.context, murphy=args.murphy, output=args.output, year=args.year)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
