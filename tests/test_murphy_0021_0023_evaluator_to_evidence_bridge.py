from bridges.murphy_0021_0023_evaluator_to_evidence_bridge import adapt_evaluator_result


def test_pass_bullish():
    r = adapt_evaluator_result({"rule_id":"MURPHY_0021","status":"PASS","directional_confirmation":"BULLISH","reason":"ok"})
    assert r["gate"] == "pass"
    assert r["available"] is True
    assert r["direction"] == "BULLISH"
    assert r["decision_hint"] == "bullish"
    assert r["confidence_delta"] == 0.0


def test_pass_bearish():
    r = adapt_evaluator_result({"rule_id":"MURPHY_0021","status":"PASS","directional_confirmation":"BEARISH","reason":"ok"})
    assert r["gate"] == "pass"
    assert r["decision_hint"] == "bearish"


def test_fail_does_not_invent_direction():
    r = adapt_evaluator_result({"rule_id":"MURPHY_0022","status":"FAIL","directional_confirmation":"NONE","reason":"not confirmed"})
    assert r["gate"] == "fail"
    assert r["decision_hint"] == "no_trade"
    assert r["direction"] == "NONE"


def test_not_evaluable_requires_review():
    r = adapt_evaluator_result({"rule_id":"MURPHY_0023","status":"NOT_EVALUABLE","directional_confirmation":"UNKNOWN","reason":"missing data"})
    assert r["gate"] == "needs_review"
    assert r["available"] is False
    assert r["conflict"] == "insufficient"


def test_raw_result_is_preserved():
    src = {"rule_id":"MURPHY_0021","status":"PASS","directional_confirmation":"BULLISH","reason":"ok","extra":"x"}
    r = adapt_evaluator_result(src)
    assert r["raw_evaluator_result"] == src
