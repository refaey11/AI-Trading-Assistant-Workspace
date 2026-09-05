from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain
from compatibility.murphy_governed_decision_gate_v1 import assess_with_murphy_gate


def _run(direction):
    return assess_with_murphy_gate(
        decision_brain,
        row={
            "mtf_trend_score": 0.8,
            "M5_trend_regime": 0.6,
            "M15_trend_regime": 0.7,
            "M30_trend_regime": 0.5,
            "H1_trend_regime": 0.6,
            "H4_trend_regime": 0.5,
            "D1_trend_regime": 0.4,
            "volume_available": True,
            "M5_volume_regime": 0.2,
            "M15_volume_regime": 0.2,
            "M30_volume_regime": 0.2,
            "H1_volume_regime": 0.2,
            "H4_volume_regime": 0.2,
            "D1_volume_regime": 0.2,
        },
        query_as_of="2024-06-03T10:00:00Z",
        mode="development",
        murphy_evidence={
            "status": "PASS",
            "direction": direction,
            "source_rule_id": "0021",
        },
        nison_evidence={"confirmation": "ABSENT", "contradiction": False},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
    )


def test_paired_brain_output_unchanged_by_murphy_direction():
    bull = _run("BULLISH")
    bear = _run("BEARISH")
    assert bull["assessment"] == bear["assessment"]
    assert bull["execution"]["final_trade_decision"] == "EXECUTE"
    assert bear["execution"]["final_trade_decision"] == "NEEDS_REVIEW"
    assert bear["execution"]["execution_eligible"] is False


def test_missing_murphy_direction_fail_closes():
    result = assess_with_murphy_gate(
        decision_brain,
        row={"mtf_trend_score": 0.8},
        query_as_of="2024-06-03T10:00:00Z",
        mode="development",
        murphy_evidence={"status": "PASS", "source_rule_id": "0003"},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
    )
    assert result["execution"]["execution_eligible"] is False
    assert "MURPHY_DIRECTION_NOT_EVALUABLE" in result["execution"]["hard_blocks"]
