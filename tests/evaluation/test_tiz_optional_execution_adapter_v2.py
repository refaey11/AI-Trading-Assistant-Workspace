from OOS_2025.tiz_optional_execution_adapter_v2 import build_optional_oos_execution_plan


def _event(**overrides):
    event = {
        "evaluation_mode": "TIZ_OPTIONAL_EVAL",
        "final_action": "BUY",
        "risk_pass": True,
        "tiz_process_state": "NOT_EVALUABLE",
        "entry_price": 1.2500,
        "atr": 0.0050,
    }
    event.update(overrides)
    return event


def test_missing_tiz_is_allowed_only_in_optional_oos_mode():
    result = build_optional_oos_execution_plan(_event())
    assert result["status"] == "EXECUTABLE"
    assert result["tiz_verified"] is False
    assert result["stop_loss"] == 1.24625
    assert result["take_profit"] == 1.2575


def test_wrong_mode_is_rejected():
    result = build_optional_oos_execution_plan(_event(evaluation_mode="CANONICAL"))
    assert result["status"] == "NOT_EXECUTABLE"


def test_risk_failure_is_still_hard_block():
    result = build_optional_oos_execution_plan(_event(risk_pass=False))
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "risk_gate_not_passed"


def test_tiz_available_is_recorded_as_verified():
    result = build_optional_oos_execution_plan(_event(tiz_process_state="READY"))
    assert result["status"] == "EXECUTABLE"
    assert result["tiz_verified"] is True
