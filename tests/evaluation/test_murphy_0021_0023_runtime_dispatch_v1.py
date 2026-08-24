from MURPHY_EVALUATORS_V1.murphy_runtime_entrypoint_v1 import evaluate_rule


def test_0021_is_registered_in_unified_runtime():
    result = evaluate_rule(
        "MURPHY_0021",
        {"close": 101.0, "previous_close": 100.0, "volume_direction": "UP"},
    )
    assert result["rule_id"] == "MURPHY_0021"
    assert result["status"] == "PASS"


def test_0022_requires_futures_oi_evidence():
    result = evaluate_rule(
        "MURPHY_0022",
        {"close": 101.0, "previous_close": 100.0, "volume_direction": "UP"},
    )
    assert result["rule_id"] == "MURPHY_0022"
    assert result["status"] == "NOT_EVALUABLE"


def test_0022_registered_and_passes_with_complete_evidence():
    result = evaluate_rule(
        "MURPHY_0022",
        {
            "close": 101.0,
            "previous_close": 100.0,
            "volume_direction": "UP",
            "oi_direction": "UP",
        },
    )
    assert result["rule_id"] == "MURPHY_0022"
    assert result["status"] == "PASS"
    assert result["directional_confirmation"] == "BULLISH"


def test_0023_registered_and_passes_with_complete_evidence():
    result = evaluate_rule(
        "MURPHY_0023",
        {
            "close": 99.0,
            "previous_close": 100.0,
            "volume_direction": "UP",
            "oi_direction": "UP",
        },
    )
    assert result["rule_id"] == "MURPHY_0023"
    assert result["status"] == "PASS"
    assert result["directional_confirmation"] == "BEARISH"


def test_0023_remains_fail_closed_without_oi():
    result = evaluate_rule(
        "MURPHY_0023",
        {"close": 99.0, "previous_close": 100.0, "volume_direction": "UP"},
    )
    assert result["rule_id"] == "MURPHY_0023"
    assert result["status"] == "NOT_EVALUABLE"
