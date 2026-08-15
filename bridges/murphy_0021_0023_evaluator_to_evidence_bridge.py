from __future__ import annotations

from typing import Any, Dict


def adapt_evaluator_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize an existing 0021-0023 evaluator result without changing its semantics."""
    status = result.get("status")
    direction = result.get("directional_confirmation", "UNKNOWN")

    if status == "PASS":
        gate = "pass"
        available = True
        decision_hint = {"BULLISH": "bullish", "BEARISH": "bearish"}.get(direction, "neutral")
        conflict = "supports" if decision_hint != "neutral" else "insufficient"
    elif status == "FAIL":
        gate = "fail"
        available = True
        decision_hint = "no_trade"
        conflict = "neutral"
    elif status == "NOT_EVALUABLE":
        gate = "needs_review"
        available = False
        decision_hint = "neutral"
        conflict = "insufficient"
    else:
        raise ValueError(f"Unsupported evaluator status: {status!r}")

    return {
        "module": "murphy_evaluator",
        "source_rule_id": result.get("rule_id"),
        "statement": result.get("reason", ""),
        "direction": direction,
        "strength": None,
        "available": available,
        "gate": gate,
        "conflict": conflict,
        "decision_hint": decision_hint,
        "confidence_delta": 0.0,
        "raw_evaluator_result": dict(result),
    }
