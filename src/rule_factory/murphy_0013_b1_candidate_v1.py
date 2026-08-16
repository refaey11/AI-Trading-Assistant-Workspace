"""Candidate B1 adapter for Murphy 0013 Symmetrical Triangle.

This module reuses the shared two-close confirmation mechanism as a candidate
policy only. It does not create a new geometry engine and does not import the
0008 Support semantics. Production freeze is intentionally out of scope.
"""
from typing import Any, Dict, Sequence


def evaluate_0013_b1_candidate(
    boundary: float | None,
    boundary_available: bool,
    closes: Sequence[float],
    direction: str,
) -> Dict[str, Any]:
    """Evaluate only the candidate two-close breakout state.

    `boundary` is the already-derived 0013 triangle boundary. The function
    accepts no tolerance, ATR, pip, percentage, or hidden lookback parameter.
    """
    if not boundary_available or boundary is None:
        return {"status": "NOT_EVALUABLE", "reason": "boundary_unavailable"}

    if direction not in {"UP", "DOWN"}:
        return {"status": "NOT_EVALUABLE", "reason": "invalid_break_direction"}

    if len(closes) == 0:
        return {"status": "NOT_EVALUABLE", "reason": "missing_completed_close"}

    def beyond(value: float) -> bool:
        return value > boundary if direction == "UP" else value < boundary

    if not beyond(closes[0]):
        return {"status": "NO_BREAK_CANDIDATE"}

    if len(closes) < 2:
        return {"status": "BREAK_CANDIDATE"}

    if beyond(closes[1]):
        return {
            "status": "DECISIVE_BREAK_CONFIRMED",
            "confirmation_index": 1,
        }

    return {"status": "NO_CONFIRMATION"}
