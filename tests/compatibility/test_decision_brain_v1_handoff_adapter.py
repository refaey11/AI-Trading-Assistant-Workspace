import importlib.util
from pathlib import Path

from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance


ROOT = Path(__file__).resolve().parents[2]
BRAIN_PATH = ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py"


def load_brain():
    spec = importlib.util.spec_from_file_location("recovered_decision_brain", BRAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def base_row():
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


def good_evidence():
    return {
        "process_gate": "PASS",
        "risk_status": "PASS",
        "confirmation": "CONFIRMED",
        "contradiction": False,
        "retrieval_status": "OK",
        "candidate_count": 20,
        "top_k_returned": 20,
        "nearest_distance": 0.21,
        "distance_summary": {"min": 0.21, "max": 0.84, "mean": 0.44},
        "historical_evidence_ids_or_positions": [1, 2, 3],
        "evidence_time_range": {
            "earliest": "2024-10-01T00:00:00Z",
            "latest": "2024-12-31T00:00:00Z",
        },
        # Deliberately present: adapter must strip it from directional use.
        "predicted_return": 0.004,
    }


def test_pre_oos_passes_and_memory_cannot_create_direction():
    result = assess_with_governance(
        load_brain(),
        row=base_row(),
        query_as_of="2024-12-31T23:00:00Z",
        murphy_evidence={"status": "PASS", "source_rule_id": "MURPHY_0003"},
        nison_evidence=good_evidence(),
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
        historical_evidence=good_evidence(),
    )
    assert result["status"] == "PASS"
    assert result["governance"]["predicted_return_used_as_direction"] is False
    assert result["governance"]["similarity_generated_direction"] is False
    assert result["historical_evidence"]["predicted_return_used_as_direction"] is False
    assert result["execution"]["final_trade_decision"] is None


def test_development_2025_is_locked():
    result = assess_with_governance(
        load_brain(), row=base_row(), query_as_of="2025-01-02T00:00:00Z"
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "2025_OOS_LOCKED"


def test_future_data_is_forbidden_even_in_oos_mode():
    result = assess_with_governance(
        load_brain(),
        row=base_row(),
        query_as_of="2026-01-01T00:00:00Z",
        mode="oos_evaluation",
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "FUTURE_DATA_FORBIDDEN"


def test_risk_fail_blocks_execution():
    result = assess_with_governance(
        load_brain(),
        row=base_row(),
        query_as_of="2024-12-31T23:00:00Z",
        nison_evidence={"confirmation": "CONFIRMED", "contradiction": False},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "FAIL"},
    )
    assert result["execution"]["eligible"] is False
    assert "RISK_GATE_FAIL" in result["execution"]["hard_blocks"]


def test_tiz_fail_blocks_execution():
    result = assess_with_governance(
        load_brain(),
        row=base_row(),
        query_as_of="2024-12-31T23:00:00Z",
        nison_evidence={"confirmation": "CONFIRMED", "contradiction": False},
        tiz_evidence={"process_gate": "FAIL"},
        risk_evidence={"risk_status": "PASS"},
    )
    assert result["execution"]["eligible"] is False
    assert "TIZ_PROCESS_GATE_FAIL" in result["execution"]["hard_blocks"]


def test_nison_contradiction_requires_review_and_cannot_flip_direction():
    result = assess_with_governance(
        load_brain(),
        row=base_row(),
        query_as_of="2024-12-31T23:00:00Z",
        nison_evidence={"confirmation": "CONFIRMED", "contradiction": True},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
    )
    assert result["governance"]["nison_generated_direction"] is False
    assert "NISON_CONTRADICTION" in result["execution"]["needs_review"]
    assert result["execution"]["eligible"] is False
