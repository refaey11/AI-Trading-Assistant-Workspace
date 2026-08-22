from murphy_0018_0019_evaluator import evaluate_0018, evaluate_0019


def test_0018_pass():
    r = evaluate_0018({"trendlines_converging": True, "upper_slope": -1.0, "lower_slope": -0.2})
    assert r["status"] == "PASS" and r["directional_confirmation"] == "BULLISH"


def test_0018_fail_wrong_slope():
    r = evaluate_0018({"trendlines_converging": True, "upper_slope": -1.0, "lower_slope": 0.2})
    assert r["status"] == "FAIL"


def test_0019_pass():
    r = evaluate_0019({"trendlines_converging": True, "upper_slope": 1.0, "lower_slope": 0.2})
    assert r["status"] == "PASS" and r["directional_confirmation"] == "BEARISH"


def test_0019_fail_wrong_slope():
    r = evaluate_0019({"trendlines_converging": True, "upper_slope": 1.0, "lower_slope": -0.2})
    assert r["status"] == "FAIL"


def test_missing_is_not_evaluable():
    assert evaluate_0018({"trendlines_converging": None, "upper_slope": -1.0, "lower_slope": -0.2})["status"] == "NOT_EVALUABLE"
    assert evaluate_0019({"trendlines_converging": True, "upper_slope": None, "lower_slope": 0.2})["status"] == "NOT_EVALUABLE"
