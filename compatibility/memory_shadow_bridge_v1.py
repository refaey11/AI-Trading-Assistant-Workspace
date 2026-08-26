"""Shadow-only historical evidence bridge for the Decision Brain.

This bridge packages existing Historical Context, Historical Outcome, Similarity,
and Context-Aware Retrieval evidence without changing direction semantics.
It is intended for chronological development years before the locked 2025 OOS.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Mapping

LOCKED_OOS_YEAR = 2025
DEVELOPMENT_START_YEAR = 2016


def _year(value: Any) -> int | None:
    if isinstance(value, datetime):
        return value.year
    if isinstance(value, str):
        text = value.strip().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(text).year
        except ValueError:
            try:
                return datetime.strptime(text[:10], "%Y-%m-%d").year
            except ValueError:
                return None
    return None


def build_shadow_historical_evidence(
    *,
    query_as_of: Any,
    historical_context: Mapping[str, Any],
    historical_outcome: Mapping[str, Any],
    similarity: Mapping[str, Any],
    context_aware_retrieval: Mapping[str, Any] | None = None,
    murphy_direction: str | None = None,
) -> dict[str, Any]:
    year = _year(query_as_of)
    if year is None:
        return {"status": "NOT_EVALUABLE", "reason": "INVALID_QUERY_TIMESTAMP"}
    if year < DEVELOPMENT_START_YEAR:
        return {"status": "NOT_EVALUABLE", "reason": "PRE_DEVELOPMENT_BOUND"}
    if year >= LOCKED_OOS_YEAR:
        return {"status": "NOT_EVALUABLE", "reason": "2025_OOS_LOCKED"}

    sources = {
        "historical_context": deepcopy(dict(historical_context)),
        "historical_outcome": deepcopy(dict(historical_outcome)),
        "similarity": deepcopy(dict(similarity)),
        "context_aware_retrieval": deepcopy(dict(context_aware_retrieval or {})),
    }

    all_timestamps = []
    for payload in sources.values():
        value = payload.get("evidence_time_range", {}) if isinstance(payload, Mapping) else {}
        latest = value.get("latest") if isinstance(value, Mapping) else None
        if latest:
            latest_year = _year(latest)
            if latest_year is not None and latest_year >= LOCKED_OOS_YEAR:
                return {"status": "NOT_EVALUABLE", "reason": "FUTURE_OR_OOS_EVIDENCE"}
            all_timestamps.append(latest)

    memory_direction = None
    conflict = "NO_MURPHY_REFERENCE"
    if murphy_direction is not None:
        conflict = "NEUTRAL"
        for payload in sources.values():
            candidate = str(payload.get("directional_bias") or payload.get("bias") or "").upper()
            if candidate in {"BUY", "SELL", "BULLISH", "BEARISH"}:
                if memory_direction is None:
                    memory_direction = candidate
                elif memory_direction != candidate:
                    conflict = "CONFLICT"
        if memory_direction and memory_direction == str(murphy_direction).upper():
            conflict = "SUPPORT"
        elif memory_direction:
            conflict = "CONTRADICT"

    package = {
        "query_as_of": query_as_of,
        "historical_context": sources["historical_context"],
        "historical_outcome": sources["historical_outcome"],
        "similarity": sources["similarity"],
        "context_aware_retrieval": sources["context_aware_retrieval"],
        "memory_role": "EVIDENCE_ONLY",
        "availability": {
            name: str(payload.get("status") or payload.get("retrieval_status") or "UNKNOWN")
            for name, payload in sources.items()
        },
        "consumption": {
            "attached_to_historical_evidence": True,
            "downstream_direction_changed": False,
        },
        "governance": {
            "direction": None,
            "final_trade_decision": None,
            "similarity_is_sole_decision_maker": False,
            "predicted_return_used_as_direction": False,
            "lookahead_violation": False,
            "2025_used_for_tuning": False,
        },
        "murphy_comparison": {
            "murphy_direction": murphy_direction,
            "memory_directional_hint": memory_direction,
            "relationship": conflict,
        },
        "evidence_latest_timestamps": all_timestamps,
    }
    return {"status": "PASS", "historical_evidence": package}
