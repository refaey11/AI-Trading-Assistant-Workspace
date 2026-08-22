from nison_0001_0002_engulfing import Candle, evaluate_candle_rule_0001, evaluate_candle_rule_0002


def test_0001_pass_on_breakout_confirmation():
    candles = [Candle(10.0, 10.5, 9.5, 9.7), Candle(9.6, 11.0, 9.5, 10.8)]
    result = evaluate_candle_rule_0001(candles, "Downtrend", {"break_above_engulfing_high": True})
    assert result["status"] == "PASS"


def test_0001_requires_confirmation():
    candles = [Candle(10.0, 10.5, 9.5, 9.7), Candle(9.6, 11.0, 9.5, 10.8)]
    result = evaluate_candle_rule_0001(candles, "Downtrend", {})
    assert result["status"] == "FAIL"


def test_0001_rejects_wrong_trend():
    candles = [Candle(10.0, 10.5, 9.5, 9.7), Candle(9.6, 11.0, 9.5, 10.8)]
    result = evaluate_candle_rule_0001(candles, "Uptrend", {"break_above_engulfing_high": True})
    assert result["status"] == "FAIL"


def test_0002_pass_on_breakdown_confirmation():
    candles = [Candle(10.0, 10.5, 9.5, 10.3), Candle(10.4, 10.5, 9.0, 9.2)]
    result = evaluate_candle_rule_0002(candles, "Uptrend", {"break_below_engulfing_low": True})
    assert result["status"] == "PASS"


def test_0002_requires_confirmation():
    candles = [Candle(10.0, 10.5, 9.5, 10.3), Candle(10.4, 10.5, 9.0, 9.2)]
    result = evaluate_candle_rule_0002(candles, "Uptrend", {})
    assert result["status"] == "FAIL"


def test_no_lookahead_metadata_is_present():
    candles = [Candle(10.0, 10.5, 9.5, 9.7), Candle(9.6, 11.0, 9.5, 10.8)]
    result = evaluate_candle_rule_0001(candles, "Downtrend", {"break_above_engulfing_high": True})
    assert result["provenance"]["lookahead"] == "none"


if __name__ == "__main__":
    tests = [
        test_0001_pass_on_breakout_confirmation,
        test_0001_requires_confirmation,
        test_0001_rejects_wrong_trend,
        test_0002_pass_on_breakdown_confirmation,
        test_0002_requires_confirmation,
        test_no_lookahead_metadata_is_present,
    ]
    for test in tests:
        test()
    print("6/6 PASS")
