"""Contract-bound adapter for existing Market State Reader outputs.

This adapter does not recreate the Market State Reader or invent calculations.
It normalizes an existing source-derived state row to the frozen Market State
contract and fails closed when required evidence is missing.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

REQUIRED_FIELDS = {
    "timestamp", "close", "trend", "structure_event", "volume_state",
    "volatility_state", "location", "market_interpretation",
}

VALID_TRENDS = {"BULL_TREND", "BEAR_TREND", "TRANSITION", "UNKNOWN"}


@dataclass(frozen=True)
class MarketStateResult:
    status: str
    market_state: Mapping[str, Any]
    volume_evaluable: bool
    final_trade_decision: Optional[str] = None


def normalize_market_state(row: Mapping[str, Any]) -> MarketStateResult:
    """Normalize an existing source-derived state row without adding semantics."""
    if any(field not in row for field in REQUIRED_FIELDS):
        return MarketStateResult("NOT_EVALUABLE", {}, False)

    trend = row.get("trend")
    if trend not in VALID_TRENDS:
        return MarketStateResult("NOT_EVALUABLE", {}, False)

    volume = row.get("volume")
    volume_ratio = row.get("volume_ratio")
    volume_evaluable = bool(volume not in (None, 0, 0.0) and volume_ratio not in (None, 0, 0.0))

    state = {
        "timestamp": row["timestamp"],
        "close": row["close"],
        "trend": trend,
        "structure_event": row["structure_event"],
        "volume_state": row["volume_state"] if volume_evaluable else "UNKNOWN",
        "volatility_state": row["volatility_state"],
        "location": row["location"],
        "candlestick": {
            "bull_engulf": bool(row.get("bull_engulf", False)),
            "bear_engulf": bool(row.get("bear_engulf", False)),
            "hammer": bool(row.get("hammer", False)),
            "shooting_star": bool(row.get("shooting_star", False)),
        },
        "market_interpretation": row["market_interpretation"],
    }

    return MarketStateResult("PASS", state, volume_evaluable)
