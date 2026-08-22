"""Fail-closed boundary for source-derived Historical Context Memory.

The memory layer is evidence only. It cannot generate direction, trade commands,
or tuning parameters. 2025 is locked OOS and is never accepted by this boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

LOCKED_OOS_YEAR = 2025
MAX_SUPPORTED_YEAR = 2024

@dataclass(frozen=True)
class HistoricalContextResult:
    status: str
    record: Mapping[str, Any]
    reason: Optional[str] = None


def _parse_year(timestamp: Any) -> Optional[int]:
    if isinstance(timestamp, datetime):
        return timestamp.year
    if isinstance(timestamp, str):
        text = timestamp.strip().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(text).year
        except ValueError:
            try:
                return datetime.strptime(text[:10], "%Y-%m-%d").year
            except ValueError:
                return None
    return None


def validate_historical_context(
    *,
    timestamp: Any,
    symbol: str,
    timeframe: str,
    context: Mapping[str, Any],
    provenance: Optional[Mapping[str, Any]] = None,
) -> HistoricalContextResult:
    year = _parse_year(timestamp)
    if year is None:
        return HistoricalContextResult("NOT_EVALUABLE", {}, "INVALID_TIMESTAMP")
    if year == LOCKED_OOS_YEAR:
        return HistoricalContextResult("NOT_EVALUABLE", {}, "2025_OOS_LOCKED")
    if year > LOCKED_OOS_YEAR:
        return HistoricalContextResult("NOT_EVALUABLE", {}, "FUTURE_DATA_FORBIDDEN")
    if year > MAX_SUPPORTED_YEAR:
        return HistoricalContextResult("NOT_EVALUABLE", {}, "UNSUPPORTED_DEVELOPMENT_WINDOW")
    if not symbol or not timeframe or not isinstance(context, Mapping):
        return HistoricalContextResult("NOT_EVALUABLE", {}, "MISSING_CONTEXT_IDENTITY")

    record = {
        "timestamp": timestamp,
        "symbol": symbol,
        "timeframe": timeframe,
        "context": dict(context),
        "provenance": dict(provenance or {}),
        "not_a_strategy": True,
        "direction": None,
        "final_trade_decision": None,
    }
    return HistoricalContextResult("PASS", record)
