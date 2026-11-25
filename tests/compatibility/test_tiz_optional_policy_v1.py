from __future__ import annotations

from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "compatibility" / "murphy_governed_decision_gate_v1.py"


def load_gate():
    spec = importlib.util.spec_from_file_location("murphy_gate", GATE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _Assessment:
    market_state = "TRENDING"
    directional_bias = "BULLISH"
    confidence = 0.9
    evidence = []
    contradictions = []
    no_trade_reasons = []


def _brain():
    class Brain:
        @staticmethod
        def assess(row, similarity=None):
            return _Assessment()
    return Brain


def _base_kwargs(*, tiz="NOT_EVALUABLE", risk="PASS", tiz_mode="optional"):
    return dict(
        decision_brain_module=_brain(),
        row={"H1_trend_regime": "BULLISH"},
        query_as_of="2024-01-02T00:00:00+00:00",
        mode="development",
        murphy_evidence={"status": "PASS", "direction": "BULLISH"},
        nison_evidence={"contradiction": False},
        tiz_evidence={"process_gate": tiz, "mode": tiz_mode, "unverified": tiz == "NOT_EVALUABLE"},
        risk_evidence={"risk_status": risk},
        tiz_mode=tiz_mode,
    )


def test_optional_missing_tiz_allows_execution_with_flag():
    gate = load_gate()
    out = gate.assess_with_murphy_gate(**_base_kwargs())
    assert out["execution"]["execution_eligible"] is True
    assert out["execution"]["final_trade_decision"] == "EXECUTE_TIZ_UNVERIFIED"
    assert out["tiz_evidence"]["unverified"] is True


def test_strict_missing_tiz_blocks_execution():
    gate = load_gate()
    out = gate.assess_with_murphy_gate(**_base_kwargs(tiz_mode="strict"))
    assert out["execution"]["execution_eligible"] is False
    assert out["execution"]["final_trade_decision"] == "BLOCKED"
    assert "TIZ_NOT_EVALUABLE" in out["execution"]["hard_blocks"]


def test_tiz_fail_blocks_even_in_optional_mode():
    gate = load_gate()
    out = gate.assess_with_murphy_gate(**_base_kwargs(tiz="FAIL"))
    assert out["execution"]["execution_eligible"] is False
    assert out["execution"]["final_trade_decision"] == "BLOCKED"
    assert "TIZ_FAIL" in out["execution"]["hard_blocks"]


def test_risk_missing_stays_hard_block_in_optional_mode():
    gate = load_gate()
    out = gate.assess_with_murphy_gate(**_base_kwargs(risk="NOT_EVALUABLE"))
    assert out["execution"]["execution_eligible"] is False
    assert out["execution"]["final_trade_decision"] == "BLOCKED"
    assert "RISK_NOT_EVALUABLE" in out["execution"]["hard_blocks"]


def test_missing_murphy_direction_still_blocks():
    gate = load_gate()
    kwargs = _base_kwargs()
    kwargs["murphy_evidence"] = {"status": "PASS", "direction": None}
    out = gate.assess_with_murphy_gate(**kwargs)
    assert out["execution"]["execution_eligible"] is False
    assert out["execution"]["final_trade_decision"] == "BLOCKED"
    assert "MURPHY_DIRECTION_NOT_EVALUABLE" in out["execution"]["hard_blocks"]
