"""Minimal integration wrapper for PIT Historical Memory.

The existing Decision Brain / Three-Book / Risk / execution semantics remain
unchanged. This wrapper only resolves point-in-time Historical Context Memory
as evidence and injects that evidence into the existing full Decision Brain
assembler with explicit provenance.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping

from RUNTIME.DECISION_RUNTIME_V1.historical_context_memory_pit_adapter_v1 import lookup_context_pit
from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event


def build_memory_evidence(
    source_csv: str | Path,
    *,
    pair: str,
    context_signature: str,
    query_as_of: Any,
    limit: int = 50,
) -> dict[str, Any]:
    result = lookup_context_pit(
        Path(source_csv),
        pair=pair,
        context_signature=context_signature,
        query_as_of=query_as_of,
        limit=limit,
    )
    payload = asdict(result)
    payload["evidence_only"] = True
    payload["direction_generated"] = False
    payload["trade_command_generated"] = False
    payload["lookahead_guard"] = "timestamp < query_as_of"
    return payload


def assemble_with_pit_memory(
    *,
    decision_brain_module: Any,
    row: Mapping[str, Any],
    query_as_of: Any,
    murphy_evidence: Mapping[str, Any],
    nison_evidence: Mapping[str, Any],
    tiz_evidence: Mapping[str, Any],
    risk_evidence: Mapping[str, Any],
    source_rule_ids: list[str],
    entry_price: float | None,
    atr: float | None,
    memory_source_csv: str | Path,
    pair: str,
    context_signature: str,
    mode: str = "oos_evaluation",
    optional_tiz: bool = False,
    provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the existing Full Brain assembler with PIT memory as evidence."""
    memory = build_memory_evidence(
        memory_source_csv,
        pair=pair,
        context_signature=context_signature,
        query_as_of=query_as_of,
    )
    merged_provenance = {
        **dict(provenance or {}),
        "historical_memory": {
            "status": memory["status"],
            "candidate_count": memory["candidate_count"],
            "latest_candidate_timestamp": memory["latest_candidate_timestamp"],
            "excluded_future_count": memory["excluded_future_count"],
            "excluded_self_count": memory["excluded_self_count"],
            "evidence_only": True,
            "direction_generated": False,
            "trade_command_generated": False,
        },
        "optional_tiz": optional_tiz,
    }

    # Keep the existing assembler untouched. Historical memory travels only as
    # historical_evidence and can never be used as a directional input.
    return assemble_decision_event(
        decision_brain_module=decision_brain_module,
        row=row,
        query_as_of=query_as_of,
        murphy_evidence=murphy_evidence,
        nison_evidence=nison_evidence,
        tiz_evidence=tiz_evidence,
        risk_evidence=risk_evidence,
        historical_evidence=memory,
        source_rule_ids=list(source_rule_ids),
        entry_price=entry_price,
        atr=atr,
        mode=mode,
        provenance=merged_provenance,
    )
