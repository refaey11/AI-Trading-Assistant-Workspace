from __future__ import annotations

"""Cheap post-run guard for decision -> risk -> execution integrity.

This is intentionally validation-only: it never creates trades and never
changes the Decision Brain. It prevents the previous zero-trade wiring bug
from being mistaken for a strategy result.
"""

import argparse
import json
from pathlib import Path

import pandas as pd


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--events", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    df = pd.read_csv(args.events)
    required = {"timestamp", "brain_bias", "risk_status", "trade_allowed", "2025_locked"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise SystemExit(f"EXECUTION_CONTRACT_FAIL missing={missing}")

    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if ts.isna().any() or (ts.dt.year == 2025).any():
        raise SystemExit("EXECUTION_CONTRACT_FAIL 2025_PRESENT_OR_INVALID_TIMESTAMP")

    allowed = df["trade_allowed"].astype(bool)
    risk_pass = df["risk_status"].astype(str).str.upper().eq("PASS")
    if (allowed & ~risk_pass).any():
        raise SystemExit("EXECUTION_CONTRACT_FAIL trade_allowed_without_risk_pass")

    result = {
        "status": "PASS",
        "events": int(len(df)),
        "trade_allowed_events": int(allowed.sum()),
        "risk_pass_events": int(risk_pass.sum()),
        "2025_present": False,
        "decision_to_risk_monotonic": True,
        "note": "Validation only; no trade/PnL inference is performed here.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
