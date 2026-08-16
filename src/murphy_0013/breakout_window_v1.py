"""Source-bounded Murphy 0013 breakout-window proposal.

The operator treats a completed close beyond a canonical triangle boundary
before the canonical apex as the observable breakout event. The commonly
quoted two-thirds-to-three-quarters timing guidance is metadata, not a hard
numeric gate.
"""


def evaluate_breakout_window(
    *,
    boundary_price: float | None,
    close_price: float | None,
    direction: str,
    close_ts: float | None,
    apex_ts: float | None,
    boundary_available_ts: float | None,
    close_available_ts: float | None,
    evaluation_ts: float | None,
) -> dict:
    required = (
        boundary_price,
        close_price,
        close_ts,
        apex_ts,
        boundary_available_ts,
        close_available_ts,
        evaluation_ts,
    )
    if any(value is None for value in required):
        return {"status": "NOT_EVALUABLE"}
    if direction not in {"UP", "DOWN"}:
        return {"status": "NOT_EVALUABLE"}
    if boundary_available_ts > evaluation_ts or close_available_ts > evaluation_ts:
        return {"status": "NOT_EVALUABLE"}
    if close_available_ts > close_ts:
        return {"status": "NOT_EVALUABLE"}
    if close_ts <= boundary_available_ts:
        return {"status": "NOT_EVALUABLE"}
    if close_ts >= apex_ts:
        return {"status": "NOT_CONFIRMED", "reason": "after_or_at_apex"}

    beyond = (
        close_price > boundary_price if direction == "UP"
        else close_price < boundary_price
    )
    if not beyond:
        return {"status": "NO_BREAKOUT"}

    return {
        "status": "BREAKOUT_OBSERVED",
        "breakout_timestamp": close_ts,
        "availability_timestamp": close_available_ts,
        "timing_context": "DESCRIPTIVE_2_3_TO_3_4_NOT_A_GATE",
    }
