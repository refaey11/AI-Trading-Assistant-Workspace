"""Governed evaluator for the existing Three-Book Decision Contract V1.

This module is a boundary evaluator, not a new strategy. It does not invent
new thresholds, indicators, or book semantics. It maps an existing frozen
Decision Brain assessment plus already-derived Murphy/Nison/TIZ/Risk evidence
into the contract's BUY/SELL/NO_TRADE status.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence
import json
from pathlib import Path

from compatibility.governed_78_rule_adapter_v1 import assert_governed_78_package

ALLOWLIST_PATH = Path("governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json")


def _norm(value: Any) -> str:
    return str(value or "").strip().upper()


def _allowed_rule_ids() -> set[str]:
    data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    return set(data["verified_runtime"]["MURPHY"]) | set(data["verified_runtime"]["NISON"])


def _rule_ids_allowed(rule_ids: Sequence[str]) -> bool:
    allowed = _allowed_rule_ids()
    return bool(rule_ids) and all(str(rule_id) in allowed for rule_id in rule_ids)


def _rule_rows(evidence: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = evidence.get("evidence_set") or {}
    if isinstance(rows, Mapping):
        return [dict(row) for row in rows.values() if isinstance(row, Mapping)]
    if isinstance(rows, Sequence) and not isinstance(rows, (str, bytes)):
        return [dict(row) for row in rows if isinstance(row, Mapping)]
    return []


def _full_rule_audit(
    murphy_evidence: Mapping[str, Any],
    nison_evidence: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Validate a full rule envelope and require the governed adapter receipt.

    Missing/unevaluable rule results are preserved and do not become signals.
    The consumer only uses existing PASS/confirmation/contradiction semantics.
    """
    m_rows = _rule_rows(murphy_evidence)
    n_rows = _rule_rows(nison_evidence)
    if not m_rows and not n_rows:
        return None

    governed_package = murphy_evidence.get("governed_78_package")
    nison_package = nison_evidence.get("governed_78_package")
    if not isinstance(governed_package, Mapping) or governed_package != nison_package:
        return {"status": "REJECTED", "reason": "MISSING_OR_MISMATCHED_78_RULE_ADAPTER_PACKAGE"}
    try:
        assert_governed_78_package(governed_package)
    except AssertionError as exc:
        return {"status": "REJECTED", "reason": str(exc)}

    m_ids = {str(r.get("source_rule_id") or r.get("rule_id") or "").strip() for r in m_rows}
    n_ids = {str(r.get("source_rule_id") or r.get("rule_id") or "").strip() for r in n_rows}
    m_ids.discard("")
    n_ids.discard("")

    package_m_ids = {str(r.get("source_rule_id") or r.get("rule_id") or "").strip() for r in governed_package["murphy"]["rows"]}
    package_n_ids = {str(r.get("source_rule_id") or r.get("rule_id") or "").strip() for r in governed_package["nison"]["rows"]}
    if m_ids != package_m_ids or n_ids != package_n_ids:
        return {"status": "REJECTED", "reason": "ADAPTER_PACKAGE_EVIDENCE_SET_MISMATCH"}

    if len(m_ids) != 34 or len(n_ids) != 44:
        return {
            "status": "REJECTED",
            "reason": "FULL_RULE_EVIDENCE_INCOMPLETE",
            "murphy_rule_count": len(m_ids),
            "nison_rule_count": len(n_ids),
        }

    allowed = _allowed_rule_ids()
    if not m_ids.issubset(allowed) or not n_ids.issubset(allowed):
        return {"status": "REJECTED", "reason": "FULL_RULE_EVIDENCE_ALLOWLIST_REJECT"}

    m_pass_directions = {
        _norm(r.get("directional_confirmation") or r.get("direction"))
        for r in m_rows
        if _norm(r.get("status")) == "PASS"
    } & {"BULLISH", "BEARISH", "BUY", "SELL", "BULL", "BEAR"}
    m_bullish = any(d in {"BULLISH", "BUY", "BULL"} for d in m_pass_directions)
    m_bearish = any(d in {"BEARISH", "SELL", "BEAR"} for d in m_pass_directions)

    # For the full-rule path, a Nison FAIL is only a contradiction when its
    # direction explicitly opposes the Brain/Murphy direction. A same-direction
    # FAIL means "not confirmed", not "contradicted". The top-level aggregate
    # contradiction flag is intentionally not authoritative for the governed
    # full-rule envelope because it may represent the legacy candidate stream.
    n_opposite_direction_fail = False
    n_confirmed = False
    for row in n_rows:
        status = _norm(row.get("status"))
        direction = _norm(row.get("direction") or row.get("directional_confirmation"))
        explicit_contradiction = bool(row.get("contradiction", False)) or _norm(row.get("confirmation")) in {
            "CONTRADICTED",
            "CONTRADICTION",
        }
        if _norm(row.get("confirmation")) == "CONFIRMED":
            n_confirmed = True
        if explicit_contradiction:
            n_opposite_direction_fail = True
        elif status == "FAIL" and direction in {"BULLISH", "BUY", "BULL"} and m_bearish:
            n_opposite_direction_fail = True
        elif status == "FAIL" and direction in {"BEARISH", "SELL", "BEAR"} and m_bullish:
            n_opposite_direction_fail = True

    return {
        "status": "PASS",
        "murphy_rule_count": len(m_ids),
        "nison_rule_count": len(n_ids),
        "murphy_bullish_pass": m_bullish,
        "murphy_bearish_pass": m_bearish,
        "nison_contradiction": n_opposite_direction_fail,
        "nison_confirmed": n_confirmed,
        "adapter_receipt": dict(governed_package.get("receipt", {})),
    }


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
    """Evaluate the existing contract and consume the governed full-rule envelope."""
    if not _rule_ids_allowed(source_rule_ids):
        return _no_trade("RULE_ALLOWLIST_REJECT", timestamp, source_rule_ids)

    bias = _norm(brain_assessment.get("directional_bias"))
    murphy_status = _norm(murphy_evidence.get("status"))
    murphy_direction = _norm(murphy_evidence.get("direction") or murphy_evidence.get("candidate_direction"))

    full_audit = _full_rule_audit(murphy_evidence, nison_evidence)
    if full_audit and full_audit.get("status") != "PASS":
        return _no_trade(str(full_audit.get("reason", "FULL_RULE_EVIDENCE_REJECTED")), timestamp, source_rule_ids)
    if full_audit:
        if full_audit["murphy_bullish_pass"] and full_audit["murphy_bearish_pass"]:
            return _no_trade("MURPHY_FULL_RULE_CONFLICT", timestamp, source_rule_ids)
        if full_audit["murphy_bullish_pass"] and bias == "BEARISH":
            return _no_trade("MURPHY_FULL_RULE_BRAIN_DIRECTION_CONFLICT", timestamp, source_rule_ids)
        if full_audit["murphy_bearish_pass"] and bias == "BULLISH":
            return _no_trade("MURPHY_FULL_RULE_BRAIN_DIRECTION_CONFLICT", timestamp, source_rule_ids)
        if full_audit["nison_contradiction"]:
            return _no_trade("NISON_FULL_RULE_CONTRADICTION", timestamp, source_rule_ids)

    if murphy_status != "PASS":
        return _no_trade("MURPHY_CONTEXT_NOT_PASS", timestamp, source_rule_ids)
    if murphy_direction in {"BULL", "BULLISH", "BUY"} and bias != "BULLISH":
        return _no_trade("MURPHY_BRAIN_DIRECTION_CONFLICT", timestamp, source_rule_ids)
    if murphy_direction in {"BEAR", "BEARISH", "SELL"} and bias != "BEARISH":
        return _no_trade("MURPHY_BRAIN_DIRECTION_CONFLICT", timestamp, source_rule_ids)

    tiz_state = _norm(tiz_evidence.get("process_state") or tiz_evidence.get("process_gate") or tiz_evidence.get("status"))
    blocked_flags = {
        "impulse_override": bool(tiz_evidence.get("impulse_override", False)),
        "loss_chasing": bool(tiz_evidence.get("loss_chasing", False)),
        "revenge_trade": bool(tiz_evidence.get("revenge_trade", False)),
    }
    if tiz_state != "READY":
        return _no_trade("TIZ_PROCESS_GATE_NOT_READY", timestamp, source_rule_ids)
    if any(blocked_flags.values()):
        return _no_trade("TIZ_BEHAVIORAL_BLOCK", timestamp, source_rule_ids)

    if not bool(risk_evidence.get("risk_pass", False)):
        return _no_trade("RISK_GATE_FAIL_OR_NOT_EVALUABLE", timestamp, source_rule_ids)
    if not str(risk_evidence.get("stop_loss") or "").strip():
        return _no_trade("STOP_LOSS_UNDEFINED", timestamp, source_rule_ids)

    nison_confirmation = _norm(nison_evidence.get("confirmation"))
    if full_audit and full_audit.get("nison_confirmed"):
        nison_confirmation = "CONFIRMED"
    if full_audit:
        nison_contradiction = bool(full_audit.get("nison_contradiction"))
    else:
        nison_contradiction = bool(nison_evidence.get("contradiction", False)) or nison_confirmation in {"CONTRADICTED", "CONTRADICTION"}
    if nison_contradiction:
        return _no_trade("NISON_CONTRADICTION", timestamp, source_rule_ids)

    if bias not in {"BULLISH", "BEARISH"}:
        return _no_trade("BRAIN_DIRECTION_NOT_EXECUTABLE", timestamp, source_rule_ids)

    final = "BUY" if bias == "BULLISH" else "SELL"
    strength = "strong" if nison_confirmation == "CONFIRMED" else "medium"
    confidence = float(brain_assessment.get("confidence", 0.0) or 0.0)

    audit = {
        "source_refs": list(source_rule_ids),
        "timestamp": timestamp,
        "backtest_status": "UNTESTED",
        "full_rule_consumer": full_audit,
    }

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
            "reasons_for": ["Murphy context passed", "Full Murphy rule envelope consumed", "Governed 78-rule adapter receipt verified", "TIZ process gate passed", "Risk hard gate passed"],
            "reasons_against": [],
            "final": final,
        },
        "audit": audit,
    }


def _no_trade(reason: str, timestamp: str, source_rule_ids: Sequence[str]) -> dict[str, Any]:
    return {
        "signal": {"direction": "NO_TRADE", "confidence": 0.0, "status": "REJECTED"},
        "murphy": {},
        "nison": {},
        "trading_zone": {},
        "risk_engine": {},
        "decision": {"logic": "reject", "reasons_for": [], "reasons_against": [reason], "final": "NO_TRADE"},
        "audit": {"source_refs": list(source_rule_ids), "timestamp": timestamp, "backtest_status": "UNTESTED"},
    }
