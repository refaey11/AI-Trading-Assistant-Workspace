"""Fail-closed boundary for source-derived Historical Outcome Memory.

Historical Outcome Memory is descriptive evidence only. This boundary does not
classify outcomes into BULL/BASE/BEAR, does not derive direction, and does not
turn positive_rate or forward returns into trade rules. 2025 is locked OOS.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

LOCKED_OOS_YEAR = 2025
MAX_SUPPORTED_YEAR = 2024
REQUIRED_STATS = {
    "occurrences",
    "median_return_6h",
    "mean_return_6h",
    "positive_rate_6h",
    "median_return_12h",
    "mean_return_12h",
    "positive_rate_12h",
    "median_return_24h",
    "mean_return_24h",
    "positive_rate_24h",
    "median_return_48h",
    "mean_return_48h",
    "positive_rate_48h",
}

@dataclass(frozen=True)
class HistoricalOutcomeResult:
    status: str
    evidence: Mapping[str, Any]
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


def validate_historical_outcome(
    *,
    timestamp: Any,
    pair: str,
    context_signature: str,
    stats: Mapping[str, Any],
    provenance: Optional[Mapping[str, Any]] = None,
) -> HistoricalOutcomeResult:
    year = _parse_year(timestamp)
    if year is None:
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "INVALID_TIMESTAMP")
    if year == LOCKED_OOS_YEAR:
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "2025_OOS_LOCKED")
    if year > LOCKED_OOS_YEAR:
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "FUTURE_DATA_FORBIDDEN")
    if year > MAX_SUPPORTED_YEAR:
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "UNSUPPORTED_DEVELOPMENT_WINDOW")
    if not pair or not context_signature or not isinstance(stats, Mapping):
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "MISSING_OUTCOME_IDENTITY")
    if not REQUIRED_STATS.issubset(stats):
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "MISSING_OUTCOME_STATS")

    try:
        occurrences = int(stats["occurrences"])
        numeric = {k: float(stats[k]) for k in REQUIRED_STATS if k != "occurrences"}
    except (TypeError, ValueError):
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "INVALID_OUTCOME_STATS")

    if occurrences < 0:
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "INVALID_OCCURRENCE_COUNT")
    if any(not (-1.0 <= v <= 1.0) for k, v in numeric.items() if "positive_rate" in k):
        return HistoricalOutcomeResult("NOT_EVALUABLE", {}, "INVALID_POSITIVE_RATE")

    evidence = {
        "timestamp": timestamp,
        "pair": pair,
        "context_signature": context_signature,
        "stats": {"occurrences": occurrences, **numeric},
        "provenance": dict(provenance or {}),
        "not_a_strategy": True,
        "direction": None,
        "final_trade_decision": None,
        "scenario_classification": None,
    }
    return HistoricalOutcomeResult("PASS", evidence)
