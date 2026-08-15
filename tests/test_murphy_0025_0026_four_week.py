from evaluators.murphy_0025_0026_four_week import evaluate_0025, evaluate_0026


def test_0025_pass_on_equal_high():
    x = evaluate_0025({"high": 1.4500, "four_week_high": 1.4500})
    assert x["status"] == "PASS"
    assert x["directional_confirmation"] == "BULLISH"


def test_0025_fail_below_reference():
    x = evaluate_0025({"high": 1.4499, "four_week_high": 1.4500})
    assert x["status"] == "FAIL"
    assert x["directional_confirmation"] == "NONE"


def test_0025_missing_reference():
    x = evaluate_0025({"high": 1.4500, "four_week_high": None})
    assert x["status"] == "NOT_EVALUABLE"


def test_0026_pass_on_equal_low():
    x = evaluate_0026({"low": 1.4000, "four_week_low": 1.4000})
    assert x["status"] == "PASS"
    assert x["directional_confirmation"] == "BEARISH"


def test_0026_fail_above_reference():
    x = evaluate_0026({"low": 1.4001, "four_week_low": 1.4000})
    assert x["status"] == "FAIL"
    assert x["directional_confirmation"] == "NONE"


def test_0026_missing_reference():
    x = evaluate_0026({"low": 1.4000, "four_week_low": None})
    assert x["status"] == "NOT_EVALUABLE"


def test_0025_does_not_use_close():
    x = evaluate_0025({"high": 1.4500, "close": 1.3900, "four_week_high": 1.4500})
    assert x["status"] == "PASS"


def test_0026_does_not_use_close():
    x = evaluate_0026({"low": 1.4000, "close": 1.4100, "four_week_low": 1.4000})
    assert x["status"] == "PASS"
