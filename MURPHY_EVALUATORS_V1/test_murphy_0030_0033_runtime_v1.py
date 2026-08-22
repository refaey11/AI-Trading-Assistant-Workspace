from MURPHY_EVALUATORS_V1.murphy_0030_0032_runtime_v1 import evaluate_0030, evaluate_0031, evaluate_0032
from MURPHY_EVALUATORS_V1.murphy_0033_runtime_v1 import evaluate_0033


def sample_columns():
    return [
        {"kind": "X", "boxes": [99, 100, 101], "bottom": 99, "top": 101},
        {"kind": "O", "boxes": [98, 97, 96], "bottom": 96, "top": 98},
        {"kind": "X", "boxes": [97, 98, 99, 100, 101], "bottom": 97, "top": 101},
    ]


def test_0030_support_reference():
    r = evaluate_0030({"columns": sample_columns()})
    assert r["status"] == "PASS"
    assert r["reference_column_index"] == 1 or r["origin_column_index"] == 1


def test_0031_long_stop_reference():
    r = evaluate_0031({"columns": sample_columns()})
    assert r["status"] == "PASS"
    assert r["placement_relation"] == "BELOW"


def test_0032_short_stop_reference():
    r = evaluate_0032({"columns": sample_columns()})
    assert r["status"] == "PASS"
    assert r["placement_relation"] == "ABOVE"


def test_0030_0032_missing_not_evaluable():
    assert evaluate_0030({})["status"] == "NOT_EVALUABLE"
    assert evaluate_0031({"columns": []})["status"] == "NOT_EVALUABLE"
    assert evaluate_0032({"columns": []})["status"] == "NOT_EVALUABLE"


def test_0033_confirmed_context():
    r = evaluate_0033({
        "reversal_candle": True,
        "short_term_trend": "DOWN",
        "oscillator_d": 15,
        "candle_direction": "BULLISH",
    })
    assert r["status"] == "CONFIRMED"
    assert r["directional_confirmation"] == "NEUTRAL"


def test_0033_missing_is_not_evaluable():
    assert evaluate_0033({"reversal_candle": True})["status"] == "NOT_EVALUABLE"
