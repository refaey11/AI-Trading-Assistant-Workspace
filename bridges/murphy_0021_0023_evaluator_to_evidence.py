"""Source-locked bridge for Murphy 0021-0023 evaluator results.

This module normalizes an evaluator result only. It does not infer market state,
create a trade, alter evaluator semantics, or assign confidence from PASS/FAIL.
The mapping is defined by MURPHY_0021_0023_RULE_ADAPTER_INTEGRATION_CONTRACT_V2.
"""

from typing import Any, Dict


def _direction(value: Any) -> str:
    value = str(value or "").strip().upper()
    if value == "BULLISH":
        return "bullish"
    if value == "BEARISH":
        return "bearish"
    return "neutral"


def adapt_evaluator_result(result: Dict[str, Any], canonical_statement: str = "") -> Dict[str, Any]:
    status = str(result.get("status") or "").strip().upper()
    direction = _direction(result.get("directional_confirmation"))
    rule_id = str(result.get("rule_id") or "UNKNOWN_RULE")
    reason = str(result.get("reason") or "").strip()

    if status == "PASS":
        available = True
        gate = "pass"
        conflict = "neutral"
        decision_hint = direction if direction in {"bullish", "bearish"} else "neutral"
    elif status == "FAIL":
        available = True
        gate = "fail"
        conflict = "contradicts"
        decision_hint = "neutral"
    elif status == "NOT_EVALUABLE":
        available = False
        gate = "needs_review"
        conflict = "insufficient"
        decision_hint = "neutral"
    else:
        available = False
        gate = "needs_review"
        conflict = "insufficient"
        decision_hint = "neutral"

    return {
        "module": "murphy_context",
        "source_rule_id": rule_id,
        "statement": canonical_statement or reason,
        "direction": direction,
        "strength": None,
        "available": available,
        "gate": gate,
        "conflict": conflict,
        "decision_hint": decision_hint,
        "confidence_delta": 0,
        "raw_evaluator_result": dict(result),
    }
