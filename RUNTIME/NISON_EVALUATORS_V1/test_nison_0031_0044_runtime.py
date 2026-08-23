from nison_0031_0044_runtime import evaluate_rule

PATTERN_RULES = [f"CANDLE_RULE_{i:04d}" for i in range(31, 39)]
MODULE_RULES = [f"NISON_MODULE_{i:04d}" for i in range(39, 45)]


def test_fail_closed_without_upstream_evidence():
    for rid in PATTERN_RULES:
        out = evaluate_rule(rid, {"context": {}})
        assert out["status"] == "NOT_EVALUABLE", (rid, out)


def test_0031_three_falling_methods():
    payload = {
        "candles": [
            {"open": 20, "high": 21, "low": 14, "close": 15, "color": "bearish", "body_class": "long"},
            {"open": 15, "high": 18, "low": 14.8, "close": 17, "color": "bullish", "body_class": "small"},
            {"open": 17, "high": 18.5, "low": 15.5, "close": 17.5, "color": "bullish", "body_class": "small"},
            {"open": 17.4, "high": 18.2, "low": 16, "close": 17, "color": "bearish", "body_class": "small"},
            {"open": 16.8, "high": 17, "low": 12, "close": 13, "color": "bearish", "body_class": "long"},
        ],
        "context": {"trend": "Downtrend", "confirmation": {"confirmed": True}},
    }
    out = evaluate_rule("CANDLE_RULE_0031", payload)
    assert out["status"] == "PASS", out


def test_0032_three_white_soldiers_requires_categorical_near_facts():
    payload = {
        "candles": [
            {"open": 10, "high": 12, "low": 9.8, "close": 11.8, "color": "bullish", "body_class": "long", "close_at_high": True},
            {"open": 11.3, "high": 13.2, "low": 11.1, "close": 13.0, "color": "bullish", "body_class": "long", "close_at_high": True, "open_within_or_near_previous_body": True},
            {"open": 12.5, "high": 14.4, "low": 12.3, "close": 14.2, "color": "bullish", "body_class": "long", "close_at_high": True, "open_within_or_near_previous_body": True},
        ],
        "context": {"confirmation": {"confirmed": True}},
    }
    out = evaluate_rule("CANDLE_RULE_0032", payload)
    assert out["status"] == "PASS", out


def test_0033_advance_block_requires_upstream_qualitative_fact():
    payload = {
        "candles": [
            {"open": 10, "high": 14, "low": 9.5, "close": 13.5, "color": "bullish", "body_class": "long"},
            {"open": 13, "high": 15, "low": 12.7, "close": 14.8, "color": "bullish", "body_class": "long"},
            {"open": 14.9, "high": 16, "low": 14.4, "close": 15.2, "color": "bullish", "body_class": "small", "noticeably_smaller_than_previous": True, "is_star_above_previous": True},
        ],
        "context": {"confirmation": {"confirmed": True}},
    }
    out = evaluate_rule("CANDLE_RULE_0033", payload)
    assert out["status"] == "PASS", out


def test_0034_separating_lines_exact_open():
    payload = {
        "candles": [
            {"open": 20, "high": 21, "low": 18, "close": 19, "color": "bearish"},
            {"open": 20, "high": 22, "low": 19.5, "close": 21.5, "color": "bullish"},
        ],
        "context": {"trend": "Uptrend", "confirmation": {"confirmed": True}},
    }
    out = evaluate_rule("CANDLE_RULE_0034", payload)
    assert out["status"] == "PASS", out


def test_0035_tasuki_gap_uses_window_facts():
    payload = {
        "candles": [
            {"open": 10, "high": 11, "low": 9.5, "close": 10.8, "color": "bullish"},
            {"open": 11.2, "high": 12, "low": 11.1, "close": 11.8, "color": "bullish", "gap_class": "gap_above_previous_high"},
            {"open": 11.7, "high": 11.9, "low": 10.9, "close": 11.3, "color": "bearish", "open_inside_previous_body": True, "close_inside_window": True, "window_closed": False},
        ],
        "context": {"trend": "Uptrend", "confirmation": {"confirmed": True}},
    }
    out = evaluate_rule("CANDLE_RULE_0035", payload)
    assert out["status"] == "PASS", out


def test_0036_gapping_play_uses_upstream_window_hold():
    payload = {"context": {
        "trend": "Uptrend",
        "window_formed": True,
        "window_closed": False,
        "window_held_as_support_or_resistance": True,
        "trend_resumed": True,
        "confirmation": {"confirmed": True},
    }}
    out = evaluate_rule("CANDLE_RULE_0036", payload)
    assert out["status"] == "PASS", out


def test_0037_side_by_side_requires_qualitative_similarity_facts():
    payload = {"candles": [
        {"open": 12.0, "high": 13.0, "low": 11.8, "close": 12.9, "color": "bullish", "opens_at_approximately_same_price_as_previous": True, "body_similar_to_previous": True},
        {"open": 12.1, "high": 13.1, "low": 11.9, "close": 13.0, "color": "bullish", "opens_at_approximately_same_price_as_previous": True, "body_similar_to_previous": True},
    ], "context": {
        "trend": "Uptrend", "window_formed": True, "window_closed": False,
        "confirmation": {"confirmed": True},
    }}
    out = evaluate_rule("CANDLE_RULE_0037", payload)
    assert out["status"] == "PASS", out


def test_0038_window_geometry_does_not_use_future_bars():
    out = evaluate_rule("CANDLE_RULE_0038", {"context": {
        "previous_session": {"high": 10.0, "low": 9.0},
        "current_session": {"high": 12.0, "low": 10.5},
        "direction": "bullish",
    }})
    assert out["status"] == "PASS"
    assert out["provenance"]["lookahead"] == "none"


def test_confirmation_required_for_0031_0037():
    payload = {
        "candles": [
            {"open": 20, "high": 21, "low": 14, "close": 15, "color": "bearish", "body_class": "long"},
            {"open": 15, "high": 18, "low": 14.8, "close": 17, "color": "bullish", "body_class": "small"},
            {"open": 17, "high": 18.5, "low": 15.5, "close": 17.5, "color": "bullish", "body_class": "small"},
            {"open": 17.4, "high": 18.2, "low": 16, "close": 17, "color": "bearish", "body_class": "small"},
            {"open": 16.8, "high": 17, "low": 12, "close": 13, "color": "bearish", "body_class": "long"},
        ],
        "context": {"trend": "Downtrend", "confirmation": {"confirmed": False}},
    }
    out = evaluate_rule("CANDLE_RULE_0031", payload)
    assert out["status"] == "FAIL", out
    assert "confirmation" in out["reason"].lower()


def test_methodology_modules_are_context_only():
    for rid in MODULE_RULES:
        out = evaluate_rule(rid, {"context": {"evidence_available": True, "role": "context", "confirmation": {"confirmed": True}}})
        assert out["status"] == "PASS", (rid, out)
        assert out["provenance"]["standalone_direction"] is False


def test_methodology_modules_fail_closed_when_missing():
    for rid in MODULE_RULES:
        out = evaluate_rule(rid, {"context": {}})
        assert out["status"] == "NOT_EVALUABLE", (rid, out)
