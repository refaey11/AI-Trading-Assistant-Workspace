from typing import Any, Dict, Optional


VALID_TYPES = {"UP", "DOWN"}


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
    confirmation_available_timestamp: Optional[Any],
) -> Dict[str, Any]:
    """Evaluate Murphy's source-defined third-test confirmation.

    Geometry is upstream. This function deliberately does not invent a
    touch/reaction tolerance, ATR threshold, percentage threshold, or
    lookback. It evaluates only already-derived Trendline Geometry V1 facts.
    """
    t = (trendline_type or "").upper()
    required = (
        t in VALID_TYPES,
        anchor_count is not None,
        third_touch is not None,
        reaction_bounce is not None,
        confirmation_available_timestamp is not None,
    )
    if not all(required):
        return _not_evaluable(
            rule_id,
            "Missing Trendline Geometry V1 evidence or confirmation availability timestamp.",
        )

    if anchor_count < 2:
        return _not_evaluable(rule_id, "At least two anchor points are required.")

    passed = bool(third_touch) and bool(reaction_bounce)
    direction = "BULLISH_STRUCTURE" if t == "UP" and passed else (
        "BEARISH_STRUCTURE" if t == "DOWN" and passed else "NONE"
    )

    return {
        "rule_id": rule_id,
        "status": "PASS" if passed else "FAIL",
        "direction": direction,
        "trendline_type": t,
        "anchor_count": anchor_count,
        "third_touch": bool(third_touch),
        "reaction_bounce": bool(reaction_bounce),
        "confirmation_available_timestamp": confirmation_available_timestamp,
        "reason": (
            "Third test/touch succeeded and price bounced from the trendline."
            if passed
            else "Third test confirmation requires both the third touch and a successful reaction/bounce."
        ),
    }


__all__ = ["evaluate_trendline_confirmation"]
