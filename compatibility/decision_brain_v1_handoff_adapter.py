"""Governed handoff adapter around the recovered Decision Brain V1 source.

This adapter does not modify the recovered Decision Brain and does not invent
its scoring. It packages already-derived evidence and enforces integration
boundaries before/after the V1 market assessment.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
from typing import Any, Mapping

LOCKED_OOS_YEAR = 2025


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


def _normalize_gate(value: Any) -> str:
    text = str(value or "").strip().upper()
    return text if text in {"PASS", "FAIL", "NOT_EVALUABLE"} else "NOT_EVALUABLE"


def _normalize_risk_gate(risk: Mapping[str, Any]) -> str:
    textual = risk.get("risk_status") or risk.get("status")
    if textual is not None and str(textual).strip() != "":
        return _normalize_gate(textual)
    if "risk_pass" in risk and risk.get("risk_pass") is not None:
        return "PASS" if bool(risk.get("risk_pass")) else "FAIL"
    return "NOT_EVALUABLE"


def _sanitize_historical(historical: Mapping[str, Any] | None) -> dict[str, Any]:
    payload = dict(historical or {})
    sources = deepcopy(payload.get("sources", {}))
    sanitized = {
        "retrieval_status": payload.get("retrieval_status") or payload.get("status"),
        "candidate_count": payload.get("candidate_count"),
        "top_k_returned": payload.get("top_k_returned"),
        "nearest_distance": payload.get("nearest_distance"),
        "distance_summary": deepcopy(payload.get("distance_summary", {})),
        "historical_evidence_ids_or_positions": deepcopy(payload.get("historical_evidence_ids_or_positions", [])),
        "evidence_time_range": deepcopy(payload.get("evidence_time_range", {})),
        "outcome_evidence": deepcopy(payload.get("outcome_evidence", {})),
        "context_evidence": deepcopy(payload.get("context_evidence", {})),
        "warnings": deepcopy(payload.get("warnings", [])),
        "sources": sources,
        "memory_role": payload.get("memory_role", "EVIDENCE_ONLY"),
        "query_as_of": payload.get("query_as_of"),
        "provenance": deepcopy(payload.get("provenance", {})),
        "consumed_by_decision_boundary": bool(payload.get("consumed_by_decision_boundary", False)),
        "predicted_return_used_as_direction": False,
    }
    return sanitized


def assess_with_governance(
    decision_brain_module,
    *,
    row: Mapping[str, Any],
    query_as_of: Any,
    mode: str = "development",
    murphy_evidence: Mapping[str, Any] | None = None,
    nison_evidence: Mapping[str, Any] | None = None,
    tiz_evidence: Mapping[str, Any] | None = None,
    risk_evidence: Mapping[str, Any] | None = None,
    historical_evidence: Mapping[str, Any] | None = None,
    provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if mode not in {"development", "oos_evaluation"}:
        return {"status": "NOT_EVALUABLE", "reason": "INVALID_MODE"}

    year = _year(query_as_of)
    if year is None:
        return {"status": "NOT_EVALUABLE", "reason": "INVALID_QUERY_TIMESTAMP"}
    if mode == "development" and year >= LOCKED_OOS_YEAR:
        return {"status": "NOT_EVALUABLE", "reason": "2025_OOS_LOCKED"}
    if year > LOCKED_OOS_YEAR:
        return {"status": "NOT_EVALUABLE", "reason": "FUTURE_DATA_FORBIDDEN"}

    row_copy = deepcopy(dict(row))
    # Similarity remains evidence-only and is never passed as a directional signal.
    assessment = decision_brain_module.assess(row_copy, similarity=None)
    assessment_dict = asdict(assessment)

    tiz = dict(tiz_evidence or {})
    risk = dict(risk_evidence or {})
    nison = dict(nison_evidence or {})

    tiz_gate = _normalize_gate(tiz.get("process_gate") or tiz.get("status"))
    risk_gate = _normalize_risk_gate(risk)
    nison_confirmation = str(nison.get("confirmation") or "ABSENT").upper()
    nison_contradiction = bool(nison.get("contradiction", False))

    hard_blocks: list[str] = []
    needs_review: list[str] = []
    if tiz_gate == "FAIL":
        hard_blocks.append("TIZ_PROCESS_GATE_FAIL")
    elif tiz_gate == "NOT_EVALUABLE":
        needs_review.append("TIZ_PROCESS_GATE_NOT_EVALUABLE")
    if risk_gate == "FAIL":
        hard_blocks.append("RISK_GATE_FAIL")
    elif risk_gate == "NOT_EVALUABLE":
        needs_review.append("RISK_GATE_NOT_EVALUABLE")
    if nison_contradiction or nison_confirmation in {"CONTRADICTED", "CONTRADICTION"}:
        needs_review.append("NISON_CONTRADICTION")

    history = _sanitize_historical(historical_evidence)
    return {
        "status": "PASS",
        "mode": mode,
        "query_as_of": query_as_of,
        "assessment": assessment_dict,
        "knowledge_alignment": deepcopy(murphy_evidence or {}),
        "murphy_evidence": deepcopy(murphy_evidence or {}),
        "nison_evidence": nison,
        "tiz_evidence": tiz,
        "risk_evidence": risk,
        "historical_evidence": history,
        "execution": {
            "eligible": not hard_blocks and not needs_review and assessment_dict.get("directional_bias") not in {"neutral", "conflicted"},
            "hard_blocks": hard_blocks,
            "needs_review": needs_review,
            "final_trade_decision": None,
        },
        "governance": {
            "recovered_v1_unchanged": True,
            "similarity_generated_direction": False,
            "predicted_return_used_as_direction": False,
            "nison_generated_direction": False,
            "tiz_generated_direction": False,
            "risk_gate_overridable": False,
            "future_data_allowed": False,
            "2025_used_for_tuning": False,
            "historical_memory_consumed_downstream": bool(history.get("consumed_by_decision_boundary")),
        },
        "provenance": deepcopy(provenance or {}),
    }
