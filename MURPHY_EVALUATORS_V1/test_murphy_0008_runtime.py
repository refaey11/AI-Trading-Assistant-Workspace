from murphy_0008_runtime import evaluate_0008


def test_0008_passes_ordered_role_reversal():
    r = evaluate_0008({"direction":"UPSIDE","level_price":1.28,"breakout_timestamp":"2020-01-02T00:00:00","retest_timestamp":"2020-02-07T22:00:00","role_reversal_timestamp":"2020-02-10T04:00:00"})
    assert r["status"] == "PASS"
    assert r["directional_confirmation"] == "BEARISH"


def test_0008_rejects_bad_order():
    r = evaluate_0008({"direction":"DOWNSIDE","level_price":1.28,"breakout_timestamp":"2020-01-02T00:00:00","retest_timestamp":"2019-12-07T22:00:00","role_reversal_timestamp":"2020-02-10T04:00:00"})
    assert r["status"] == "NOT_EVALUABLE"


def test_0008_missing_evidence():
    r = evaluate_0008({"direction":"UPSIDE","level_price":1.28,"breakout_timestamp":"2020-01-02T00:00:00"})
    assert r["status"] == "NOT_EVALUABLE"
