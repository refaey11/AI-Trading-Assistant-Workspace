from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from frozen_candidate_risk_profile_v1 import evaluate_frozen_candidate_risk


def read_csv(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp", kind="stable").reset_index(drop=True)


def choose_exit(h1: pd.DataFrame, start_index: int, direction: str, sl: float, tp: float) -> tuple[str, int, bool]:
    for j in range(start_index + 1, len(h1)):
        row = h1.iloc[j]
        high = float(row["high"])
        low = float(row["low"])
        if direction == "BUY":
            stop_hit = low <= sl
            tp_hit = high >= tp
        else:
            stop_hit = high >= sl
            tp_hit = low <= tp
        if stop_hit and tp_hit:
            return "AMBIGUOUS", j, True
        if stop_hit:
            return "LOSS", j, False
        if tp_hit:
            return "WIN", j, False
    return "OPEN", len(h1) - 1, False


def run(events_path: Path, h1_path: Path, out_dir: Path) -> dict:
    events = read_csv(
        events_path,
        {"timestamp", "status", "direction", "nison_contradiction", "entry_price", "atr"},
    )
    h1 = read_csv(h1_path, {"timestamp", "open", "high", "low", "close"})
    h1 = h1[h1["timestamp"].dt.year.eq(2025)].reset_index(drop=True)
    ts_to_idx = {ts: i for i, ts in enumerate(h1["timestamp"])}

    eligible = events[
        events["status"].astype(str).eq("EXECUTABLE")
        & events["direction"].astype(str).isin({"BUY", "SELL"})
        & (~events["nison_contradiction"].fillna(False).astype(bool))
    ].copy()

    # Track every executable opportunity independently. This is a signal-quality
    # diagnostic only: it ignores position overlap and account-level risk blocking.
    independent_records: list[dict] = []
    for row in eligible.to_dict("records"):
        ts = pd.Timestamp(row["timestamp"])
        idx = ts_to_idx.get(ts)
        entry = float(row["entry_price"])
        atr = float(row["atr"])
        if idx is None or atr <= 0:
            independent_records.append({"timestamp": ts, "status": "INVALID_INPUT"})
            continue
        direction = str(row["direction"])
        stop_distance = 0.75 * atr
        if direction == "BUY":
            sl = entry - stop_distance
            tp = entry + 2.0 * stop_distance
        else:
            sl = entry + stop_distance
            tp = entry - 2.0 * stop_distance
        outcome, exit_idx, ambiguous = choose_exit(h1, idx, direction, sl, tp)
        independent_records.append(
            {
                "timestamp": ts,
                "direction": direction,
                "status": outcome,
                "r_core": None if ambiguous or outcome in {"OPEN", "INVALID_INPUT"} else (2.0 if outcome == "WIN" else -1.0),
                "exit_timestamp": h1.iloc[exit_idx]["timestamp"] if exit_idx is not None else None,
            }
        )

    independent = pd.DataFrame(independent_records)
    valid = independent[independent["r_core"].notna()].copy() if not independent.empty else independent

    # Reproduce the current execution-constrained protocol, but label every
    # skipped opportunity so the 2691 -> 31 gap reconciles instead of disappearing.
    equity = 10_000.0
    peak = equity
    loss_streak = 0
    last_exit_idx = -1
    first_breaker_ts = None
    execution_records: list[dict] = []

    for row in eligible.to_dict("records"):
        ts = pd.Timestamp(row["timestamp"])
        idx = ts_to_idx.get(ts)
        if idx is None:
            execution_records.append({"timestamp": ts, "classification": "INVALID_INPUT"})
            continue
        if idx <= last_exit_idx:
            execution_records.append({"timestamp": ts, "classification": "OVERLAP_SKIPPED"})
            continue

        direction = str(row["direction"])
        entry = float(row["entry_price"])
        atr = float(row["atr"])
        risk = evaluate_frozen_candidate_risk(
            direction=direction,
            equity=equity,
            peak_equity=peak,
            entry=entry,
            atr=atr,
            prior_loss_streak=loss_streak,
        )
        if not risk.risk_pass:
            reason = risk.reason
            if reason == "DRAWDOWN_CIRCUIT_BREAKER" and first_breaker_ts is None:
                first_breaker_ts = ts
            execution_records.append({
                "timestamp": ts,
                "classification": "RISK_BLOCKED",
                "reason": reason,
            })
            continue

        outcome, exit_idx, ambiguous = choose_exit(
            h1, idx, direction, float(risk.stop_loss), float(risk.take_profit)
        )
        execution_records.append({
            "timestamp": ts,
            "classification": "EXECUTED_ATTEMPT",
            "outcome": outcome,
            "ambiguous": ambiguous,
        })

        if outcome == "OPEN":
            last_exit_idx = exit_idx
            continue

        r_core = None if ambiguous else (2.0 if outcome == "WIN" else -1.0)
        if r_core is not None:
            risk_money = equity * risk.risk_percent
            equity += risk_money * r_core
            peak = max(peak, equity)
            loss_streak = loss_streak + 1 if r_core < 0 else 0
        last_exit_idx = exit_idx

    execution = pd.DataFrame(execution_records)
    counts = execution["classification"].value_counts().to_dict() if not execution.empty else {}
    risk_reasons = (
        execution.loc[execution["classification"].eq("RISK_BLOCKED"), "reason"]
        .fillna("UNKNOWN")
        .value_counts()
        .to_dict()
        if not execution.empty
        else {}
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    independent.to_csv(out_dir / "SIGNAL_OPPORTUNITY_OUTCOMES_2025.csv", index=False)
    execution.to_csv(out_dir / "EXECUTION_CENSORING_CLASSIFICATION_2025.csv", index=False)

    total_r = float(valid["r_core"].sum()) if not valid.empty else 0.0
    wins = int((valid["r_core"] > 0).sum()) if not valid.empty else 0
    losses = int((valid["r_core"] < 0).sum()) if not valid.empty else 0

    after_breaker = 0
    if first_breaker_ts is not None:
        after_breaker = int((eligible["timestamp"] > first_breaker_ts).sum())

    result = {
        "status": "COMPLETED_EXECUTION_CENSORING_DIAGNOSTIC",
        "evaluation_year": 2025,
        "eligible_events": int(len(eligible)),
        "execution_classification_counts": {str(k): int(v) for k, v in counts.items()},
        "risk_block_reason_counts": {str(k): int(v) for k, v in risk_reasons.items()},
        "first_drawdown_breaker_timestamp": str(first_breaker_ts) if first_breaker_ts is not None else None,
        "eligible_events_after_first_breaker": after_breaker,
        "independent_signal_outcome": {
            "wins": wins,
            "losses": losses,
            "ambiguous": int((independent["status"] == "AMBIGUOUS").sum()) if not independent.empty else 0,
            "open": int((independent["status"] == "OPEN").sum()) if not independent.empty else 0,
            "total_core_R": total_r,
            "expectancy_R": (total_r / len(valid)) if len(valid) else 0.0,
            "profit_factor": ((wins * 2.0) / losses) if losses else None,
        },
        "governance": {
            "diagnostic_only": True,
            "does_not_modify_2025_rules": True,
            "does_not_promote_new_risk_rules": True,
            "independent_signal_mode_ignores_execution_censorship": True,
            "execution_mode_reproduces_current_frozen_candidate_protocol": True,
        },
    }
    (out_dir / "EXECUTION_CENSORING_DIAGNOSTIC_2025.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--h1", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    result = run(args.events, args.h1, args.output_dir)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
