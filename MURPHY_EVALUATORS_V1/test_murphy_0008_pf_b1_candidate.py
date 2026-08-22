from murphy_0008_pf_b1_candidate import evaluate_0008_candidate


def base():
    return {
        "role": "SUPPORT",
        "breakout_timestamp": "2020-01-02 00:00:00",
        "breakout_close": 1.20,
        "level_price": 1.21,
        "level_available_at": "2019-12-30 00:00:00",
        "direction": "DOWNSIDE",
    }


def test_missing_retest_is_not_evaluable():
    r = evaluate_0008_candidate(base())
    assert r["status"] == "NOT_EVALUABLE"
    assert r["stage"] == "BREAKOUT_CONFIRMED_RETEST_MISSING"


def test_non_support_fails():
    r = evaluate_0008_candidate({**base(), "role": "RESISTANCE"})
    assert r["status"] == "FAIL"


def test_wrong_direction_fails():
    r = evaluate_0008_candidate({**base(), "direction": "UPSIDE"})
    assert r["status"] == "FAIL"


def test_role_reversal_passes_when_downside_break_and_retest_are_confirmed():
    r = evaluate_0008_candidate({**base(), "retest_confirmed": True, "role_reversal_confirmed": True})
    assert r["status"] == "PASS"
    assert r["directional_confirmation"] == "BEARISH"


def test_role_reversal_fails_when_retest_not_confirmed():
    r = evaluate_0008_candidate({**base(), "retest_confirmed": False, "role_reversal_confirmed": True})
    assert r["status"] == "FAIL"
