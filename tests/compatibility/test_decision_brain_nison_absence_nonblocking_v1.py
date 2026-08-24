from datetime import datetime, timezone

import decision_brain
from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance


def _row():
    return {
        "mtf_trend_score": 0.7,
        "M5_trend_regime": 0.4,
        "M15_trend_regime": 0.3,
        "M30_trend_regime": 0.2,
        "H1_trend_regime": 0.4,
        "H4_trend_regime": 0.5,
        "D1_trend_regime": 0.3,
        "volume_available": True,
        "M5_volume_regime": 0.2,
        "M15_volume_regime": 0.2,
        "M30_volume_regime": 0.1,
        "H1_volume_regime": 0.1,
        "H4_volume_regime": 0.2,
        "D1_volume_regime": 0.2,
    }


def test_missing_nison_evidence_does_not_block_brain_when_other_gates_pass():
    result = assess_with_governance(
        decision_brain,
        row=_row(),
        query_as_of=datetime(2024, 12, 31, 23, tzinfo=timezone.utc),
        murphy_evidence={"status": "PASS", "source_rule_id": "MURPHY_0003"},
        nison_evidence={},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
        historical_evidence={},
    )
    assert result["status"] == "PASS"
    assert result["assessment"]["directional_bias"] == "bullish"
    assert result["execution"]["eligible"] is True
    assert result["execution"]["hard_blocks"] == []
    assert result["execution"]["needs_review"] == []
    assert result["governance"]["nison_generated_direction"] is False


def test_nison_contradiction_still_blocks_execution_for_review():
    result = assess_with_governance(
        decision_brain,
        row=_row(),
        query_as_of=datetime(2024, 12, 31, 23, tzinfo=timezone.utc),
        murphy_evidence={"status": "PASS", "source_rule_id": "MURPHY_0003"},
        nison_evidence={"confirmation": "CONTRADICTED", "contradiction": True},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
        historical_evidence={},
    )
    assert result["execution"]["eligible"] is False
    assert "NISON_CONTRADICTION" in result["execution"]["needs_review"]


def test_2025_remains_locked_for_development():
    result = assess_with_governance(
        decision_brain,
        row=_row(),
        query_as_of=datetime(2025, 6, 1, tzinfo=timezone.utc),
        murphy_evidence={"status": "PASS"},
        nison_evidence={},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "2025_OOS_LOCKED"
