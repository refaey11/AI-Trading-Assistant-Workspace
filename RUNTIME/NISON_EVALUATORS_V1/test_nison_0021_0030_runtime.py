from nison_0021_0030_runtime import evaluate_rule

RULES = [f"CANDLE_RULE_{i:04d}" for i in range(21, 31)]


def test_unknown_inputs_fail_closed():
    for rid in RULES:
        out = evaluate_rule(rid, {"candles": [], "context": {}})
        assert out["status"] == "NOT_EVALUABLE", (rid, out)


def test_formation_fact_and_confirmation_path():
    for rid in RULES:
        if rid == "CANDLE_RULE_0030":
            payload = {"context": {"trend": "Uptrend", "formation_complete": True,
                                   "final_bullish_strong": True,
                                   "confirmation": {"confirmed": True}}}
        else:
            payload = {"context": {"formation_confirmed": True,
                                   "confirmation": {"confirmed": True}}}
        out = evaluate_rule(rid, payload)
        assert out["status"] == "PASS", (rid, out)


def test_confirmation_is_required_where_contract_requires_it():
    for rid in RULES:
        if rid == "CANDLE_RULE_0030":
            payload = {"context": {"trend": "Uptrend", "formation_complete": True,
                                   "final_bullish_strong": True,
                                   "confirmation": {"confirmed": False}}}
        else:
            payload = {"context": {"formation_confirmed": True,
                                   "confirmation": {"confirmed": False}}}
        out = evaluate_rule(rid, payload)
        assert out["status"] == "FAIL", (rid, out)
        assert "confirmation" in out["reason"].lower()
