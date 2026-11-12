from OOS_2025.tiz_optional_execution_adapter_v2 import build_optional_oos_execution_plan


def _event(**overrides):
    event = {
        "evaluation_mode": "TIZ_OPTIONAL_EVAL",
        "final_action": "BUY",
        "risk_pass": True,
        "entry_price": 1.2500,
        "atr": 0.0050,
    }
    event.update(overrides)
    return event


def test_missing_tiz_is_allowed_and_levels_remain_frozen():
    result = build_optional_oos_execution_plan(_event())
    assert result["status"] == "EXECUTABLE"
    assert result["stop_loss"] == 1.24625
    assert result["take_profit"] == 1.2575
    assert result["tiz_decision_authority"] is False


def test_tiz_status_never_changes_execution_or_levels():
    plans = [build_optional_oos_execution_plan(_event(tiz_process_state=state)) for state in ("READY", "FAIL", "NOT_EVALUABLE", "UNRECOGNIZED")]
    assert all(plan["status"] == "EXECUTABLE" for plan in plans)
    assert all(plan["stop_loss"] == plans[0]["stop_loss"] for plan in plans)
    assert all(plan["take_profit"] == plans[0]["take_profit"] for plan in plans)


def test_wrong_mode_is_rejected():
    result = build_optional_oos_execution_plan(_event(evaluation_mode="CANONICAL"))
    assert result["status"] == "NOT_EXECUTABLE"


def test_risk_failure_is_still_hard_block():
    result = build_optional_oos_execution_plan(_event(risk_pass=False))
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "risk_gate_not_passed"
