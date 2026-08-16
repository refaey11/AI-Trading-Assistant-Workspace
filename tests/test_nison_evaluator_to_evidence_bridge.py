from bridges.nison_evaluator_to_evidence_bridge import adapt_nison_evaluator_result


def test_pass_supports_existing_direction_without_creating_direction():
    out = adapt_nison_evaluator_result({
        "status": "PASS", "rule_id": "NISON_0038", "direction": "BULLISH"
    })
    assert out["gate"] == "pass"
    assert out["available"] is True
    assert out["conflict"] == "supports"
    assert out["decision_hint"] == "neutral"
    assert out["confidence_delta"] == 0.0


def test_fail_contradicts_without_forcing_no_trade():
    out = adapt_nison_evaluator_result({
        "status": "FAIL", "rule_id": "NISON_0035", "direction": "BEARISH"
    })
    assert out["gate"] == "fail"
    assert out["conflict"] == "contradicts"
    assert out["decision_hint"] == "neutral"


def test_not_evaluable_is_neutral_review_state():
    out = adapt_nison_evaluator_result({
        "status": "NOT_EVALUABLE", "rule_id": "NISON_0037", "direction": "UNKNOWN"
    })
    assert out["gate"] == "needs_review"
    assert out["available"] is False
    assert out["decision_hint"] == "neutral"


def test_unsupported_status_is_rejected():
    try:
        adapt_nison_evaluator_result({"status": "PASS_CANDIDATE"})
    except ValueError as exc:
        assert "Unsupported evaluator status" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
