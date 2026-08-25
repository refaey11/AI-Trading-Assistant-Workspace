from murphy_0003_0004_runtime_v2 import evaluate_0003, evaluate_0004


def test_0003_both_higher_pass():
    r = evaluate_0003(1.30, 1.28, 1.27, 1.25)
    assert r["status"] == "PASS"
    assert r["peaks_higher"] and r["troughs_higher"]


def test_0003_peak_not_higher_fails():
    r = evaluate_0003(1.27, 1.28, 1.27, 1.25)
    assert r["status"] == "FAIL"
    assert not r["peaks_higher"] and r["troughs_higher"]


def test_0003_trough_not_higher_fails():
    r = evaluate_0003(1.30, 1.28, 1.24, 1.25)
    assert r["status"] == "FAIL"
    assert r["peaks_higher"] and not r["troughs_higher"]


def test_0004_both_lower_pass():
    r = evaluate_0004(1.27, 1.30, 1.22, 1.25)
    assert r["status"] == "PASS"
    assert r["peaks_lower"] and r["troughs_lower"]


def test_0004_peak_not_lower_fails():
    r = evaluate_0004(1.30, 1.28, 1.22, 1.25)
    assert r["status"] == "FAIL"
    assert not r["peaks_lower"] and r["troughs_lower"]


def test_0004_trough_not_lower_fails():
    r = evaluate_0004(1.27, 1.30, 1.26, 1.25)
    assert r["status"] == "FAIL"
    assert r["peaks_lower"] and not r["troughs_lower"]


def test_missing_input_is_not_evaluable():
    assert evaluate_0003(None, 1.2, 1.1, 1.0)["status"] == "NOT_EVALUABLE"
    assert evaluate_0004(1.2, 1.3, None, 1.1)["status"] == "NOT_EVALUABLE"
