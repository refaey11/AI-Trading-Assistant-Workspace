"""Contract-bound adapter for existing Market Scenario Engine outputs.

Normalizes source-derived scenario output only. It does not recompute scores,
invent thresholds, create entry logic, or generate a final trade decision.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

REQUIRED_MARKET_STATE = {
    "pair", "timestamp", "close", "trend", "structure", "volume",
    "volatility", "location", "interpretation",
}
REQUIRED_SCENARIO = {
    "scores", "primary_scenario", "decision", "confidence",
    "bullish_evidence", "bearish_evidence",
    "bullish_invalidation", "bearish_invalidation", "required_confirmation",
}


@dataclass(frozen=True)
class ScenarioResult:
    status: str
    scenario: Mapping[str, Any]
    final_trade_decision: None = None


def normalize_scenario(source: Mapping[str, Any]) -> ScenarioResult:
    """Normalize an existing source-derived scenario without adding semantics."""
    market_state = source.get("market_state")
    scenario = source.get("scenario_analysis")
    if not isinstance(market_state, Mapping) or not isinstance(scenario, Mapping):
        return ScenarioResult("NOT_EVALUABLE", {})
    if not REQUIRED_MARKET_STATE.issubset(market_state.keys()):
        return ScenarioResult("NOT_EVALUABLE", {})
    if not REQUIRED_SCENARIO.issubset(scenario.keys()):
        return ScenarioResult("NOT_EVALUABLE", {})

    normalized = {
        "pair": market_state["pair"],
        "timestamp": market_state["timestamp"],
        "oos_status": "OOS_2025_READ_ONLY" if str(market_state["timestamp"]).startswith("2025") else "NON_2025",
        "primary_scenario": scenario["primary_scenario"],
        "source_decision": scenario["decision"],
        "confidence": scenario["confidence"],
        "scores": scenario["scores"],
        "bullish_evidence": scenario["bullish_evidence"],
        "bearish_evidence": scenario["bearish_evidence"],
        "bullish_invalidation": scenario["bullish_invalidation"],
        "bearish_invalidation": scenario["bearish_invalidation"],
        "required_confirmation": scenario["required_confirmation"],
        "final_trade_decision": None,
        "execution_fields_generated": False,
    }
    return ScenarioResult("PASS", normalized)
