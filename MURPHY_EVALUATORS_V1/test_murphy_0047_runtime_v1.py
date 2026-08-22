from MURPHY_EVALUATORS_V1.murphy_0047_runtime_v1 import evaluate_0047


def test_0047_pass_fail_missing():
    assert evaluate_0047({"index_new_high": True, "ad_fails_high": True})["status"] == "PASS"
    assert evaluate_0047({"index_new_high": True, "ad_fails_high": False})["status"] == "FAIL"
    assert evaluate_0047({"index_new_high": False, "ad_fails_high": True})["status"] == "FAIL"
    assert evaluate_0047({"index_new_high": None, "ad_fails_high": True})["status"] == "NOT_EVALUABLE"
