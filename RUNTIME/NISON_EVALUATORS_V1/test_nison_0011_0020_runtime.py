from nison_0011_0020_runtime import evaluate_rule

CASES = {
"CANDLE_RULE_0011":{"candles":[{"open":10,"high":11,"low":9.8,"close":10.9,"color":"bullish","body_class":"long"},{"open":11.1,"high":11.2,"low":11.0,"close":11.1,"color":"doji","doji_isolated":True},{"open":11.0,"high":11.1,"low":9.0,"close":9.3,"color":"bearish","body_class":"strong"}],"context":{"trend":"Uptrend","confirmation":{"confirmed":True}}},
"CANDLE_RULE_0012":{"candles":[{"open":10,"high":10.2,"low":8.5,"close":8.8,"color":"bearish","body_class":"long"},{"open":8.6,"high":8.7,"low":8.5,"close":8.6,"color":"doji","gap_class":"gap_below_first","doji_isolated":True},{"open":8.9,"high":10.0,"low":8.8,"close":9.7,"color":"bullish","body_class":"strong","gap_class":"gap_above_doji"}],"context":{"trend":"Downtrend","confirmation":{"confirmed":True}}},
"CANDLE_RULE_0013":{"candles":[{"open":10,"high":11,"low":9,"close":11,"body_class":"long","color":"bullish"},{"open":10.5,"high":10.7,"low":10.3,"close":10.5,"body_class":"small","color":"bearish","open_inside_previous_body":True}],"context":{"trend":"Uptrend","confirmation":{"confirmed":True}}},
"CANDLE_RULE_0014":{"candles":[{"open":10,"high":11,"low":9,"close":11,"body_class":"long","color":"bullish"},{"open":10.5,"high":10.8,"low":10.2,"close":10.5,"color":"doji","open_inside_previous_body":True}],"context":{"trend":"Uptrend"}},
"CANDLE_RULE_0015":{"candles":[{"open":10,"high":11,"low":9,"close":10.5,"equal_extreme":True},{"open":10.5,"high":11,"low":10,"close":10.8,"equal_extreme":True}],"context":{"trend":"Uptrend","confirmation":{"confirmed":True}}},
"CANDLE_RULE_0016":{"candles":[{"open":10,"high":11,"low":9,"close":9.5,"equal_extreme":True},{"open":9.5,"high":10,"low":9,"close":9.8,"equal_extreme":True}],"context":{"trend":"Downtrend","confirmation":{"confirmed":True}}},
"CANDLE_RULE_0017":{"candles":[{"open":10,"high":11,"low":9.8,"close":10.9,"color":"bullish","body_class":"long"},{"open":11.2,"high":11.5,"low":10.8,"close":11.0,"color":"bearish","gap_class":"gap_above_first"},{"open":11.0,"high":11.2,"low":10.5,"close":10.8,"color":"bearish","gap_class":"inside_gap_area"}],"context":{"trend":"Uptrend","confirmation":{"confirmed":True}}},
"CANDLE_RULE_0018":{"candles":[{"open":10,"high":10.1,"low":8.8,"close":9.0,"color":"bearish","body_class":"long","close_near_low":True},{"open":9.5,"high":9.7,"low":8.5,"close":8.7,"color":"bearish","open_inside_previous_body":True,"close_near_low":True},{"open":9.1,"high":9.3,"low":8.2,"close":8.4,"color":"bearish","open_inside_previous_body":True,"close_near_low":True}],"context":{"trend":"Uptrend"}},
"CANDLE_RULE_0019":{"candles":[{"open":10,"high":10.2,"low":8.8,"close":9.0,"color":"bearish","body_class":"long"},{"open":8.7,"high":9.5,"low":8.6,"close":9.0,"color":"bullish","gap_class":"gap_below_previous_close","close_relation":"approximately_equal_previous_close"}],"context":{"trend":"Downtrend"}},
"CANDLE_RULE_0020":{"candles":[{"open":9.0,"high":10.2,"low":8.8,"close":10.0,"color":"bullish","body_class":"long"},{"open":10.3,"high":10.4,"low":9.2,"close":10.0,"color":"bearish","gap_class":"gap_above_previous_close","close_relation":"approximately_equal_previous_close"}],"context":{"trend":"Uptrend"}},
}

def test_positive():
    for rid,payload in CASES.items():
        out=evaluate_rule(rid,payload)
        assert out["status"]=="PASS",(rid,out)

def test_confirmation_required():
    required={"CANDLE_RULE_0011","CANDLE_RULE_0012","CANDLE_RULE_0013","CANDLE_RULE_0015","CANDLE_RULE_0016","CANDLE_RULE_0017"}
    for rid in required:
        payload=CASES[rid]
        p={**payload,"context":{k:v for k,v in payload["context"].items() if k!="confirmation"}}
        out=evaluate_rule(rid,p)
        assert out["status"]=="FAIL",(rid,out)

def test_trend_rejection():
    required={"CANDLE_RULE_0011":"Downtrend","CANDLE_RULE_0015":"Downtrend","CANDLE_RULE_0016":"Uptrend","CANDLE_RULE_0017":"Downtrend","CANDLE_RULE_0018":"Downtrend","CANDLE_RULE_0019":"Uptrend","CANDLE_RULE_0020":"Downtrend"}
    for rid,bad_trend in required.items():
        payload=CASES[rid]
        p={**payload,"context":{**payload["context"],"trend":bad_trend}}
        out=evaluate_rule(rid,p)
        assert out["status"]=="FAIL",(rid,out)
