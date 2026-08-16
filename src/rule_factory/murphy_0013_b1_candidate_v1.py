"""Candidate B1 adapter for Murphy 0013 Symmetrical Triangle.

This module reuses the shared two-close confirmation mechanism as a candidate
policy only. It does not create a new geometry engine and does not import the
0008 Support semantics. Production freeze is intentionally out of scope.
"""
from datetime import datetime
from typing import Any, Dict, Sequence


def _parse_time(value: Any):
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def evaluate_0013_b1_candidate(
    boundary: float | None,
    boundary_available: bool,
    closes: Sequence[float],
    direction: str,
    close_available_timestamps: Sequence[Any] | None = None,
    decision_time: Any | None = None,
) -> Dict[str, Any]:
    """Evaluate the candidate two-close breakout state with chronology gating.

    The first two closes must be completed and available no later than the
    decision timestamp. Missing or future timestamps fail closed.
    """
    if not boundary_available or boundary is None:
        return {"status": "NOT_EVALUABLE", "reason": "boundary_unavailable"}

    if direction not in {"UP", "DOWN"}:
        return {"status": "NOT_EVALUABLE", "reason": "invalid_break_direction"}

    if len(closes) == 0:
        return {"status": "NOT_EVALUABLE", "reason": "missing_completed_close"}

    if close_available_timestamps is None or decision_time is None:
        return {"status": "NOT_EVALUABLE", "reason": "missing_close_provenance"}

    decision = _parse_time(decision_time)
    if decision is None or len(close_available_timestamps) < min(2, len(closes)):
        return {"status": "NOT_EVALUABLE", "reason": "invalid_close_provenance"}

    parsed = [_parse_time(t) for t in close_available_timestamps[:len(closes)]]
    if any(t is None for t in parsed):
        return {"status": "NOT_EVALUABLE", "reason": "invalid_close_timestamp"}
    if any(t > decision for t in parsed[:2]):
        return {"status": "NOT_EVALUABLE", "reason": "close_not_available_at_decision_time"}
    if parsed[1] < parsed[0] if len(parsed) >= 2 else False:
        return {"status": "NOT_EVALUABLE", "reason": "close_chronology_violation"}

    def beyond(value: float) -> bool:
        return value > boundary if direction == "UP" else value < boundary

    if not beyond(closes[0]):
        return {"status": "NO_BREAK_CANDIDATE"}

    if len(closes) < 2:
        return {"status": "BREAK_CANDIDATE"}

    if beyond(closes[1]):
        return {"status": "DECISIVE_BREAK_CONFIRMED", "confirmation_index": 1}

    return {"status": "NO_CONFIRMATION"}
