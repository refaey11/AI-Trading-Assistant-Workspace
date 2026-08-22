from murphy_0008_role_reversal_candidate import evaluate_0008_candidate


def test_candidate_pass():
    r = evaluate_0008_candidate({
        'role':'SUPPORT','direction':'DOWNSIDE',
        'breakout_timestamp':'2020-03-13 16:00:00',
        'retest_timestamp':'2020-03-13 17:00:00',
        'role_reversal_timestamp':'2020-03-13 19:00:00',
        'level_price':1.24667,
    })
    assert r['status'] == 'CANDIDATE_PASS'
    assert r['directional_confirmation'] == 'BEARISH'


def test_wrong_role_fails():
    r = evaluate_0008_candidate({
        'role':'RESISTANCE','direction':'UPSIDE',
        'breakout_timestamp':'2020-03-13 16:00:00',
        'retest_timestamp':'2020-03-13 17:00:00',
        'role_reversal_timestamp':'2020-03-13 19:00:00',
        'level_price':1.24667,
    })
    assert r['status'] == 'FAIL'


def test_missing_retest_not_evaluable():
    r = evaluate_0008_candidate({
        'role':'SUPPORT','direction':'DOWNSIDE',
        'breakout_timestamp':'2020-03-13 16:00:00',
        'retest_timestamp':None,
        'role_reversal_timestamp':None,
        'level_price':1.24667,
    })
    assert r['status'] == 'NOT_EVALUABLE'


def test_invalid_chronology_not_evaluable():
    r = evaluate_0008_candidate({
        'role':'SUPPORT','direction':'DOWNSIDE',
        'breakout_timestamp':'2020-03-13 16:00:00',
        'retest_timestamp':'2020-03-13 15:00:00',
        'role_reversal_timestamp':'2020-03-13 19:00:00',
        'level_price':1.24667,
    })
    assert r['status'] == 'NOT_EVALUABLE'
