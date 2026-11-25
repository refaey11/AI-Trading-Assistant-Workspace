from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BRAIN_PATH = ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py"


def load_csv(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df.timestamp.isna().any():
        raise ValueError(f"{path}: invalid timestamp")
    return df.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)


def norm(v: Any) -> str:
    t = str(v or "").strip().upper()
    return {"BUY": "BULLISH", "BULL": "BULLISH", "BULLISH": "BULLISH", "SELL": "BEARISH", "BEAR": "BEARISH", "BEARISH": "BEARISH"}.get(t, t)


def event_direction(r: pd.Series) -> str | None:
    """Direction is executable only when Murphy, Nison and Brain agree."""
    m, n, b = norm(r.get("murphy_direction")), norm(r.get("nison_confirmation")), norm(r.get("brain_bias"))
    if m not in {"BULLISH", "BEARISH"} or n != m or b != m:
        return None
    return "BUY" if m == "BULLISH" else "SELL"


def simulate(bars: pd.DataFrame, entry_idx: int, side: str, entry: float, atr: float, rr: float, atr_mult: float, max_bars: int) -> dict[str, Any]:
    if atr <= 0:
        return {"outcome": "REJECTED_BAD_ATR"}
    risk = atr * atr_mult
    sl = entry - risk if side == "BUY" else entry + risk
    tp = entry + risk * rr if side == "BUY" else entry - risk * rr
    last = min(len(bars), entry_idx + 1 + max_bars)
    for j in range(entry_idx + 1, last):
        b = bars.iloc[j]
        hit_sl = float(b.low) <= sl if side == "BUY" else float(b.high) >= sl
        hit_tp = float(b.high) >= tp if side == "BUY" else float(b.low) <= tp
        if hit_sl and hit_tp:
            return {"outcome": "AMBIGUOUS", "r_multiple": None, "exit_timestamp": b.timestamp, "stop_loss": sl, "take_profit": tp}
        if hit_tp:
            return {"outcome": "TP", "r_multiple": rr, "exit_timestamp": b.timestamp, "stop_loss": sl, "take_profit": tp}
        if hit_sl:
            return {"outcome": "SL", "r_multiple": -1.0, "exit_timestamp": b.timestamp, "stop_loss": sl, "take_profit": tp}
    return {"outcome": "TIME_EXIT", "r_multiple": None, "exit_timestamp": bars.iloc[last - 1].timestamp if last > entry_idx + 1 else None, "stop_loss": sl, "take_profit": tp}


def run(bars_path: Path, events_path: Path, out_dir: Path, pair: str, rr: float = 2.0, atr_mult: float = 0.75, max_bars: int = 48) -> dict[str, Any]:
    bars = load_csv(bars_path, {"timestamp", "open", "high", "low", "close"})
    events = load_csv(events_path, {"timestamp", "murphy_direction", "nison_confirmation", "brain_bias", "entry_price", "atr"})
    events = events[(events.timestamp.dt.year == 2025)].copy()
    if events.empty:
        raise ValueError("No 2025 events supplied")

    bar_pos = pd.Series(bars.index, index=bars.timestamp)
    rows: list[dict[str, Any]] = []
    trades: list[dict[str, Any]] = []
    for _, r in events.iterrows():
        side = event_direction(r)
        base = {"pair": pair, "signal_timestamp": r.timestamp, "murphy_direction": r.murphy_direction, "nison_confirmation": r.nison_confirmation, "brain_bias": r.brain_bias, "entry_price": r.entry_price, "atr": r.atr, "decision": side or "NO_TRADE"}
        if side is None:
            base["reason"] = "DIRECTION_NOT_ALIGNED"
            rows.append(base)
            continue
        matches = bars.index[bars.timestamp == r.timestamp]
        if len(matches) == 0:
            base["decision"] = "NO_TRADE"
            base["reason"] = "NO_MATCHING_BAR"
            rows.append(base)
            continue
        i = int(matches[0])
        if i + 1 >= len(bars):
            base["decision"] = "NO_TRADE"
            base["reason"] = "NO_NEXT_BAR"
            rows.append(base)
            continue
        # Execute at the next H1 open: the signal candle cannot be traded with hindsight.
        entry = float(bars.iloc[i + 1].open)
        result = simulate(bars, i + 1, side, entry, float(r.atr), rr, atr_mult, max_bars)
        trade = {**base, "entry_timestamp": bars.iloc[i + 1].timestamp, "entry_price_actual": entry, **result}
        trades.append(trade)
        rows.append(trade)

    out_dir.mkdir(parents=True, exist_ok=True)
    decisions = pd.DataFrame(rows)
    trades_df = pd.DataFrame(trades)
    decisions.to_csv(out_dir / "decision_events_2025.csv", index=False)
    trades_df.to_csv(out_dir / "paper_trades_2025.csv", index=False)
    valid = trades_df[trades_df.r_multiple.notna()] if not trades_df.empty else trades_df
    wins = int((valid.r_multiple > 0).sum()) if not valid.empty else 0
    losses = int((valid.r_multiple < 0).sum()) if not valid.empty else 0
    gross_win = float(valid.loc[valid.r_multiple > 0, "r_multiple"].sum()) if not valid.empty else 0.0
    gross_loss = float(-valid.loc[valid.r_multiple < 0, "r_multiple"].sum()) if not valid.empty else 0.0
    equity = valid.r_multiple.cumsum() if not valid.empty else pd.Series(dtype=float)
    metrics = {
        "pair": pair, "window": "2025-only", "signals": int(len(events)), "decisions": int(len(decisions)),
        "executed": int(len(trades_df)), "resolved": int(len(valid)), "wins": wins, "losses": losses,
        "win_rate": wins / len(valid) if len(valid) else None,
        "profit_factor": gross_win / gross_loss if gross_loss else None,
        "expectancy_R": float(valid.r_multiple.mean()) if len(valid) else None,
        "total_R": float(valid.r_multiple.sum()) if len(valid) else 0.0,
        "max_drawdown_R": float((equity - equity.cummax()).min()) if not equity.empty else 0.0,
        "rr": rr, "atr_stop_multiple": atr_mult, "max_bars": max_bars,
        "future_data_used": False, "tuning_applied": False, "live_execution": False,
        "official_profitability_claim": False,
    }
    Path(out_dir / "metrics_2025.json").write_text(json.dumps(metrics, indent=2, default=str), encoding="utf-8")
    Path(out_dir / "governance_2025.json").write_text(json.dumps({"window": "2025-only", "oos": True, "tuning": False, "lookahead_entry": False, "live_execution": False, "official_profitability_claim": False}, indent=2), encoding="utf-8")
    return metrics


def main() -> int:
    p = argparse.ArgumentParser(description="Deterministic paper-trading runner over existing Decision Brain evidence.")
    p.add_argument("--bars", type=Path, required=True)
    p.add_argument("--events", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--pair", required=True)
    p.add_argument("--rr", type=float, default=2.0)
    p.add_argument("--atr-stop", type=float, default=0.75)
    p.add_argument("--max-bars", type=int, default=48)
    a = p.parse_args()
    print(json.dumps(run(a.bars, a.events, a.out_dir, a.pair, a.rr, a.atr_stop, a.max_bars), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
