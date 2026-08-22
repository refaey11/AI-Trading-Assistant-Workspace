from nison_0031_0044_runtime import evaluate_rule

PATTERN_RULES = [f"CANDLE_RULE_{i:04d}" for i in range(31, 39)]
MODULE_RULES = [f"NISON_MODULE_{i:04d}" for i in range(39, 45)]


def test_fail_closed_without_upstream_evidence():
    for rid in PATTERN_RULES:
        out = evaluate_rule(rid, {"context": {}})
        assert out["status"] == "NOT_EVALUABLE", (rid, out)


def test_pattern_confirmation_path():
    for rid in PATTERN_RULES:
        if rid == "CANDLE_RULE_0038":
            payload = {"context": {
                "previous_session": {"high": 10.0, "low": 9.0},
                "current_session": {"high": 12.0, "low": 10.5},
                "direction": "bullish",
            }}
            out = evaluate_rule(rid, payload)
            assert out["status"] == "PASS", (rid, out)
        else:
            payload = {"context": {"formation_confirmed": True, "confirmation": {"confirmed": True}}}
            out = evaluate_rule(rid, payload)
            assert out["status"] == "PASS", (rid, out)


def test_confirmation_required_for_0031_0037():
    for rid in PATTERN_RULES:
        if rid == "CANDLE_RULE_0038":
            continue
        payload = {"context": {"formation_confirmed": True, "confirmation": {"confirmed": False}}}
        out = evaluate_rule(rid, payload)
        assert out["status"] == "FAIL", (rid, out)
        assert "confirmation" in out["reason"].lower()


def test_methodology_modules_are_context_only():
    for rid in MODULE_RULES:
        out = evaluate_rule(rid, {"context": {"evidence_available": True, "role": "context"}})
        assert out["status"] == "PASS", (rid, out)
        assert out["provenance"]["standalone_direction"] is False


def test_methodology_modules_fail_closed_when_missing():
    for rid in MODULE_RULES:
        out = evaluate_rule(rid, {"context": {}})
        assert out["status"] == "NOT_EVALUABLE", (rid, out)


def test_window_geometry_does_not_use_future_bars():
    out = evaluate_rule("CANDLE_RULE_0038", {"context": {
        "previous_session": {"high": 10.0, "low": 9.0},
        "current_session": {"high": 12.0, "low": 10.5},
        "direction": "bullish",
    }})
    assert out["status"] == "PASS"
    assert out["provenance"]["lookahead"] == "none"
