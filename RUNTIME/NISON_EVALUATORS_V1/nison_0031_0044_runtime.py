"""Fail-closed runtime adapters for Nison 0031-0044.

0031-0038 are candlestick pattern scopes. 0039-0044 are frozen
methodology/topic modules. This file exposes only source-backed upstream facts;
it does not invent thresholds, sessionization, comparators, or standalone
trade direction. Nison remains confirmation/context evidence only.
"""
from __future__ import annotations
from typing import Any, Dict

PATTERN_RULES = {f"CANDLE_RULE_{i:04d}" for i in range(31, 39)}
MODULE_RULES = {f"NISON_MODULE_{i:04d}" for i in range(39, 45)}


def _result(rule_id: str, status: str, reason: str) -> Dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "reason": reason,
        "provenance": {
            "source": "Steve Nison",
            "lookahead": "none",
            "numeric_thresholds_invented": False,
            "standalone_direction": False,
        },
    }


def _confirmed(ctx: Dict[str, Any]) -> bool:
    return bool(ctx.get("confirmation", {}).get("confirmed", False))


def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx = payload.get("context", {})

    if rule_id in MODULE_RULES:
        if ctx.get("evidence_available") is not True:
            return _result(rule_id, "NOT_EVALUABLE", "methodology evidence is not available")
        if ctx.get("role") not in {"confirmation", "context"}:
            return _result(rule_id, "NOT_EVALUABLE", "Nison module role must be confirmation/context")
        return _result(rule_id, "PASS", "frozen methodology module accepted as context/confirmation evidence")

    if rule_id not in PATTERN_RULES:
        return _result(rule_id, "NOT_EVALUABLE", "unsupported rule id")

    if rule_id == "CANDLE_RULE_0038":
        prev = ctx.get("previous_session") or {}
        cur = ctx.get("current_session") or {}
        direction = ctx.get("direction")
        if not prev or not cur or direction not in {"bullish", "bearish"}:
            return _result(rule_id, "NOT_EVALUABLE", "requires previous/current session OHLC and direction")
        if direction == "bullish":
            ok = prev.get("high") < cur.get("low")
        else:
            ok = cur.get("high") < prev.get("low")
        return _result(rule_id, "PASS" if ok else "FAIL", "source-mapped Window structural geometry; sessionization remains upstream")

    # 0031-0037: accept only source-backed upstream formation facts.
    if ctx.get("formation_confirmed") is not True:
        return _result(rule_id, "NOT_EVALUABLE", "requires source-backed upstream formation fact")

    # These patterns rely on confirmation/evidence; qualitative source clauses
    # remain explicit gates rather than invented numeric comparators.
    if not _confirmed(ctx):
        return _result(rule_id, "FAIL", "confirmation required by source contract")

    return _result(rule_id, "PASS", "source-backed upstream formation plus confirmation accepted")
