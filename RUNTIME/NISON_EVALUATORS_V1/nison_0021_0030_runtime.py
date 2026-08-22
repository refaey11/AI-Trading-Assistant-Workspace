"""Fail-closed runtime adapters for Nison CANDLE_RULE_0021..0030.

The canonical source contract is already frozen. This layer does not invent
formation geometry for rules whose detailed formation contract is not exposed
as deterministic runtime inputs. Those rules require upstream formation
facts and source-backed confirmation facts; otherwise they return
NOT_EVALUABLE. Rule 0030 uses only source-stated completion/trend/final-candle
facts. Nison remains confirmation/context evidence only.
"""
from __future__ import annotations
from typing import Any, Dict


def _result(rule_id: str, status: str, reason: str) -> Dict[str, Any]:
    return {"rule_id": rule_id, "status": status, "reason": reason,
            "provenance": {"source": "Steve Nison", "lookahead": "none",
                           "numeric_thresholds_invented": False}}


def _confirmed(ctx: Dict[str, Any]) -> bool:
    return bool(ctx.get("confirmation", {}).get("confirmed", False))


def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if rule_id not in {f"CANDLE_RULE_{i:04d}" for i in range(21, 31)}:
        return _result(rule_id, "NOT_EVALUABLE", "unsupported rule id")
    ctx = payload.get("context", {})

    if rule_id == "CANDLE_RULE_0030":
        if ctx.get("trend") != "Uptrend":
            return _result(rule_id, "NOT_EVALUABLE", "source requires an existing uptrend")
        if ctx.get("formation_complete") is not True:
            return _result(rule_id, "NOT_EVALUABLE", "pattern must be fully completed")
        if ctx.get("final_bullish_strong") is not True:
            return _result(rule_id, "NOT_EVALUABLE", "final bullish candle must satisfy upstream source-backed strong-candle fact")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "three rising methods source-mapped structural contract")

    if ctx.get("formation_confirmed") is not True:
        return _result(rule_id, "NOT_EVALUABLE", "requires source-backed upstream formation fact")

    confirmation_required = {
        "CANDLE_RULE_0021", "CANDLE_RULE_0022", "CANDLE_RULE_0023",
        "CANDLE_RULE_0024", "CANDLE_RULE_0025", "CANDLE_RULE_0026",
        "CANDLE_RULE_0027", "CANDLE_RULE_0028", "CANDLE_RULE_0029",
    }
    if rule_id in confirmation_required and not _confirmed(ctx):
        return _result(rule_id, "FAIL", "confirmation required by source contract")

    return _result(rule_id, "PASS", "upstream formation evidence + source confirmation accepted; no formation geometry invented")
