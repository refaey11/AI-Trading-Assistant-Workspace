"""Governed orchestration boundary for the existing full Decision Brain.

This module creates no new trading logic. It composes the recovered Decision
Brain assessment, governance handoff, Three-Book decision boundary, and frozen
execution adapter. Missing evidence fails closed.
"""
from __future__ import annotations

from importlib import import_module
from typing import Any, Mapping

from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance
from compatibility.governed_78_rule_adapter_v1 import assert_governed_78_package, build_governed_78_package
from compatibility.memory_decision_handoff_adapter_v1 import build_memory_handoff
from evaluation.three_book_decision_evaluator_v1 import evaluate_three_book_decision
from OOS_2025.execution_oos_adapter_v1 import build_execution_plan


def _norm(value: Any) -> str:
    return str(value or "").strip().upper()


def _full_murphy_compatibility(murphy_evidence: Mapping[str, Any]) -> dict[str, Any]:
    rows = murphy_evidence.get("evidence_set") or {}
    if isinstance(rows, Mapping):
        rows = list(rows.values())
    elif not isinstance(rows, list):
        rows = []

    pass_directions = {
        _norm(row.get("directional_confirmation") or row.get("direction"))
        for row in rows
        if _norm(row.get("status")) == "PASS"
    } & {"BULLISH", "BEARISH", "BUY", "SELL", "BULL", "BEAR"}

    bullish = any(v in {"BULLISH", "BUY", "BULL"} for v in pass_directions)
    bearish = any(v in {"BEARISH", "SELL", "BEAR"} for v in pass_directions)

    if bullish and not bearish:
        return {**dict(murphy_evidence), "status": "PASS", "direction": "BULLISH", "compatibility_source": "FULL_34_RULE_EVIDENCE"}
    if bearish and not bullish:
        return {**dict(murphy_evidence), "status": "PASS", "direction": "BEARISH", "compatibility_source": "FULL_34_RULE_EVIDENCE"}
    if bullish and bearish:
        return {**dict(murphy_evidence), "status": "CONFLICT", "direction": "NONE", "compatibility_source": "FULL_34_RULE_EVIDENCE"}

    has_fail = any(_norm(row.get("status")) == "FAIL" for row in rows)
    if has_fail:
        return {**dict(murphy_evidence), "status": "FAIL", "direction": "NONE", "compatibility_source": "FULL_34_RULE_EVIDENCE"}
    return {**dict(murphy_evidence), "status": "NOT_EVALUABLE", "direction": "NONE", "compatibility_source": "FULL_34_RULE_EVIDENCE"}


def _prepare_memory_evidence(
    *,
    historical_evidence: Mapping[str, Any] | None,
    query_as_of: Any,
    murphy_direction: str | None,
    provenance: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    """Normalize existing memory evidence into the governed downstream envelope.

    The adapter is intentionally evidence-only. It never derives BUY/SELL and
    never receives 2025 development queries.
    """
    if historical_evidence is None:
        return None
    if isinstance(historical_evidence.get("historical_evidence"), Mapping):
        # Already packaged by the memory adapter.
        packaged = dict(historical_evidence["historical_evidence"])
        packaged["consumed_by_decision_boundary"] = True
        return packaged

    result = build_memory_handoff(
        query_as_of=query_as_of,
        murphy_direction=murphy_direction,
        historical_context=historical_evidence.get("historical_context"),
        historical_outcome=historical_evidence.get("historical_outcome"),
        similarity=historical_evidence.get("similarity"),
        context_aware_retrieval=historical_evidence.get("context_aware_retrieval"),
        provenance=provenance,
    )
    return result["historical_evidence"]


def assemble_decision_event(
    *,
    decision_brain_module: Any,
    row: Mapping[str, Any],
    query_as_of: Any,
    murphy_evidence: Mapping[str, Any],
    nison_evidence: Mapping[str, Any],
    tiz_evidence: Mapping[str, Any],
    risk_evidence: Mapping[str, Any],
    historical_evidence: Mapping[str, Any] | None,
    source_rule_ids: list[str],
    entry_price: float | None,
    atr: float | None,
    mode: str = "oos_evaluation",
    provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    governed_78 = None
    full_rule_path = str((provenance or {}).get("fan_in_mode", "")) == "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT"
    if full_rule_path:
        adapter_result = build_governed_78_package(
            query_as_of=query_as_of,
            murphy_rows=murphy_evidence.get("evidence_set", {}),
            nison_rows=nison_evidence.get("evidence_set", {}),
            mode=mode,
            provenance=provenance,
        )
        if adapter_result.status != "PASS":
            return {"status": "NOT_EVALUABLE", "reason": adapter_result.reason or "RULE_ADAPTER_REJECTED"}
        governed_78 = dict(adapter_result.package)
        assert_governed_78_package(governed_78)
        murphy_evidence = {**dict(murphy_evidence), "governed_78_package": governed_78}
        nison_evidence = {**dict(nison_evidence), "governed_78_package": governed_78}

    memory_payload = _prepare_memory_evidence(
        historical_evidence=historical_evidence,
        query_as_of=query_as_of,
        murphy_direction=murphy_evidence.get("direction") or murphy_evidence.get("candidate_direction"),
        provenance=provenance,
    )

    governance = assess_with_governance(
        decision_brain_module,
        row=row,
        query_as_of=query_as_of,
        mode=mode,
        murphy_evidence=murphy_evidence,
        nison_evidence=nison_evidence,
        tiz_evidence=tiz_evidence,
        risk_evidence=risk_evidence,
        historical_evidence=memory_payload,
        provenance={
            **dict(provenance or {}),
            "governed_78_adapter": governed_78.get("receipt", {}) if governed_78 else None,
            "memory_handoff_consumed": bool(memory_payload is not None),
        },
    )
    if governance.get("status") != "PASS":
        return {"status": "NOT_EVALUABLE", "reason": governance.get("reason", "GOVERNANCE_GATE_NOT_PASS"), "governance": governance}

    decision_tiz = {"process_state": tiz_evidence.get("process_state") or tiz_evidence.get("process_gate") or tiz_evidence.get("status"), **dict(tiz_evidence)}
    if bool((provenance or {}).get("optional_tiz")) and str(decision_tiz.get("process_state") or "").upper() in {"NOT_EVALUABLE", "AVAILABLE", "MISSING", "ABSENT"}:
        decision_tiz["process_state"] = "READY"
        decision_tiz["process_gate"] = "READY"
        decision_tiz["tiz_verified"] = False
        decision_tiz["tiz_optional_bypass"] = True

    decision_murphy = _full_murphy_compatibility(murphy_evidence) if full_rule_path else dict(murphy_evidence)

    decision = evaluate_three_book_decision(
        brain_assessment=governance["assessment"],
        murphy_evidence=decision_murphy,
        nison_evidence=nison_evidence,
        tiz_evidence=decision_tiz,
        risk_evidence={
            "risk_pass": risk_evidence.get("risk_pass") if "risk_pass" in risk_evidence else str(risk_evidence.get("risk_status") or risk_evidence.get("status") or "").upper() == "PASS",
            "stop_loss": risk_evidence.get("stop_loss"),
            "take_profit": risk_evidence.get("take_profit"),
            "rr": risk_evidence.get("rr"),
        },
        source_rule_ids=source_rule_ids,
        timestamp=str(query_as_of),
    )
    if decision["decision"]["final"] not in {"BUY", "SELL"}:
        return {"status": "NO_TRADE", "decision": decision, "governance": governance, "execution_plan": {"status": "NOT_EXECUTABLE", "reason": "decision_not_approved"}}

    execution_plan = build_execution_plan({
        "timestamp": query_as_of,
        "final_action": decision["decision"]["final"],
        "entry_price": entry_price,
        "atr": atr,
        "risk_pass": True,
        "tiz_process_state": decision_tiz.get("process_state"),
    })
    if execution_plan.get("status") != "EXECUTABLE":
        return {"status": "NOT_EXECUTABLE", "decision": decision, "governance": governance, "execution_plan": execution_plan}

    return {
        "status": "EXECUTABLE",
        "decision": decision,
        "governance": governance,
        "execution_plan": execution_plan,
        "audit": {
            "source_rule_ids": list(source_rule_ids),
            "query_as_of": query_as_of,
            "historical_memory_used_for_direction": False,
            "historical_memory_consumed_downstream": bool(memory_payload is not None),
            "nison_generated_direction": False,
            "tiz_generated_direction": False,
            "risk_overridden": False,
            "oos_tuning": False,
            "governed_78_adapter_receipt": governed_78.get("receipt", {}) if governed_78 else None,
            "tiz_optional_bypass": bool(decision_tiz.get("tiz_optional_bypass", False)),
            "murphy_compatibility_source": "FULL_34_RULE_EVIDENCE" if full_rule_path else "LEGACY_INPUT",
        },
    }


def assemble_from_dict(event: Mapping[str, Any]) -> dict[str, Any]:
    module = import_module("RECOVERED_SOURCES.DECISION_BRAIN_V1.decision_brain")
    return assemble_decision_event(
        decision_brain_module=module,
        row=event["row"],
        query_as_of=event["query_as_of"],
        murphy_evidence=event.get("murphy_evidence", {}),
        nison_evidence=event.get("nison_evidence", {}),
        tiz_evidence=event.get("tiz_evidence", {}),
        risk_evidence=event.get("risk_evidence", {}),
        historical_evidence=event.get("historical_evidence"),
        source_rule_ids=list(event.get("source_rule_ids", [])),
        entry_price=event.get("entry_price"),
        atr=event.get("atr"),
        mode=event.get("mode", "oos_evaluation"),
        provenance=event.get("provenance"),
    )
