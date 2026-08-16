from __future__ import annotations

from typing import Any, Dict

_ALLOWED_STATUSES = {"PASS", "FAIL", "NOT_EVALUABLE"}
_ALLOWED_DIRECTIONS = {"BULLISH", "BEARISH", "NEUTRAL", "UNKNOWN", None}


def adapt_nison_evaluator_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize an existing Nison result as confirmation-only evidence."""
    status = result.get("status")
    direction = result.get("direction", result.get("directional_confirmation", "UNKNOWN"))
    if status not in _ALLOWED_STATUSES:
        raise ValueError(f"Unsupported evaluator status: {status!r}")
    if direction not in _ALLOWED_DIRECTIONS:
        raise ValueError(f"Unsupported Nison direction: {direction!r}")

    if status == "PASS":
        gate, available = "pass", True
        conflict = "supports" if direction in {"BULLISH", "BEARISH"} else "insufficient"
    elif status == "FAIL":
        gate, available = "fail", True
        conflict = "contradicts" if direction in {"BULLISH", "BEARISH"} else "neutral"
    else:
        gate, available, conflict = "needs_review", False, "insufficient"

    return {
        "module": "nison_confirmation",
        "source_rule_id": result.get("rule_id"),
        "statement": result.get("reason", ""),
        "direction": direction,
        "strength": result.get("strength"),
        "available": available,
        "gate": gate,
        "conflict": conflict,
        "decision_hint": "neutral",
        "confidence_delta": 0.0,
        "raw_evaluator_result": dict(result),
    }
