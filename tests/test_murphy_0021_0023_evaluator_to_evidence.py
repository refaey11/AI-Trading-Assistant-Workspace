from bridges.murphy_0021_0023_evaluator_to_evidence import adapt_evaluator_result


def test_0021_pass_bullish():
    x = adapt_evaluator_result({"rule_id": "0021", "status": "PASS", "directional_confirmation": "BULLISH", "reason": "ok"})
    assert x["available"] is True
    assert x["gate"] == "pass"
    assert x["direction"] == "bullish"
    assert x["conflict"] == "neutral"
    assert x["decision_hint"] == "bullish"
    assert x["confidence_delta"] == 0


def test_0021_pass_bearish():
    x = adapt_evaluator_result({"rule_id": "0021", "status": "PASS", "directional_confirmation": "BEARISH", "reason": "ok"})
    assert x["direction"] == "bearish"
    assert x["decision_hint"] == "bearish"


def test_0021_fail_does_not_infer_opposite_direction():
    x = adapt_evaluator_result({"rule_id": "0021", "status": "FAIL", "directional_confirmation": "NONE", "reason": "failed"})
    assert x["available"] is True
    assert x["gate"] == "fail"
    assert x["direction"] == "neutral"
    assert x["conflict"] == "contradicts"
    assert x["decision_hint"] == "neutral"


def test_0022_pass_bullish():
    x = adapt_evaluator_result({"rule_id": "0022", "status": "PASS", "directional_confirmation": "BULLISH", "reason": "ok"})
    assert x["gate"] == "pass"
    assert x["direction"] == "bullish"


def test_0022_fail_no_opposite_direction():
    x = adapt_evaluator_result({"rule_id": "0022", "status": "FAIL", "directional_confirmation": "NONE", "reason": "failed"})
    assert x["gate"] == "fail"
    assert x["direction"] == "neutral"
    assert x["decision_hint"] == "neutral"


def test_0022_not_evaluable():
    x = adapt_evaluator_result({"rule_id": "0022", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN", "reason": "missing evidence"})
    assert x["available"] is False
    assert x["gate"] == "needs_review"
    assert x["direction"] == "neutral"
    assert x["conflict"] == "insufficient"


def test_0023_pass_bearish():
    x = adapt_evaluator_result({"rule_id": "0023", "status": "PASS", "directional_confirmation": "BEARISH", "reason": "ok"})
    assert x["gate"] == "pass"
    assert x["direction"] == "bearish"
    assert x["decision_hint"] == "bearish"


def test_unknown_status_is_review_and_direction_neutral():
    x = adapt_evaluator_result({"rule_id": "0021", "status": "UNKNOWN", "directional_confirmation": "BULLISH", "reason": "bad status"})
    assert x["available"] is False
    assert x["gate"] == "needs_review"
    assert x["direction"] == "neutral"
    assert x["decision_hint"] == "neutral"


def test_missing_direction_does_not_infer():
    x = adapt_evaluator_result({"rule_id": "0023", "status": "PASS", "reason": "ok"})
    assert x["direction"] == "neutral"
    assert x["decision_hint"] == "neutral"


def test_raw_result_is_preserved_and_confidence_is_zero():
    raw = {"rule_id": "0022", "status": "PASS", "directional_confirmation": "BULLISH", "reason": "ok", "metadata": {"year": 2025}}
    x = adapt_evaluator_result(raw)
    assert x["raw_evaluator_result"] == raw
    assert x["confidence_delta"] == 0
