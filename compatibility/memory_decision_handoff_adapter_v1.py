"""Governed handoff for existing historical-memory evidence.

This adapter only packages already-derived memory evidence for the Decision
Brain boundary. Memory remains evidence-only and cannot create direction or a
final trade decision. 2025+ is rejected for development use.
"""
from __future__ import annotations

from typing import Any, Mapping

from compatibility.memory_evidence_shadow_bridge_v1 import build_shadow_memory_envelope


def build_memory_handoff(
    *,
    query_as_of: Any,
    murphy_direction: str | None,
    historical_context: Mapping[str, Any] | None = None,
    historical_outcome: Mapping[str, Any] | None = None,
    similarity: Mapping[str, Any] | None = None,
    context_aware_retrieval: Mapping[str, Any] | None = None,
    provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    envelope = build_shadow_memory_envelope(
        query_as_of=query_as_of,
        murphy_direction=murphy_direction,
        memory_evidence={
            "historical_context": dict(historical_context or {}),
            "historical_outcome": dict(historical_outcome or {}),
            "similarity": dict(similarity or {}),
            "context_aware_retrieval": dict(context_aware_retrieval or {}),
        },
    )
    return {
        "status": envelope["status"],
        "historical_evidence": {
            "memory_role": "EVIDENCE_ONLY",
            "sources": envelope["memory_evidence"],
            "summary": envelope["summary"],
            "governance": envelope["governance"],
            "provenance": dict(provenance or {}),
            "consumed_by_decision_boundary": True,
            "final_trade_decision": None,
            "direction": None,
        },
    }
