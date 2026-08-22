from murphy_0008_runtime import evaluate_0008


def test_0008_fails_closed_until_approved_break_definition():
    r = evaluate_0008({
        "direction": "UPSIDE",
        "level_price": 1.28,
        "breakout_timestamp": "2020-01-02T00:00:00",
        "retest_timestamp": "2020-02-07T22:00:00",
        "role_reversal_timestamp": "2020-02-10T04:00:00",
    })
    assert r["status"] == "NOT_EVALUABLE"
    assert r["directional_confirmation"] == "UNKNOWN"


def test_0008_does_not_infer_downside_mapping():
    r = evaluate_0008({
        "direction": "DOWNSIDE",
        "level_price": 1.28,
        "breakout_timestamp": "2020-01-02T00:00:00",
        "retest_timestamp": "2020-02-07T22:00:00",
        "role_reversal_timestamp": "2020-02-10T04:00:00",
    })
    assert r["status"] == "NOT_EVALUABLE"


if __name__ == '__main__':
    test_0008_fails_closed_until_approved_break_definition()
    test_0008_does_not_infer_downside_mapping()
    print('0008: FAIL-CLOSED 2/2')
