from __future__ import annotations

from typing import Any, Dict


_ALLOWED_STATUSES = {"PASS", "FAIL", "NOT_EVALUABLE"}
_ALLOWED_DIRECTIONS = {"BULLISH", "BEARISH", "NEUTRAL", "UNKNOWN", None}
_CANDIDATE_TO_CONFIRMATION = {
    "BUY_CANDIDATE": "BULLISH",
    "SELL_CANDIDATE": "BEARISH",
}


def adapt_nison_evaluator_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize an existing Nison evaluator result without changing its semantics.

    Nison is confirmation-only: PASS can support an already-established direction,
    FAIL can contradict it, and NOT_EVALUABLE cannot create or block direction by
    itself. Candidate labels from legacy/runtime evaluators are normalized to
    confirmation evidence labels only; this adapter never creates a trade decision.
    """
    status = result.get("status")
    raw_direction = result.get("direction", result.get("directional_confirmation", "UNKNOWN"))
    direction = _CANDIDATE_TO_CONFIRMATION.get(raw_direction, raw_direction)

    if status not in _ALLOWED_STATUSES:
        raise ValueError(f"Unsupported evaluator status: {status!r}")
    if direction not in _ALLOWED_DIRECTIONS:
        raise ValueError(f"Unsupported Nison direction: {direction!r}")

    if status == "PASS":
        gate = "pass"
        available = True
        conflict = "supports" if direction in {"BULLISH", "BEARISH"} else "insufficient"
    elif status == "FAIL":
        gate = "fail"
        available = True
        conflict = "contradicts" if direction in {"BULLISH", "BEARISH"} else "neutral"
    else:
        gate = "needs_review"
        available = False
        conflict = "insufficient"

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
        "raw_direction": raw_direction,
        "raw_evaluator_result": dict(result),
    }
