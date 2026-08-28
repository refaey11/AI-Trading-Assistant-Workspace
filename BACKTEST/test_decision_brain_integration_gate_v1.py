import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "BACKTEST" / "decision_brain_integration_gate_v1.py"
ADAPTER_PATH = ROOT / "compatibility" / "decision_brain_v1_handoff_adapter.py"
BRAIN_PATH = ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_governance_adapter_accepts_full_evidence_package_without_direction_from_memory():
    adapter = load(ADAPTER_PATH, "handoff_adapter")
    brain = load(BRAIN_PATH, "brain")
    row = {
        "mtf_trend_score": 0.6,
        "M5_trend_regime": 0.4,
        "M15_trend_regime": 0.4,
        "M30_trend_regime": 0.3,
        "H1_trend_regime": 0.4,
        "H4_trend_regime": 0.2,
        "D1_trend_regime": 0.1,
        "volume_available": True,
        "M5_volume_regime": 0.2,
        "M15_volume_regime": 0.1,
        "M30_volume_regime": 0.1,
        "H1_volume_regime": 0.1,
        "H4_volume_regime": 0.1,
        "D1_volume_regime": 0.1,
    }
    result = adapter.assess_with_governance(
        brain,
        row=row,
        query_as_of="2024-12-30T12:00:00Z",
        murphy_evidence={"status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0003"},
        nison_evidence={"confirmation": "CONFIRMED", "contradiction": False},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
        historical_evidence={
            "retrieval_status": "OK",
            "candidate_count": 10,
            "top_k_returned": 10,
            "nearest_distance": 0.2,
            "distance_summary": {"min": 0.2, "max": 0.7, "mean": 0.4},
            "historical_evidence_ids_or_positions": [1, 2],
            "evidence_time_range": {"earliest": "2018-01-01T00:00:00Z", "latest": "2024-12-29T00:00:00Z"},
            "predicted_return": 0.12,
        },
    )
    assert result["status"] == "PASS"
    assert result["governance"]["similarity_generated_direction"] is False
    assert result["governance"]["predicted_return_used_as_direction"] is False
    assert result["governance"]["nison_generated_direction"] is False


def test_adapter_locks_2025_for_development():
    adapter = load(ADAPTER_PATH, "handoff_adapter_oos")
    brain = load(BRAIN_PATH, "brain_oos")
    result = adapter.assess_with_governance(
        brain,
        row={"mtf_trend_score": 0.5},
        query_as_of="2025-01-02T00:00:00Z",
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "2025_OOS_LOCKED"


def test_gate_module_imports():
    load(GATE_PATH, "integration_gate")
