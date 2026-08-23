from nison_0001_0010_router import evaluate_rule


def test_router_0031_0044():
    cases = {
        "CANDLE_RULE_0031": {
            "candles": [
                {"open": 20, "high": 21, "low": 14, "close": 15, "color": "bearish", "body_class": "long"},
                {"open": 15, "high": 18, "low": 14.8, "close": 17, "color": "bullish", "body_class": "small"},
                {"open": 17, "high": 18.5, "low": 15.5, "close": 17.5, "color": "bullish", "body_class": "small"},
                {"open": 17.4, "high": 18.2, "low": 16, "close": 17, "color": "bearish", "body_class": "small"},
                {"open": 16.8, "high": 17, "low": 12, "close": 13, "color": "bearish", "body_class": "long"},
            ],
            "context": {"trend": "Downtrend", "confirmation": {"confirmed": True}},
        },
        "CANDLE_RULE_0032": {
            "candles": [
                {"open": 10, "high": 12, "low": 9.8, "close": 11.8, "color": "bullish", "body_class": "long", "close_at_high": True},
                {"open": 11.3, "high": 13.2, "low": 11.1, "close": 13.0, "color": "bullish", "body_class": "long", "close_at_high": True, "open_within_or_near_previous_body": True},
                {"open": 12.5, "high": 14.4, "low": 12.3, "close": 14.2, "color": "bullish", "body_class": "long", "close_at_high": True, "open_within_or_near_previous_body": True},
            ],
            "context": {"confirmation": {"confirmed": True}},
        },
        "CANDLE_RULE_0033": {
            "candles": [
                {"open": 10, "high": 14, "low": 9.5, "close": 13.5, "color": "bullish", "body_class": "long"},
                {"open": 13, "high": 15, "low": 12.7, "close": 14.8, "color": "bullish", "body_class": "long"},
                {"open": 14.9, "high": 16, "low": 14.4, "close": 15.2, "color": "bullish", "body_class": "small", "noticeably_smaller_than_previous": True, "is_star_above_previous": True},
            ],
            "context": {"confirmation": {"confirmed": True}},
        },
        "CANDLE_RULE_0034": {
            "candles": [
                {"open": 20, "high": 21, "low": 18, "close": 19, "color": "bearish"},
                {"open": 20, "high": 22, "low": 19.5, "close": 21.5, "color": "bullish"},
            ],
            "context": {"trend": "Uptrend", "confirmation": {"confirmed": True}},
        },
        "CANDLE_RULE_0035": {
            "candles": [
                {"open": 10, "high": 11, "low": 9.5, "close": 10.8, "color": "bullish"},
                {"open": 11.2, "high": 12, "low": 11.1, "close": 11.8, "color": "bullish", "gap_class": "gap_above_previous_high"},
                {"open": 11.7, "high": 11.9, "low": 10.9, "close": 11.3, "color": "bearish", "open_inside_previous_body": True, "close_inside_window": True, "window_closed": False},
            ],
            "context": {"trend": "Uptrend", "confirmation": {"confirmed": True}},
        },
        "CANDLE_RULE_0036": {
            "context": {
                "trend": "Uptrend",
                "window_formed": True,
                "window_closed": False,
                "window_held_as_support_or_resistance": True,
                "trend_resumed": True,
                "confirmation": {"confirmed": True},
            }
        },
        "CANDLE_RULE_0037": {
            "candles": [
                {"open": 12.0, "high": 13.0, "low": 11.8, "close": 12.9, "color": "bullish", "opens_at_approximately_same_price_as_previous": True, "body_similar_to_previous": True},
                {"open": 12.1, "high": 13.1, "low": 11.9, "close": 13.0, "color": "bullish", "opens_at_approximately_same_price_as_previous": True, "body_similar_to_previous": True},
            ],
            "context": {"trend": "Uptrend", "window_formed": True, "window_closed": False, "confirmation": {"confirmed": True}},
        },
    }

    for rid, payload in cases.items():
        out = evaluate_rule(rid, payload)
        assert out["status"] == "PASS", (rid, out)

    out = evaluate_rule("CANDLE_RULE_0038", {"context": {
        "previous_session": {"high": 10.0, "low": 9.0},
        "current_session": {"high": 12.0, "low": 10.5},
        "direction": "bullish",
    }})
    assert out["status"] == "PASS", ("CANDLE_RULE_0038", out)

    for i in range(39, 45):
        rid = f"NISON_MODULE_{i:04d}"
        out = evaluate_rule(rid, {"context": {"evidence_available": True, "role": "context", "confirmation": {"confirmed": True}}})
        assert out["status"] == "PASS", (rid, out)
        assert out["provenance"]["standalone_direction"] is False


if __name__ == "__main__":
    test_router_0031_0044()
    print("Nison router smoke 0031-0044: PASS")
