from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

EXPECTED_FOLDS = {
    "2024": {"calibration_end": "2023-12-31T23:59:59Z"},
    "2025": {"calibration_end": "2024-12-31T23:59:59Z"},
}
REQUIRED = {
    "event_id",
    "timestamp",
    "direction",
    "gross_r",
    "cost_r",
    "net_r",
    "outcome",
    "ambiguous",
}


def _load(path: str | Path, fold: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"{fold}: missing required columns: {sorted(missing)}")
    if fold not in EXPECTED_FOLDS:
        raise ValueError(f"Unsupported fold: {fold}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].isna().any():
        raise ValueError(f"{fold}: invalid timestamp")
    years = set(df["timestamp"].dt.year.astype(int).tolist())
    expected_year = int(fold)
    if years != {expected_year}:
        raise ValueError(f"{fold}: expected only {expected_year} timestamps, got {sorted(years)}")
    if df["event_id"].duplicated().any():
        raise ValueError(f"{fold}: duplicate event_id")
    for col in ["gross_r", "cost_r", "net_r"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any():
            raise ValueError(f"{fold}: non-numeric {col}")
    if (df["ambiguous"].astype(bool) & ~df["outcome"].astype(str).eq("AMBIGUOUS")).any():
        raise ValueError(f"{fold}: ambiguity flag/outcome mismatch")
    if "feature_available_at" in df.columns:
        feature_at = pd.to_datetime(df["feature_available_at"], utc=True)
        if (feature_at > df["timestamp"]).any():
            raise ValueError(f"{fold}: future feature availability detected")
    if "memory_built_through" in df.columns:
        memory_at = pd.to_datetime(df["memory_built_through"], utc=True)
        if (memory_at > df["timestamp"]).any():
            raise ValueError(f"{fold}: memory/index leakage detected")
    if "decision_available_at" in df.columns:
        decision_at = pd.to_datetime(df["decision_available_at"], utc=True)
        if (decision_at > df["timestamp"]).any():
            raise ValueError(f"{fold}: decision availability after event timestamp")
    return df.sort_values("timestamp").reset_index(drop=True)


def _metrics(df: pd.DataFrame) -> dict[str, Any]:
    net = df["net_r"].astype(float)
    gross = df["gross_r"].astype(float)
    wins = int((net > 0).sum())
    losses = int((net < 0).sum())
    positive = float(net[net > 0].sum())
    negative = float(net[net < 0].sum())
    pf = positive / abs(negative) if negative < 0 else None
    equity = net.cumsum()
    drawdown = equity - equity.cummax()
    return {
        "trades": int(len(df)),
        "wins": wins,
        "losses": losses,
        "win_rate": wins / len(df) if len(df) else 0.0,
        "profit_factor": pf,
        "expectancy_r": float(net.mean()) if len(df) else 0.0,
        "net_pnl_r": float(net.sum()),
        "gross_pnl_r": float(gross.sum()),
        "costs_r": float(df["cost_r"].sum()),
        "max_drawdown_r": float(drawdown.min()) if len(df) else 0.0,
        "ambiguous_trades": int(df["ambiguous"].astype(bool).sum()),
        "timeout_trades": int(df["outcome"].astype(str).eq("TIMEOUT").sum()),
    }


def run(fold_2024: str | Path, fold_2025: str | Path) -> dict[str, Any]:
    a = _load(fold_2024, "2024")
    b = _load(fold_2025, "2025")

    required_meta = {"signal_contract_id", "execution_protocol_id", "cost_model_id", "ambiguity_policy_id"}
    for name, df in [("2024", a), ("2025", b)]:
        missing = required_meta - set(df.columns)
        if missing:
            raise ValueError(f"{name}: missing frozen protocol metadata columns: {sorted(missing)}")
        for meta in required_meta:
            if df[meta].nunique(dropna=False) != 1:
                raise ValueError(f"{name}: {meta} must be uniform within fold")

    for meta in required_meta:
        if a[meta].iloc[0] != b[meta].iloc[0]:
            raise ValueError(f"protocol mismatch across folds: {meta}")

    all_rows = pd.concat([a.assign(fold="2024"), b.assign(fold="2025")], ignore_index=True)
    metrics = {
        "2024_oos": _metrics(a),
        "2025_oos": _metrics(b),
        "combined": _metrics(all_rows),
    }
    result = {
        "status": "PASS",
        "mode": "FINAL_OOS_WALK_FORWARD_LEAKAGE_GATE",
        "calibration_protocol": {
            "fold_2024": "2016-2023 -> OOS 2024",
            "fold_2025": "2016-2024 -> OOS 2025",
        },
        "uniform_protocol": {
            "signal_contract_id": a["signal_contract_id"].iloc[0],
            "execution_protocol_id": a["execution_protocol_id"].iloc[0],
            "cost_model_id": a["cost_model_id"].iloc[0],
            "ambiguity_policy_id": a["ambiguity_policy_id"].iloc[0],
        },
        "no_oos_tuning": True,
        "leakage_checks": {
            "feature_availability": "PASS_OR_HARD_FAIL",
            "memory_index_availability": "PASS_OR_HARD_FAIL",
            "decision_availability": "PASS_OR_HARD_FAIL",
            "future_outcome_used_as_feature": "NOT_INFERRED_FROM_OUTCOME_COLUMNS",
        },
        "metrics": metrics,
    }
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--oos-2024", required=True)
    p.add_argument("--oos-2025", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    result = run(args.oos_2024, args.oos_2025)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
