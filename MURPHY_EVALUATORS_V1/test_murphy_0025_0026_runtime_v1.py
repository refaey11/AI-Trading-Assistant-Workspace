from MURPHY_EVALUATORS_V1.murphy_0025_0026_runtime_v1 import evaluate_0025, evaluate_0026


def test_0025_pass_fail_missing():
    assert evaluate_0025({"current_high": 101, "preceding_4w_high": 100})["status"] == "PASS"
    assert evaluate_0025({"current_high": 99, "preceding_4w_high": 100})["status"] == "FAIL"
    assert evaluate_0025({"current_high": 99})["status"] == "NOT_EVALUABLE"


def test_0026_pass_fail_missing():
    assert evaluate_0026({"current_low": 99, "preceding_4w_low": 100})["status"] == "PASS"
    assert evaluate_0026({"current_low": 101, "preceding_4w_low": 100})["status"] == "FAIL"
    assert evaluate_0026({"current_low": 101})["status"] == "NOT_EVALUABLE"
