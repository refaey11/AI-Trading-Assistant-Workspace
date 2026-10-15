from src.murphy_0013.breakout_window_v1 import evaluate_breakout_window


def base(**overrides):
    data = {
        "boundary_price": 100.0,
        "close_price": 101.0,
        "direction": "UP",
        "close_ts": 8.0,
        "apex_ts": 10.0,
        "boundary_available_ts": 5.0,
        "close_available_ts": 8.0,
        "evaluation_ts": 8.0,
    }
    data.update(overrides)
    return data


def test_completed_close_above_upper_before_apex_is_breakout():
    result = evaluate_breakout_window(**base())
    assert result["status"] == "BREAKOUT_OBSERVED"


def test_intraday_breach_without_close_outside_is_not_breakout():
    result = evaluate_breakout_window(**base(close_price=100.0))
    assert result["status"] == "NO_BREAKOUT"


def test_breakout_at_or_after_apex_is_not_confirmed():
    result = evaluate_breakout_window(**base(close_ts=10.0, close_available_ts=10.0, evaluation_ts=10.0))
    assert result["status"] == "NOT_CONFIRMED"


def test_missing_provenance_is_not_evaluable():
    result = evaluate_breakout_window(**base(close_available_ts=None))
    assert result["status"] == "NOT_EVALUABLE"


def test_future_close_is_not_evaluable():
    result = evaluate_breakout_window(**base(close_available_ts=9.0, evaluation_ts=8.0))
    assert result["status"] == "NOT_EVALUABLE"


def test_downside_breakout_uses_lower_boundary():
    result = evaluate_breakout_window(**base(boundary_price=100.0, close_price=99.0, direction="DOWN"))
    assert result["status"] == "BREAKOUT_OBSERVED"


def test_two_thirds_three_quarters_is_not_a_hard_gate():
    result = evaluate_breakout_window(**base(close_ts=9.5, close_available_ts=9.5, evaluation_ts=9.5))
    assert result["status"] == "BREAKOUT_OBSERVED"
    assert result["timing_context"] == "DESCRIPTIVE_2_3_TO_3_4_NOT_A_GATE"
