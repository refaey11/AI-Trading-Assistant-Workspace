from __future__ import annotations

"""Isolated Strategy V1 research adapter.

This module does NOT change the Decision Brain, rules, risk contracts, OOS data,
or the canonical replay. It consumes an existing 2016-2024 decision-event CSV
and labels strategy evidence into research layers so the next ablation can be
measured without modifying runtime semantics.

Research layers:
  context      = HTF/MTF directional environment
  setup        = breakout/continuation/structure evidence
  confirmation = Nison/price-action evidence
  memory       = historical evidence label
  risk         = authoritative risk result
  decision     = canonical Brain decision result

The adapter is intentionally descriptive: it never creates BUY/SELL signals.
"""

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

WINDOW_START = pd.Timestamp("2016-01-01", tz="UTC")
WINDOW_END = pd.Timestamp("2025-01-01", tz="UTC")


def _norm(v: Any) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ""
    return str(v).strip().upper()


def classify_context(row: pd.Series) -> str:
    vals = [_norm(row.get(k)) for k in ("H4_trend_regime", "D1_trend_regime", "mtf_trend_regime")]
    if any("BULL" in v or "UP" == v or "UPTREND" in v for v in vals):
        bull = True
    else:
        bull = False
    if any("BEAR" in v or "DOWN" == v or "DOWNTREND" in v for v in vals):
        bear = True
    else:
        bear = False
    if bull and not bear:
        return "BULLISH_CONTEXT"
    if bear and not bull:
        return "BEARISH_CONTEXT"
    if bull and bear:
        return "MIXED_CONTEXT"
    return "UNRESOLVED_CONTEXT"


def classify_confirmation(row: pd.Series) -> str:
    c = _norm(row.get("nison_confirmation"))
    contradiction = bool(row.get("nison_contradiction", False))
    if contradiction:
        return "CONTRADICT"
    if c in {"CONFIRMED", "WEAK", "ABSENT"}:
        return c
    return "UNKNOWN"


def classify_memory(row: pd.Series) -> str:
    for k in ("memory_status", "historical_memory_status", "historical_evidence_status"):
        v = _norm(row.get(k))
        if v in {"SUPPORT", "SUPPORTS", "SUPPORTED"}:
            return "SUPPORT"
        if v in {"CONTRADICT", "CONTRADICTS", "CONTRADICTION"}:
            return "CONTRADICT"
        if v in {"NEUTRAL"}:
            return "NEUTRAL"
        if v in {"INSUFFICIENT", "NOT_EVALUABLE", "NONE"}:
            return "INSUFFICIENT"
    return "UNRECORDED"


def classify_setup(row: pd.Series) -> str:
    candidates = []
    for k in ("structure_event", "setup_type", "scenario", "pattern", "market_scenario"):
        v = _norm(row.get(k))
        if v:
            candidates.append(v)
    text = " ".join(candidates)
    if "BREAKOUT" in text:
        return "BREAKOUT"
    if "CONTINUATION" in text or "PULLBACK" in text:
        return "CONTINUATION"
    if "COMPRESSION" in text or "RANGE" in text:
        return "COMPRESSION"
    return "UNCLASSIFIED"


def adapt(input_csv: Path, output_dir: Path) -> dict[str, Any]:
    df = pd.read_csv(input_csv)
    if "timestamp" not in df.columns:
        raise ValueError("Input event file must contain timestamp")
    ts = pd.to_datetime(df["timestamp"], utc=True, errors="raise", format="mixed")
    df = df.loc[(ts >= WINDOW_START) & (ts < WINDOW_END)].copy()
    df["timestamp"] = ts.loc[df.index]

    out = df.copy()
    out["research_context"] = out.apply(classify_context, axis=1)
    out["research_setup"] = out.apply(classify_setup, axis=1)
    out["research_confirmation"] = out.apply(classify_confirmation, axis=1)
    out["research_memory"] = out.apply(classify_memory, axis=1)
    out["strategy_eligible"] = (
        out.get("brain_final", "").astype(str).str.upper().isin(["BUY", "SELL"])
        | out.get("brain_status", "").astype(str).str.upper().isin(["EXECUTABLE"])
    )
    out["risk_allowed"] = out.get("risk_pass", False).astype(bool)
    out["future_data_used_research"] = False

    output_dir.mkdir(parents=True, exist_ok=True)
    event_path = output_dir / "strategy_v1_research_events_2016_2024.csv"
    out.to_csv(event_path, index=False)

    # Compact ablation-ready counts; no parameter tuning occurs here.
    ablation = {
        "window": "2016-2024",
        "future_data_used": False,
        "tuning_applied": False,
        "brain_semantics_changed": False,
        "rows": int(len(out)),
        "context_counts": out["research_context"].value_counts(dropna=False).to_dict(),
        "setup_counts": out["research_setup"].value_counts(dropna=False).to_dict(),
        "confirmation_counts": out["research_confirmation"].value_counts(dropna=False).to_dict(),
        "memory_counts": out["research_memory"].value_counts(dropna=False).to_dict(),
        "strategy_eligible_rows": int(out["strategy_eligible"].sum()),
        "risk_allowed_rows": int(out["risk_allowed"].sum()),
        "note": "Descriptive adapter only; does not generate direction or alter canonical risk/runtime semantics.",
    }
    (output_dir / "strategy_v1_ablation_manifest_2016_2024.json").write_text(json.dumps(ablation, indent=2, default=str), encoding="utf-8")
    return ablation


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(adapt(args.input, args.output_dir), indent=2, default=str))


if __name__ == "__main__":
    main()
