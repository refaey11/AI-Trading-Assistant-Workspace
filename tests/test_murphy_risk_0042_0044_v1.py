from src.murphy_risk.risk_rule_evaluator_0042_0044_v1 import (
    evaluate_0042, evaluate_0043, evaluate_0044
)


def test_0042_upper_bound_pass():
    assert evaluate_0042(50.0) == "PASS"


def test_0042_upper_bound_fail():
    assert evaluate_0042(50.01) == "FAIL"


def test_0043_range_pass():
    assert evaluate_0043(10.0) == "PASS"
    assert evaluate_0043(15.0) == "PASS"


def test_0043_upper_bound_fail():
    assert evaluate_0043(15.01) == "FAIL"


def test_0043_below_guideline_not_violation():
    assert evaluate_0043(9.99) == "NOT_EVALUABLE"


def test_0044_upper_bound_pass():
    assert evaluate_0044(5.0) == "PASS"


def test_0044_upper_bound_fail():
    assert evaluate_0044(5.01) == "FAIL"


def test_missing_evidence_is_not_evaluable():
    assert evaluate_0042(None) == "NOT_EVALUABLE"
    assert evaluate_0043(None) == "NOT_EVALUABLE"
    assert evaluate_0044(None) == "NOT_EVALUABLE"
