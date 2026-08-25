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
from evaluation.three_book_decision_evaluator_v1 import evaluate_three_book_decision
from OOS_2025.execution_oos_adapter_v1 import build_execution_plan


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
    if str((provenance or {}).get("fan_in_mode", "")) == "LOSSLESS_FULL_EVIDENCE_WITH_LEGACY_DECISION_COMPAT":
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

    governance = assess_with_governance(
        decision_brain_module,
        row=row,
        query_as_of=query_as_of,
        mode=mode,
        murphy_evidence=murphy_evidence,
        nison_evidence=nison_evidence,
        tiz_evidence=tiz_evidence,
        risk_evidence=risk_evidence,
        historical_evidence=historical_evidence,
        provenance={**dict(provenance or {}), "governed_78_adapter": governed_78.get("receipt", {}) if governed_78 else None},
    )
    if governance.get("status") != "PASS":
        return {"status": "NOT_EVALUABLE", "reason": governance.get("reason", "GOVERNANCE_GATE_NOT_PASS"), "governance": governance}

    decision = evaluate_three_book_decision(
        brain_assessment=governance["assessment"],
        murphy_evidence=murphy_evidence,
        nison_evidence=nison_evidence,
        tiz_evidence={"process_state": tiz_evidence.get("process_state") or tiz_evidence.get("process_gate") or tiz_evidence.get("status"), **dict(tiz_evidence)},
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
        "tiz_process_state": tiz_evidence.get("process_state") or tiz_evidence.get("process_gate") or tiz_evidence.get("status"),
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
            "nison_generated_direction": False,
            "tiz_generated_direction": False,
            "risk_overridden": False,
            "oos_tuning": False,
            "governed_78_adapter_receipt": governed_78.get("receipt", {}) if governed_78 else None,
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
