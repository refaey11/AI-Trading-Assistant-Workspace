from evaluator_candidate_v1 import Input, evaluate

def test_bullish_reversal_downtrend_oversold():
    assert evaluate(Input(True, "DOWN", 15, "BULLISH")).state == "CONFIRMED"

def test_bearish_reversal_uptrend_overbought():
    assert evaluate(Input(True, "UP", 85, "BEARISH")).state == "CONFIRMED"

def test_mid_zone_conflicts():
    assert evaluate(Input(True, "DOWN", 65, "BULLISH")).state == "CONFLICT"

def test_missing_context_not_evaluable():
    assert evaluate(Input(True, None, 15, "BULLISH")).state == "NOT_EVALUABLE"

def test_non_reversal_not_eligible():
    assert evaluate(Input(False, "DOWN", 15, "BULLISH")).state == "CONFLICT"

def test_wrong_context_conflicts():
    assert evaluate(Input(True, "UP", 15, "BULLISH")).state == "CONFLICT"

def test_invalid_stochastic_not_evaluable():
    assert evaluate(Input(True, "DOWN", 120, "BULLISH")).state == "NOT_EVALUABLE"

def test_future_row_does_not_change_prior_result():
    prior = Input(True, "DOWN", 15, "BULLISH")
    before = evaluate(prior)
    _ = evaluate(Input(True, "UP", 85, "BEARISH"))
    assert before == evaluate(prior)

def test_direction_is_always_neutral():
    assert evaluate(Input(True, "DOWN", 15, "BULLISH")).direction == "NEUTRAL"
