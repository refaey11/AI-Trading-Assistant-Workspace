from __future__ import annotations

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain
from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event


RULES = ["MURPHY_0003", "NISON_0001"]


def row():
    return {
        "mtf_trend_score": 0.7,
        "M5_trend_regime": 0.4,
        "M15_trend_regime": 0.5,
        "M30_trend_regime": 0.3,
        "H1_trend_regime": 0.4,
        "H4_trend_regime": 0.2,
        "D1_trend_regime": 0.1,
        "volume_available": True,
        "M5_volume_regime": 0.2,
        "M15_volume_regime": 0.1,
    }


def base():
    return dict(
        decision_brain_module=decision_brain,
        row=row(),
        query_as_of="2024-12-31T23:00:00Z",
        murphy_evidence={"status": "PASS", "direction": "BULLISH"},
        nison_evidence={"confirmation": "CONFIRMED", "contradiction": False},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS", "stop_loss": "1.2700", "take_profit": "1.2800", "rr": "2.0"},
        historical_evidence={"predicted_return": 0.004, "retrieval_status": "OK"},
        source_rule_ids=RULES,
        entry_price=1.275,
        atr=0.002,
    )


def test_full_assembler_executes_only_when_all_gates_pass():
    result = assemble_decision_event(**base())
    assert result["status"] == "EXECUTABLE"
    assert result["decision"]["decision"]["final"] == "BUY"
    assert result["execution_plan"]["direction"] == "BUY"
    assert result["execution_plan"]["sl_atr"] == 0.75
    assert result["execution_plan"]["tp_r"] == 2.0
    assert result["audit"]["historical_memory_used_for_direction"] is False
    assert result["audit"]["nison_generated_direction"] is False


def test_risk_fail_blocks_execution():
    args = base()
    args["risk_evidence"] = {"risk_status": "FAIL", "stop_loss": "1.2700"}
    result = assemble_decision_event(**args)
    assert result["status"] == "NO_TRADE"
    assert result["decision"]["decision"]["final"] == "NO_TRADE"


def test_nison_contradiction_blocks_execution():
    args = base()
    args["nison_evidence"] = {"confirmation": "CONTRADICTION", "contradiction": True}
    result = assemble_decision_event(**args)
    assert result["status"] == "NO_TRADE"


def test_tiz_fail_blocks_execution():
    args = base()
    args["tiz_evidence"] = {"process_gate": "FAIL"}
    result = assemble_decision_event(**args)
    assert result["status"] == "NO_TRADE"


def test_missing_execution_inputs_fail_closed():
    args = base()
    args["entry_price"] = None
    result = assemble_decision_event(**args)
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["execution_plan"]["reason"] == "missing_entry_or_atr"


def test_2025_oos_does_not_tune_or_change_semantics():
    args = base()
    args["query_as_of"] = "2025-12-31T23:00:00Z"
    result = assemble_decision_event(**args)
    assert result["status"] == "EXECUTABLE"
    assert result["audit"]["oos_tuning"] is False
