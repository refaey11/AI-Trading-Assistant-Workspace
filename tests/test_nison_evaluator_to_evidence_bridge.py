from bridges.nison_evaluator_to_evidence_bridge import adapt_nison_evaluator_result


def test_pass_supports_bullish_without_creating_direction():
    out = adapt_nison_evaluator_result({
        "status": "PASS",
        "rule_id": "NISON_0038",
        "direction": "BULLISH",
        "reason": "Window confirmed",
    })
    assert out["module"] == "nison_confirmation"
    assert out["gate"] == "pass"
    assert out["available"] is True
    assert out["conflict"] == "supports"
    assert out["decision_hint"] == "neutral"
    assert out["confidence_delta"] == 0.0


def test_fail_contradicts_bearish_without_forcing_no_trade():
    out = adapt_nison_evaluator_result({
        "status": "FAIL",
        "rule_id": "NISON_0035",
        "direction": "BEARISH",
        "reason": "Tasuki condition failed",
    })
    assert out["gate"] == "fail"
    assert out["available"] is True
    assert out["conflict"] == "contradicts"
    assert out["decision_hint"] == "neutral"
    assert out["confidence_delta"] == 0.0


def test_not_evaluable_is_needs_review_and_neutral():
    out = adapt_nison_evaluator_result({
        "status": "NOT_EVALUABLE",
        "rule_id": "NISON_0037",
        "direction": "UNKNOWN",
        "reason": "Comparator not source-locked",
    })
    assert out["gate"] == "needs_review"
    assert out["available"] is False
    assert out["conflict"] == "insufficient"
    assert out["decision_hint"] == "neutral"


def test_unsupported_status_is_rejected():
    try:
        adapt_nison_evaluator_result({"status": "PASS_CANDIDATE"})
    except ValueError as exc:
        assert "Unsupported evaluator status" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
