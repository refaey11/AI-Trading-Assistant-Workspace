from OOS_2025.tiz_fail_closed_gate_v1 import evaluate_tiz_gate


def test_missing_tiz_is_metadata_only():
    result = evaluate_tiz_gate({"tiz_process_state": "NOT_EVALUABLE", "authoritative": False})
    assert result["status"] == "METADATA_ONLY"
    assert result["process_state"] == "NOT_EVALUABLE"
    assert result["decision_authority"] is False
    assert result["execution_effect"] is False


def test_tiz_fail_does_not_create_execution_block():
    result = evaluate_tiz_gate({"tiz_process_state": "FAIL", "authoritative": True})
    assert result["status"] == "METADATA_ONLY"
    assert result["process_state"] == "FAIL"
    assert "execution_allowed" not in result


def test_tiz_reported_direction_is_only_diagnostic_metadata():
    result = evaluate_tiz_gate({"tiz_process_state": "READY", "direction": "BUY"})
    assert result["status"] == "METADATA_ONLY"
    assert result["direction_field_valid"] is False
    assert result["decision_authority"] is False
