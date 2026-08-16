from src.rule_factory.pf_h1_horizontal_level_v1 import evaluate_pf_h1


def test_exact_horizontal_is_confirmed():
    assert evaluate_pf_h1({"slope": 0})["status"] == "CONFIRMED"


def test_nonzero_slope_is_not_confirmed():
    assert evaluate_pf_h1({"slope": 0.01})["status"] == "NOT_CONFIRMED"


def test_missing_slope_does_not_invent_tolerance():
    result = evaluate_pf_h1({})
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "horizontal_tolerance_not_defined"
