"""Governed evaluator for the existing Three-Book Decision Contract V1.

TIZ remains audit/process context only. It is not a production execution gate.
The evaluator maps an existing Decision Brain assessment plus Murphy/Nison/Risk
 evidence into BUY/SELL/NO_TRADE without creating new directional logic.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence
import json
from pathlib import Path

ALLOWLIST_PATH = Path("governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json")


def _norm(value: Any) -> str:
    return str(value or "").strip().upper()


def _allowed_rule_ids() -> set[str]:
    data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    return set(data["verified_runtime"]["MURPHY"]) | set(data["verified_runtime"]["NISON"])


def _rule_ids_allowed(rule_ids: Sequence[str]) -> bool:
    allowed = _allowed_rule_ids()
    return bool(rule_ids) and all(str(rule_id) in allowed for rule_id in rule_ids)


def evaluate_three_book_decision(
    *,
    brain_assessment: Mapping[str, Any],
    murphy_evidence: Mapping[str, Any],
    nison_evidence: Mapping[str, Any],
    tiz_evidence: Mapping[str, Any],
    risk_evidence: Mapping[str, Any],
    source_rule_ids: Sequence[str],
    timestamp: str,
) -> dict[str, Any]:
    """Evaluate the existing contract with TIZ as audit-only process context."""
    if not _rule_ids_allowed(source_rule_ids):
        return _no_trade("RULE_ALLOWLIST_REJECT", timestamp, source_rule_ids, tiz_evidence)

    bias = _norm(brain_assessment.get("directional_bias"))
    murphy_status = _norm(murphy_evidence.get("status"))
    murphy_direction = _norm(murphy_evidence.get("direction") or murphy_evidence.get("candidate_direction"))

    if murphy_status != "PASS":
        return _no_trade("MURPHY_CONTEXT_NOT_PASS", timestamp, source_rule_ids, tiz_evidence)
    if murphy_direction in {"BULL", "BULLISH", "BUY"} and bias != "BULLISH":
        return _no_trade("MURPHY_BRAIN_DIRECTION_CONFLICT", timestamp, source_rule_ids, tiz_evidence)
    if murphy_direction in {"BEAR", "BEARISH", "SELL"} and bias != "BEARISH":
        return _no_trade("MURPHY_BRAIN_DIRECTION_CONFLICT", timestamp, source_rule_ids, tiz_evidence)

    if not bool(risk_evidence.get("risk_pass", False)):
        return _no_trade("RISK_GATE_FAIL_OR_NOT_EVALUABLE", timestamp, source_rule_ids, tiz_evidence)
    if not str(risk_evidence.get("stop_loss") or "").strip():
        return _no_trade("STOP_LOSS_UNDEFINED", timestamp, source_rule_ids, tiz_evidence)

    nison_confirmation = _norm(nison_evidence.get("confirmation"))
    nison_contradiction = bool(nison_evidence.get("contradiction", False)) or nison_confirmation in {"CONTRADICTED", "CONTRADICTION"}
    if nison_contradiction:
        return _no_trade("NISON_CONTRADICTION", timestamp, source_rule_ids, tiz_evidence)

    if bias not in {"BULLISH", "BEARISH"}:
        return _no_trade("BRAIN_DIRECTION_NOT_EXECUTABLE", timestamp, source_rule_ids, tiz_evidence)

    final = "BUY" if bias == "BULLISH" else "SELL"
    strength = "strong" if nison_confirmation == "CONFIRMED" else "medium"
    confidence = float(brain_assessment.get("confidence", 0.0) or 0.0)

    return {
        "signal": {
            "direction": final,
            "confidence": confidence,
            "status": "EXECUTABLE",
        },
        "murphy": dict(murphy_evidence),
        "nison": dict(nison_evidence),
        "trading_zone": dict(tiz_evidence),
        "risk_engine": dict(risk_evidence),
        "decision": {
            "logic": strength,
            "reasons_for": ["Murphy context passed", "Risk hard gate passed"],
            "reasons_against": [],
            "final": final,
        },
        "audit": {
            "source_refs": list(source_rule_ids),
            "timestamp": timestamp,
            "backtest_status": "UNTESTED",
            "tiz_execution_gate": "DISABLED",
            "tiz_audit_state": dict(tiz_evidence),
        },
    }


def _no_trade(reason: str, timestamp: str, source_rule_ids: Sequence[str], tiz_evidence: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "signal": {"direction": "NO_TRADE", "confidence": 0.0, "status": "REJECTED"},
        "murphy": {},
        "nison": {},
        "trading_zone": dict(tiz_evidence),
        "risk_engine": {},
        "decision": {"logic": "reject", "reasons_for": [], "reasons_against": [reason], "final": "NO_TRADE"},
        "audit": {
            "source_refs": list(source_rule_ids),
            "timestamp": timestamp,
            "backtest_status": "UNTESTED",
            "tiz_execution_gate": "DISABLED",
            "tiz_audit_state": dict(tiz_evidence),
        },
    }
