"""Source-locked bridge for Murphy 0028 evaluator results.

This bridge normalizes the existing Murphy 0028 evaluator output into Decision
Brain evidence. It does not detect divergence, change evaluator semantics,
create a trade, infer the opposite direction, or assign a confidence magnitude.

Source/project contract basis:
- MURPHY_0027_0029_EVALUATOR_V1
- GBPUSD Rule Adapter Contract V1

0028 semantics already implemented upstream:
confirmed BEARISH divergence at a HIGH pivot -> PASS / BEARISH_WARNING.
"""

from typing import Any, Dict


RULE_ID = "MURPHY_0028"
CANONICAL_STATEMENT = (
    "Confirmed bearish price/RSI divergence on a high-pivot sequence."
)


def _direction(value: Any) -> str:
    """Normalize the evaluator's directional confirmation without inference."""
    value = str(value or "").strip().upper()
    if value in {"BEARISH", "BEARISH_WARNING"}:
        return "bearish"
    if value in {"BULLISH", "BULLISH_WARNING"}:
        return "bullish"
    return "neutral"


def adapt_evaluator_result(
    result: Dict[str, Any], canonical_statement: str = CANONICAL_STATEMENT
) -> Dict[str, Any]:
    """Map an existing 0028 evaluator result to Rule Adapter evidence.

    The mapping is status-preserving. FAIL never becomes the opposite direction,
    NOT_EVALUABLE never becomes PASS, and confidence_delta is always zero.
    """
    status = str(result.get("status") or "").strip().upper()
    rule_id = str(result.get("rule_id") or RULE_ID)
    reason = str(result.get("reason") or "").strip()

    # Only evaluator-emitted directional confirmations are normalized.
    direction = _direction(result.get("directional_confirmation"))

    if status == "PASS":
        available = True
        gate = "pass"
        conflict = "neutral"
        decision_hint = direction if direction in {"bullish", "bearish"} else "neutral"
    elif status == "FAIL":
        available = True
        gate = "fail"
        conflict = "contradicts"
        # Deliberately do not infer bullish from a failed bearish rule.
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
        "direction": direction if status == "PASS" else "neutral",
        "strength": None,
        "available": available,
        "gate": gate,
        "conflict": conflict,
        "decision_hint": decision_hint,
        "confidence_delta": 0,
        "raw_evaluator_result": dict(result),
    }
