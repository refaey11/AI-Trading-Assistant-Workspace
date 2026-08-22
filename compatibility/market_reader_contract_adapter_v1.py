"""Contract-bound Market Reader adapter.

Normalizes existing source-derived market-state/evidence inputs into the
frozen Market Reader V1 output contract. It does not invent indicators,
thresholds, scenarios, or directional rules.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence

ALLOWED_DECISIONS = {"BUY BIAS", "SELL BIAS", "WAIT", "NO TRADE"}


@dataclass(frozen=True)
class MarketReaderResult:
    status: str
    output: Mapping[str, Any]
    final_trade_decision: Optional[str] = None


def normalize_market_reading(
    *,
    symbol: str,
    timeframe: str,
    market_state: Mapping[str, Any],
    locations: Sequence[Mapping[str, Any]] = (),
    evidence: Sequence[Mapping[str, Any]] = (),
    knowledge_matches: Sequence[Mapping[str, Any]] = (),
    contradictions: Sequence[Mapping[str, Any]] = (),
    scenarios: Sequence[Mapping[str, Any]] = (),
    interpretation: str = "",
    confidence: float = 0.0,
    decision: str = "WAIT",
    invalidation: str = "",
    risk_plan: Optional[Mapping[str, Any]] = None,
) -> MarketReaderResult:
    required_state = {"trend", "structure", "volatility", "volume"}
    if not symbol or not timeframe:
        return MarketReaderResult("NOT_EVALUABLE", {})
    if not required_state.issubset(market_state):
        return MarketReaderResult("NOT_EVALUABLE", {})
    if decision not in ALLOWED_DECISIONS:
        return MarketReaderResult("NOT_EVALUABLE", {})
    if not 0.0 <= float(confidence) <= 1.0:
        return MarketReaderResult("NOT_EVALUABLE", {})

    output = {
        "symbol": symbol,
        "timeframe": timeframe,
        "market_state": {
            "trend": market_state["trend"],
            "structure": market_state["structure"],
            "volatility": market_state["volatility"],
            "volume": market_state["volume"],
        },
        "locations": list(locations),
        "evidence": list(evidence),
        "knowledge_matches": list(knowledge_matches),
        "contradictions": list(contradictions),
        "scenarios": list(scenarios),
        "interpretation": interpretation,
        "confidence": float(confidence),
        "decision": decision,
        "invalidation": invalidation,
        "risk_plan": risk_plan,
    }
    return MarketReaderResult("PASS", output, None)
