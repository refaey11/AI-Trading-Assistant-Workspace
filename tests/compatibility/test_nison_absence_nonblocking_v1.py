from datetime import datetime, timezone
import importlib.util
from pathlib import Path

from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance

ROOT = Path(__file__).resolve().parents[2]
BRAIN_PATH = ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py"


def _load_brain():
    spec = importlib.util.spec_from_file_location("recovered_decision_brain", BRAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _row():
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


def test_nison_absent_or_not_evaluable_does_not_globally_block_brain():
    result = assess_with_governance(
        _load_brain(),
        row=_row(),
        query_as_of=datetime(2024, 12, 31, tzinfo=timezone.utc),
        murphy_evidence={"status": "PASS", "source_rule_id": "MURPHY_0003"},
        nison_evidence={},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
    )
    assert result["status"] == "PASS"
    assert result["governance"]["nison_generated_direction"] is False
    assert "NISON_CONTRADICTION" not in result["execution"]["needs_review"]
    assert result["execution"]["eligible"] is True


def test_nison_directional_contradiction_remains_blocking():
    result = assess_with_governance(
        _load_brain(),
        row=_row(),
        query_as_of=datetime(2024, 12, 31, tzinfo=timezone.utc),
        nison_evidence={"confirmation": "CONFIRMED", "contradiction": True},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
    )
    assert result["execution"]["eligible"] is False
    assert "NISON_CONTRADICTION" in result["execution"]["needs_review"]
