from nison_0001_0010_router import evaluate_rule

CASES = {
    "CANDLE_RULE_0001": {
        "candles": [
            {"open": 10.0, "high": 10.5, "low": 9.5, "close": 9.7},
            {"open": 9.6, "high": 11.0, "low": 9.5, "close": 10.8},
        ],
        "context": {"trend": "Downtrend"},
        "confirmation": {"break_above_engulfing_high": True},
    },
    "CANDLE_RULE_0002": {
        "candles": [
            {"open": 10.0, "high": 10.5, "low": 9.5, "close": 10.3},
            {"open": 10.4, "high": 10.5, "low": 9.0, "close": 9.2},
        ],
        "context": {"trend": "Uptrend"},
        "confirmation": {"break_below_engulfing_low": True},
    },
    "CANDLE_RULE_0003": {"candles": [{"open":10,"high":11,"low":9.8,"close":10.8,"color":"bullish","body_class":"long"},{"open":11.1,"high":11.2,"low":10,"close":10.2,"color":"bearish"}], "context": {"trend":"Uptrend", "confirmation":{"confirmed":True}}},
    "CANDLE_RULE_0004": {"candles": [{"open":10.8,"high":11,"low":9,"close":9.2,"color":"bearish","body_class":"long"},{"open":8.9,"high":10.3,"low":8.8,"close":10.2,"color":"bullish"}], "context": {"trend":"Downtrend", "confirmation":{"confirmed":True}}},
    "CANDLE_RULE_0005": {"candles": [{"open":10,"high":10.5,"low":9,"close":9.1,"color":"bearish","body_class":"long"},{"open":8.8,"high":9.5,"low":8.7,"close":9.12,"color":"bullish","close_relation":"near_previous_close"}], "context": {"trend":"Downtrend", "confirmation":{"confirmed":True}}},
    "CANDLE_RULE_0006": {"candles": [{"open":10,"high":10.5,"low":9,"close":9.1,"color":"bearish","body_class":"long"},{"open":8.8,"high":9.6,"low":8.7,"close":9.3,"color":"bullish","close_relation":"slightly_above_previous_close"}], "context": {"trend":"Downtrend", "confirmation":{"confirmed":True}}},
    "CANDLE_RULE_0007": {"candles": [{"open":10,"high":10.5,"low":9,"close":9.0,"color":"bearish","body_class":"long"},{"open":8.8,"high":9.8,"low":8.7,"close":9.4,"color":"bullish","close_relation":"well_into_body"}], "context": {"trend":"Downtrend", "confirmation":{"confirmed":True}}},
    "CANDLE_RULE_0008": {"candles": [{"open":10,"high":10.2,"low":8.5,"close":8.8,"color":"bearish","body_class":"long"},{"open":8.6,"high":8.9,"low":8.5,"close":8.7,"color":"bearish","body_class":"small"},{"open":8.7,"high":10.5,"low":8.6,"close":9.6,"color":"bullish","body_class":"strong"}], "context": {"trend":"Downtrend", "confirmation":{"confirmed":True}}},
    "CANDLE_RULE_0009": {"candles": [{"open":8.8,"high":10.2,"low":8.5,"close":10,"color":"bullish","body_class":"long"},{"open":10.1,"high":10.4,"low":9.9,"close":10.2,"color":"bullish","body_class":"small"},{"open":10.1,"high":10.2,"low":8.3,"close":9.2,"color":"bearish","body_class":"strong"}], "context": {"trend":"Uptrend", "confirmation":{"confirmed":True}}},
    "CANDLE_RULE_0010": {"candles": [{"open":10,"high":10.2,"low":8.5,"close":8.8,"color":"bearish","body_class":"long"},{"open":8.6,"high":8.8,"low":8.5,"close":8.65,"color":"doji"},{"open":8.7,"high":10.2,"low":8.6,"close":9.7,"color":"bullish","body_class":"strong"}], "context": {"trend":"Downtrend", "confirmation":{"confirmed":True}}},
}

for rule_id, payload in CASES.items():
    result = evaluate_rule(rule_id, payload)
    assert result["status"] == "PASS", (rule_id, result)

print("10/10 unified router PASS")
