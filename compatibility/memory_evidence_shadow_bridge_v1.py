"""Shadow-only bridge for existing historical-memory subsystems.

This module does not rebuild memory systems and does not change Decision Brain
semantics. It packages already-derived evidence from the existing historical
memory sources for 2016-2024 development validation, while explicitly recording
availability, candidate counts, lookahead flags, and evidence-only invariants.
2025 remains locked and cannot be used for development/tuning.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

LOCKED_OOS_YEAR = 2025
MAX_DEVELOPMENT_YEAR = 2024

MEMORY_KEYS = (
    "historical_context",
    "historical_outcome",
    "similarity",
    "context_aware_retrieval",
)


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


def _candidate_count(value: Any) -> int:
    if not isinstance(value, Mapping):
        return 0
    for key in ("candidate_count", "count", "occurrences", "top_k_returned"):
        raw = value.get(key)
        try:
            return max(0, int(raw))
        except (TypeError, ValueError):
            continue
    items = value.get("similar_contexts")
    if isinstance(items, (list, tuple)):
        return len(items)
    return 0


def build_shadow_memory_envelope(
    *,
    query_as_of: Any,
    murphy_direction: str | None,
    memory_evidence: Mapping[str, Any] | None = None,
    provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    year = _year(query_as_of)
    if year is None:
        raise ValueError("query_as_of must contain a valid timestamp")
    if year >= LOCKED_OOS_YEAR:
        raise ValueError("2025_OOS_LOCKED")
    if year > MAX_DEVELOPMENT_YEAR:
        raise ValueError("FUTURE_DATA_FORBIDDEN")
    if not isinstance(memory_evidence, Mapping):
        memory_evidence = {}

    sources = {}
    total_violations = 0
    total_candidates = 0
    for key in MEMORY_KEYS:
        payload = memory_evidence.get(key)
        available = isinstance(payload, Mapping) and bool(payload)
        candidates = _candidate_count(payload)
        lookahead = False
        if isinstance(payload, Mapping):
            lookahead = bool(
                payload.get("lookahead_violation", False)
                or payload.get("future_data_used", False)
                or payload.get("predicted_return_used_as_direction", False)
            )
        sources[key] = {
            "available": available,
            "candidate_count": candidates,
            "lookahead_violation": lookahead,
            "direction_generated": False,
            "final_trade_decision_generated": False,
        }
        total_candidates += candidates
        total_violations += int(lookahead)

    return {
        "status": "PASS_SHADOW_ONLY",
        "query_as_of": query_as_of,
        "evaluation_year": year,
        "murphy_direction": murphy_direction,
        "sources": sources,
        "summary": {
            "retrieval_available": any(x["available"] for x in sources.values()),
            "total_candidate_count": total_candidates,
            "lookahead_violation_count": total_violations,
            "agreement_with_murphy": None,
            "memory_consumed_downstream": None,
        },
        "governance": {
            "memory_role": "EVIDENCE_ONLY",
            "memory_generated_direction": False,
            "similarity_is_sole_decision_maker": False,
            "predicted_return_used_as_direction": False,
            "tuning_parameters_generated": False,
            "2025_used_for_tuning": False,
            "oos_2025_locked": True,
        },
        "provenance": dict(provenance or {}),
    }
