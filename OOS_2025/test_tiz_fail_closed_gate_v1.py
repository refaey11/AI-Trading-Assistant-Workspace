from OOS_2025.tiz_fail_closed_gate_v1 import evaluate_tiz_gate


def test_missing_tiz_is_no_trade():
    result = evaluate_tiz_gate({
        "tiz_process_state": "NOT_EVALUABLE",
        "authoritative": False,
        "direction": "NEUTRAL",
    })
    assert result["status"] == "NOT_EVALUABLE"
    assert result["execution_allowed"] is False


def test_non_authoritative_tiz_is_no_trade():
    result = evaluate_tiz_gate({
        "tiz_process_state": "READY",
        "authoritative": False,
        "direction": "NEUTRAL",
    })
    assert result["status"] == "NOT_EVALUABLE"
    assert result["execution_allowed"] is False


def test_authoritative_pass_is_allowed():
    result = evaluate_tiz_gate({
        "tiz_process_state": "READY",
        "authoritative": True,
        "direction": "NEUTRAL",
    })
    assert result["status"] == "PASS"
    assert result["execution_allowed"] is True


def test_tiz_cannot_create_direction():
    result = evaluate_tiz_gate({
        "tiz_process_state": "READY",
        "authoritative": True,
        "direction": "BUY",
    })
    assert result["status"] == "BLOCKED"
    assert result["execution_allowed"] is False
