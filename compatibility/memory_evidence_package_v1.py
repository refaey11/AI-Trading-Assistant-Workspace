"""Minimal governed package for the three verified historical-memory sources.

This is a packaging boundary, not a strategy. It accepts already-derived evidence
from Historical Context, Historical Outcome, and Similarity Memory V2 without
recomputing or inventing their semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional

LOCKED_OOS_YEAR = 2025


@dataclass(frozen=True)
class MemoryEvidencePackageResult:
    status: str
    package: Mapping[str, Any]
    reason: Optional[str] = None


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


def build_memory_evidence_package(
    *,
    query_as_of: Any,
    historical_context: Mapping[str, Any],
    historical_outcome: Mapping[str, Any],
    similarity: Mapping[str, Any],
    mode: str = "development",
    provenance: Optional[Mapping[str, Any]] = None,
) -> MemoryEvidencePackageResult:
    if mode not in {"development", "oos_evaluation"}:
        return MemoryEvidencePackageResult("NOT_EVALUABLE", {}, "INVALID_MODE")

    year = _year(query_as_of)
    if year is None:
        return MemoryEvidencePackageResult("NOT_EVALUABLE", {}, "INVALID_QUERY_TIMESTAMP")
    if mode == "development" and year >= LOCKED_OOS_YEAR:
        return MemoryEvidencePackageResult("NOT_EVALUABLE", {}, "2025_OOS_LOCKED")
    if year > LOCKED_OOS_YEAR:
        return MemoryEvidencePackageResult("NOT_EVALUABLE", {}, "FUTURE_DATA_FORBIDDEN")

    for name, value in (
        ("historical_context", historical_context),
        ("historical_outcome", historical_outcome),
        ("similarity", similarity),
    ):
        if not isinstance(value, Mapping):
            return MemoryEvidencePackageResult("NOT_EVALUABLE", {}, f"INVALID_{name.upper()}_EVIDENCE")

    package = {
        "query_as_of": query_as_of,
        "mode": mode,
        "historical_context": dict(historical_context),
        "historical_outcome": dict(historical_outcome),
        "similarity": dict(similarity),
        "provenance": dict(provenance or {}),
        "memory_role": "EVIDENCE_ONLY",
        "direction": None,
        "final_trade_decision": None,
        "similarity_is_sole_decision_maker": False,
        "predicted_return_used_as_direction": False,
        "tuning_parameters_generated": False,
    }
    return MemoryEvidencePackageResult("PASS", package)
