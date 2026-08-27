"""Governed shadow-only bridge for the existing historical memory systems.

This adapter does not rebuild or query any memory subsystem. It accepts already-derived
memory evidence, validates the development/OOS boundary, and packages the evidence for
shadow consumption without emitting or mutating directional decisions.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Optional

LOCKED_OOS_YEAR = 2025
_REQUIRED_SOURCES = (
    "historical_context",
    "historical_outcome",
    "similarity",
    "context_aware_retrieval",
)


def _year(value: Any) -> Optional[int]:
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


def _candidate_count(value: Mapping[str, Any]) -> int:
    raw = value.get("candidate_count", 0)
    if raw is None:
        return 0
    try:
        count = int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("INVALID_CANDIDATE_COUNT") from exc
    if count < 0:
        raise ValueError("INVALID_CANDIDATE_COUNT")
    return count


def build_shadow_memory_envelope(
    *,
    query_as_of: Any,
    murphy_direction: Optional[str] = None,
    memory_evidence: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> dict[str, Any]:
    """Build a fail-closed, evidence-only shadow envelope.

    Development mode is strictly pre-2025. 2025 and later are rejected so this bridge
    cannot become a tuning path or accidentally leak OOS/future information.
    """
    year = _year(query_as_of)
    if year is None:
        raise ValueError("INVALID_QUERY_TIMESTAMP")
    if year >= LOCKED_OOS_YEAR:
        raise ValueError("2025_OOS_LOCKED")

    evidence = dict(memory_evidence or {})
    for source in evidence:
        if source not in _REQUIRED_SOURCES:
            raise ValueError(f"UNKNOWN_MEMORY_SOURCE:{source}")
    for source in _REQUIRED_SOURCES:
        value = evidence.get(source, {})
        if not isinstance(value, Mapping):
            raise ValueError(f"INVALID_{source.upper()}_EVIDENCE")
        status = value.get("status", "NOT_EVALUABLE")
        if status not in {"PASS", "NOT_EVALUABLE"}:
            raise ValueError(f"INVALID_{source.upper()}_STATUS")

    counts = {source: _candidate_count(evidence.get(source, {})) for source in _REQUIRED_SOURCES}
    package = {
        "query_as_of": query_as_of,
        "memory_evidence": {source: dict(evidence.get(source, {})) for source in _REQUIRED_SOURCES},
        "murphy_direction_at_boundary": murphy_direction,
        "summary": {
            "candidate_counts": counts,
            "total_candidate_count": sum(counts.values()),
        },
        "governance": {
            "memory_role": "EVIDENCE_ONLY",
            "memory_generated_direction": False,
            "memory_can_override_murphy": False,
            "2025_used_for_tuning": False,
            "future_data_allowed": False,
            "shadow_only": True,
        },
    }
    return {"status": "PASS_SHADOW_ONLY", **package}
