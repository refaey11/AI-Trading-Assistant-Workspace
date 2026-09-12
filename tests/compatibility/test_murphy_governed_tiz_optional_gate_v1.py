import importlib.util
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "compatibility" / "murphy_governed_decision_gate_v1.py"


def load_gate():
    spec = importlib.util.spec_from_file_location("murphy_gate", GATE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brain():
    return SimpleNamespace(
        market_state="trend",
        directional_bias="bullish",
        confidence=0.8,
        evidence=[],
        contradictions=[],
        no_trade_reasons=[],
    )


def test_optional_missing_tiz_allows_execution_with_explicit_flag():
    gate = load_gate()
    result = gate.assess_with_murphy_gate(
        brain,
        row={},
        query_as_of="2024-12-31T23:00:00Z",
        mode="development",
        murphy_evidence={"status": "PASS", "direction": "BULLISH"},
        nison_evidence={"confirmation": "ABSENT", "contradiction": False},
        tiz_evidence={"process_gate": "NOT_EVALUABLE", "unverified": True, "mode": "optional"},
        risk_evidence={"risk_status": "PASS"},
        tiz_mode="optional",
    )
    assert result["execution"]["execution_eligible"] is True
    assert result["execution"]["final_trade_decision"] == "EXECUTE_TIZ_UNVERIFIED"
    assert result["execution"]["tiz_unverified"] is True
    assert result["execution"]["hard_blocks"] == []


def test_strict_missing_tiz_blocks_execution():
    gate = load_gate()
    result = gate.assess_with_murphy_gate(
        brain,
        row={},
        query_as_of="2024-12-31T23:00:00Z",
        mode="development",
        murphy_evidence={"status": "PASS", "direction": "BULLISH"},
        nison_evidence={"confirmation": "ABSENT", "contradiction": False},
        tiz_evidence={"process_gate": "NOT_EVALUABLE", "unverified": True, "mode": "strict"},
        risk_evidence={"risk_status": "PASS"},
        tiz_mode="strict",
    )
    assert result["execution"]["execution_eligible"] is False
    assert result["execution"]["final_trade_decision"] == "BLOCKED"
    assert "TIZ_NOT_EVALUABLE" in result["execution"]["hard_blocks"]


def test_risk_remains_hard_gate_in_optional_tiz_mode():
    gate = load_gate()
    result = gate.assess_with_murphy_gate(
        brain,
        row={},
        query_as_of="2024-12-31T23:00:00Z",
        mode="development",
        murphy_evidence={"status": "PASS", "direction": "BULLISH"},
        nison_evidence={"confirmation": "ABSENT", "contradiction": False},
        tiz_evidence={"process_gate": "NOT_EVALUABLE", "unverified": True, "mode": "optional"},
        risk_evidence={"risk_status": "FAIL"},
        tiz_mode="optional",
    )
    assert result["execution"]["execution_eligible"] is False
    assert "RISK_FAIL" in result["execution"]["hard_blocks"]
