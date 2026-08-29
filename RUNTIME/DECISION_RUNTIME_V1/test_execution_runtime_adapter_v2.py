from execution_runtime_adapter_v2 import build_execution_plan


def test_tiz_unavailable_is_unverified_not_blocking_when_risk_passes():
    result = build_execution_plan({
        "final_action": "BUY",
        "entry_price": 1.25,
        "atr": 0.005,
        "risk_pass": True,
        "tiz_process_state": "NOT_EVALUABLE",
    })
    assert result["status"] == "EXECUTABLE"
    assert result["tiz_verified"] is False
    assert result["tiz_status"] == "NOT_EVALUABLE"
    assert round(result["stop_loss"], 6) == 1.24625
    assert round(result["take_profit"], 6) == 1.2575


def test_tiz_available_is_verified():
    result = build_execution_plan({
        "final_action": "SELL",
        "entry_price": 1.25,
        "atr": 0.005,
        "risk_pass": True,
        "tiz_process_state": "READY",
    })
    assert result["status"] == "EXECUTABLE"
    assert result["tiz_verified"] is True


def test_risk_remains_hard_gate():
    result = build_execution_plan({
        "final_action": "BUY",
        "entry_price": 1.25,
        "atr": 0.005,
        "risk_pass": False,
        "tiz_process_state": "NOT_EVALUABLE",
    })
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "risk_gate_not_passed"
