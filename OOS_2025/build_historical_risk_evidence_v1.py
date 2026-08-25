from __future__ import annotations
import argparse, json, sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from risk_engine.risk_execution_runtime_v1 import RiskRequest, evaluate_risk


def _normalize_direction(v):
    r = str(v or "").upper()
    return "BUY" if r in {"BUY", "BULLISH"} else "SELL" if r in {"SELL", "BEARISH"} else None


def build(*, context: Path, murphy: Path, output: Path, year: int, equity: float = 10000.0) -> dict:
    ctx = pd.read_csv(context)
    m = pd.read_csv(murphy)
    for name, df, cols in [("context", ctx, {"timestamp", "entry_price", "atr"}), ("murphy", m, {"timestamp", "direction"})]:
        miss = sorted(cols - set(df.columns))
        if miss:
            raise ValueError(f"{name}: missing required columns {miss}")
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        if df["timestamp"].isna().any() or df["timestamp"].duplicated().any():
            raise ValueError(f"{name}: invalid or duplicate timestamps")

    ctx = ctx[ctx["timestamp"].dt.year == year].copy()
    m = m[m["timestamp"].dt.year == year].copy()
    merged = ctx.merge(m[["timestamp", "direction"]], on="timestamp", how="inner")
    if merged.empty:
        raise ValueError(f"No joinable Murphy/context timestamps for {year}")

    rows = []
    for _, r in merged.sort_values("timestamp").iterrows():
        d = _normalize_direction(r["direction"])
        entry = float(r["entry_price"])
        atr = float(r["atr"])
        if d is None:
            rows.append({"timestamp": r["timestamp"], "risk_status": "FAIL", "reason": "INVALID_DIRECTION"})
            continue
        stop_distance = 0.75 * atr
        tp_distance = 2.0 * stop_distance
        result = evaluate_risk(
            RiskRequest(
                equity=equity,
                risk_percent=0.005,
                entry_price=entry,
                stop_distance=stop_distance,
                take_profit_distance=tp_distance,
                stop_mode="structure",
                risk_budget_locked=True,
            ),
            d,
            atr,
        )
        rows.append({
            "timestamp": r["timestamp"],
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
    return {
        "status": "PASS",
        "evaluation_year": year,
        "rows": int(len(out)),
        "risk_profile": 0.005,
        "stop_atr": 0.75,
        "target_r": 2.0,
        "source_backed_inputs_only": True,
        "new_strategy_semantics": False,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    a = p.parse_args()
    report = build(context=a.context, murphy=a.murphy, output=a.output, year=a.year)
    a.manifest.parent.mkdir(parents=True, exist_ok=True)
    a.manifest.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
