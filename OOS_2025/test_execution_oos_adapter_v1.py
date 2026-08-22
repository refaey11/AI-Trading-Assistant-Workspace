from OOS_2025.execution_oos_adapter_v1 import build_execution_plan


def test_long_uses_075_atr_and_2r():
    plan = build_execution_plan({
        "final_action": "BUY",
        "entry_price": 100.0,
        "atr": 2.0,
        "risk_pass": True,
        "tiz_process_state": "READY",
    })
    assert plan["status"] == "EXECUTABLE"
    assert plan["stop_loss"] == 98.5
    assert plan["take_profit"] == 103.0
    assert plan["sl_atr"] == 0.75
    assert plan["tp_r"] == 2.0


def test_short_is_mirrored():
    plan = build_execution_plan({
        "final_action": "SELL",
        "entry_price": 100.0,
        "atr": 2.0,
        "risk_pass": True,
        "tiz_process_state": "READY",
    })
    assert plan["status"] == "EXECUTABLE"
    assert plan["stop_loss"] == 101.5
    assert plan["take_profit"] == 97.0


def test_missing_evidence_fails_closed():
    plan = build_execution_plan({
        "final_action": "BUY",
        "entry_price": 100.0,
        "atr": 2.0,
        "risk_pass": True,
        "tiz_process_state": "NOT_EVALUABLE",
    })
    assert plan["status"] == "NOT_EXECUTABLE"


def test_invalid_risk_fails_closed():
    plan = build_execution_plan({
        "final_action": "BUY",
        "entry_price": 100.0,
        "atr": 2.0,
        "risk_pass": False,
        "tiz_process_state": "READY",
    })
    assert plan["status"] == "NOT_EXECUTABLE"
