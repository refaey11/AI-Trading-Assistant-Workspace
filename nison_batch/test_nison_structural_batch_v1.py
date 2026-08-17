from nison_structural_batch_v1 import (
    Candle, evaluate_0021_three_mountains, evaluate_0023_three_buddha_tops,
    evaluate_0024_three_buddha_bottoms, evaluate_0034, evaluate_0038,
)


def c(i, o, h, l, cl):
    return Candle(str(i), o, h, l, cl)


def test_0034_equal_open_opposite_color_passes():
    r = evaluate_0034(c(1, 1.10, 1.11, 1.08, 1.09), c(2, 1.10, 1.14, 1.09, 1.13))
    assert r.status == "PASS"


def test_0034_non_equal_open_fails():
    r = evaluate_0034(c(1, 1.10, 1.11, 1.08, 1.09), c(2, 1.101, 1.14, 1.09, 1.13))
    assert r.status == "FAIL"


def test_0038_window_up_and_down():
    assert evaluate_0038(c(1, 1.10, 1.12, 1.09, 1.11), c(2, 1.13, 1.15, 1.125, 1.14)).status == "PASS"
    assert evaluate_0038(c(1, 1.10, 1.12, 1.09, 1.11), c(2, 1.08, 1.085, 1.05, 1.06)).status == "PASS"


def test_0021_requires_three_peaks():
    assert evaluate_0021_three_mountains([10, 11, 10.5]).status == "PASS"
    assert evaluate_0021_three_mountains([10, 11]).status == "NOT_EVALUABLE"


def test_0023_middle_peak_highest():
    assert evaluate_0023_three_buddha_tops([10, 12, 11]).status == "PASS"
    assert evaluate_0023_three_buddha_tops([10, 9, 11]).status == "FAIL"


def test_0024_middle_trough_lowest():
    assert evaluate_0024_three_buddha_bottoms([10, 8, 9]).status == "PASS"
    assert evaluate_0024_three_buddha_bottoms([10, 11, 9]).status == "FAIL"
