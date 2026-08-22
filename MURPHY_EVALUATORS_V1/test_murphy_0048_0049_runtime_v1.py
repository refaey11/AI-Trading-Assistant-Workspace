from MURPHY_EVALUATORS_V1.murphy_0048_0049_runtime_v1 import evaluate_0048, evaluate_0049


def test_0048_pass_fail_not_evaluable():
    assert evaluate_0048({"trin_ma10": 1.21})["status"] == "PASS"
    assert evaluate_0048({"trin_ma10": 1.20})["status"] == "FAIL"
    assert evaluate_0048({})["status"] == "NOT_EVALUABLE"


def test_0049_pass_fail_not_evaluable():
    assert evaluate_0049({"trin": 0.69})["status"] == "PASS"
    assert evaluate_0049({"trin": 0.70})["status"] == "FAIL"
    assert evaluate_0049({})["status"] == "NOT_EVALUABLE"


def test_operators_are_source_bounded():
    assert evaluate_0048({"trin_ma10": 1.30})["operator"] == "trin_ma10 > 1.20"
    assert evaluate_0049({"trin": 0.60})["operator"] == "trin < 0.70"
