"""Fail-closed development boundary for Similarity Memory V2.

Preserves the frozen source method semantics and prevents 2025 OOS data from
being used as development retrieval evidence. This layer is evidence-only and
cannot emit direction or a final trade decision.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Optional, Sequence

LOCKED_OOS_YEAR = 2025
MAX_SUPPORTED_YEAR = 2024
DECLARED_TOP_K = 20


@dataclass(frozen=True)
class SimilarityResult:
    status: str
    result: Mapping[str, Any]
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


def validate_similarity_read(
    *,
    current_context: Mapping[str, Any],
    similar_contexts: Sequence[Mapping[str, Any]],
) -> SimilarityResult:
    if not isinstance(current_context, Mapping):
        return SimilarityResult("NOT_EVALUABLE", {}, "INVALID_CURRENT_CONTEXT")
    if not isinstance(similar_contexts, Sequence) or isinstance(similar_contexts, (str, bytes)):
        return SimilarityResult("NOT_EVALUABLE", {}, "INVALID_SIMILAR_CONTEXTS")

    current_year = _parse_year(current_context.get("timestamp"))
    if current_year is None:
        return SimilarityResult("NOT_EVALUABLE", {}, "INVALID_CURRENT_TIMESTAMP")
    if current_year == LOCKED_OOS_YEAR:
        return SimilarityResult("NOT_EVALUABLE", {}, "2025_OOS_LOCKED")
    if current_year > LOCKED_OOS_YEAR:
        return SimilarityResult("NOT_EVALUABLE", {}, "FUTURE_DATA_FORBIDDEN")
    if current_year > MAX_SUPPORTED_YEAR:
        return SimilarityResult("NOT_EVALUABLE", {}, "UNSUPPORTED_DEVELOPMENT_WINDOW")

    if len(similar_contexts) > DECLARED_TOP_K:
        return SimilarityResult("NOT_EVALUABLE", {}, "TOP_K_EXCEEDED")

    clean_matches = []
    for row in similar_contexts:
        if not isinstance(row, Mapping):
            return SimilarityResult("NOT_EVALUABLE", {}, "INVALID_SIMILAR_CONTEXT")
        year = _parse_year(row.get("timestamp"))
        if year is None:
            return SimilarityResult("NOT_EVALUABLE", {}, "INVALID_SIMILAR_TIMESTAMP")
        if year == LOCKED_OOS_YEAR:
            return SimilarityResult("NOT_EVALUABLE", {}, "2025_SIMILAR_MATCH_LOCKED")
        if year > LOCKED_OOS_YEAR:
            return SimilarityResult("NOT_EVALUABLE", {}, "FUTURE_SIMILAR_MATCH_FORBIDDEN")
        if year > MAX_SUPPORTED_YEAR:
            return SimilarityResult("NOT_EVALUABLE", {}, "UNSUPPORTED_SIMILAR_MATCH_WINDOW")
        clean_matches.append(dict(row))

    return SimilarityResult(
        "PASS",
        {
            "current_context": dict(current_context),
            "similar_contexts": clean_matches,
            "top_k": DECLARED_TOP_K,
            "not_a_strategy": True,
            "direction": None,
            "final_trade_decision": None,
        },
    )
