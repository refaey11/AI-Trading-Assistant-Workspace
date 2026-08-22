"""Contract-bound adapter for existing Market Scenario Engine outputs.

No scenario thresholds or trade logic are invented here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

REQUIRED_FIELDS = {
    "pair",
    "primary_scenario",
    "decision",
    "confidence",
    "bullish_score",
    "bearish_score",
    "neutral_score",
}

ALLOWED_SCENARIOS = {"BULLISH", "BEARISH", "NEUTRAL / TWO-SIDED"}
ALLOWED_DECISIONS = {"WAIT", "BIAS"}


@dataclass(frozen=True)
class ScenarioResult:
    status: str
    scenario: Mapping[str, Any]
    final_trade_decision: Optional[str] = None


def normalize_scenario(row: Mapping[str, Any]) -> ScenarioResult:
    if any(field not in row for field in REQUIRED_FIELDS):
        return ScenarioResult("NOT_EVALUABLE", {})

    scenario_name = row.get("primary_scenario")
    if scenario_name not in ALLOWED_SCENARIOS:
        return ScenarioResult("NOT_EVALUABLE", {})

    decision = row.get("decision")
    if decision not in ALLOWED_DECISIONS:
        return ScenarioResult("NOT_EVALUABLE", {})

    try:
        confidence = float(row["confidence"])
        bullish = float(row["bullish_score"])
        bearish = float(row["bearish_score"])
        neutral = float(row["neutral_score"])
    except (TypeError, ValueError):
        return ScenarioResult("NOT_EVALUABLE", {})

    if min(confidence, bullish, bearish, neutral) < 0:
        return ScenarioResult("NOT_EVALUABLE", {})

    scenario = {
        "pair": row["pair"],
        "primary_scenario": scenario_name,
        "decision": decision,
        "confidence": confidence,
        "bullish_score": bullish,
        "bearish_score": bearish,
        "neutral_score": neutral,
        "supporting_evidence": row.get("supporting_evidence", []),
        "contradictions": row.get("contradictions", []),
        "required_confirmation": row.get("required_confirmation", []),
    }

    return ScenarioResult("PASS", scenario)
