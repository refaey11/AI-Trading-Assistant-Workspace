"""Bridge Murphy 0006/0007 confirmations into the generic Decision Brain evidence shape.

This is an integration adapter only. It does not change Murphy semantics, create
thresholds, or decide a trade. The Murphy operator remains the sole evaluator of
third-touch/reaction/no-break for this module.
"""

from dataclasses import asdict
from typing import Any, Dict, Optional

from .murphy_event_operator import Confirmation


def confirmation_to_decision_evidence(
    confirmation: Optional[Confirmation],
    *,
    gate: str = "pass",
    conflict: str = "supports",
) -> Dict[str, Any]:
    """Normalize an already-evaluated Murphy confirmation for the Brain.

    ``None`` is represented as unavailable evidence; it is never converted into
    a directional signal. A confirmed 0006 is bullish context and 0007 bearish
    context. Strength is deliberately bounded and conservative; the Decision
    Brain remains responsible for final synthesis and confidence.
    """
    if confirmation is None:
        return {
            "module": "murphy_context",
            "source_rule_id": "MURPHY_0006_0007",
            "statement": "Murphy 0006/0007 confirmation unavailable",
            "direction": "neutral",
            "strength": 0.0,
            "available": False,
            "gate": "needs_review",
            "conflict": "insufficient",
            "decision_hint": "neutral",
            "confidence_delta": 0.0,
        }

    if confirmation.rule_id == "MURPHY_0006":
        direction = "bullish"
        statement = "Murphy 0006 confirmed: reaction-low up trendline with third touch and reaction"
    elif confirmation.rule_id == "MURPHY_0007":
        direction = "bearish"
        statement = "Murphy 0007 confirmed: reaction-high down trendline with third touch and reaction"
    else:
        raise ValueError(f"unsupported Murphy confirmation: {confirmation.rule_id}")

    return {
        "module": "murphy_context",
        "source_rule_id": confirmation.rule_id,
        "statement": statement,
        "direction": direction,
        "strength": 0.45,
        "available": True,
        "gate": gate,
        "conflict": conflict,
        "decision_hint": direction,
        "confidence_delta": 0.0,
        "confirmation_available_at": confirmation.confirmation_available_at.isoformat(),
        "third_touch_timestamp": confirmation.third_touch.timestamp.isoformat(),
        "reaction_timestamp": confirmation.reaction.timestamp.isoformat(),
    }


def adapt_confirmation(confirmation: Confirmation) -> Dict[str, Any]:
    """Alias used by the production-path smoke test."""
    return confirmation_to_decision_evidence(confirmation)
