from typing import Any, Dict, Optional


VALID_TYPES = {"UP", "DOWN"}
RULE_BINDINGS = {
    "MURPHY_0006": ("UP", "BULLISH_STRUCTURE"),
    "MURPHY_0007": ("DOWN", "BEARISH_STRUCTURE"),
}


def _not_evaluable(rule_id: str, reason: str) -> Dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": "NOT_EVALUABLE",
        "direction": "NONE",
        "reason": reason,
    }


def evaluate_trendline_confirmation(
    *,
    rule_id: str,
    trendline_type: Optional[str],
    anchor_count: Optional[int],
    third_touch: Optional[bool],
    reaction_bounce: Optional[bool],
    no_break: Optional[bool],
    confirmation_available_timestamp: Optional[Any],
) -> Dict[str, Any]:
    """Evaluate Murphy's source-defined third-test confirmation.

    Geometry is upstream. This function deliberately does not invent a
    touch/reaction tolerance, ATR threshold, percentage threshold, or
    lookback. It evaluates only already-derived Trendline Geometry V1 facts.
    """
    t = (trendline_type or "").upper()
    binding = RULE_BINDINGS.get(rule_id)
    required = (
        binding is not None,
        t in VALID_TYPES,
        anchor_count is not None,
        third_touch is not None,
        reaction_bounce is not None,
        no_break is not None,
        confirmation_available_timestamp is not None,
    )
    if not all(required):
        return _not_evaluable(
            rule_id,
            "Missing Trendline Geometry V1 evidence, rule binding, or confirmation availability timestamp.",
        )

    expected_type, expected_direction = binding
    if t != expected_type:
        return _not_evaluable(
            rule_id,
            f"Rule binding mismatch: {rule_id} requires {expected_type} trendline geometry.",
        )

    if anchor_count < 2:
        return _not_evaluable(rule_id, "At least two anchor points are required.")

    passed = bool(third_touch) and bool(reaction_bounce) and bool(no_break)
    direction = expected_direction if passed else "NONE"

    return {
        "rule_id": rule_id,
        "status": "PASS" if passed else "FAIL",
        "direction": direction,
        "trendline_type": t,
        "anchor_count": anchor_count,
        "third_touch": bool(third_touch),
        "reaction_bounce": bool(reaction_bounce),
        "no_break": bool(no_break),
        "confirmation_available_timestamp": confirmation_available_timestamp,
        "reason": (
            "Third test/touch succeeded, price bounced from the trendline, and no break occurred."
            if passed
            else "Third test confirmation requires third touch, successful reaction/bounce, and no break."
        ),
    }


__all__ = ["evaluate_trendline_confirmation"]
