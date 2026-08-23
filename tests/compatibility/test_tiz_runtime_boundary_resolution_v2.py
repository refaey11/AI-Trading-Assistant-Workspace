from __future__ import annotations

import json
from pathlib import Path

from OOS_2025.tiz_optional_eval_v1 import evaluate_execution_eligibility
from OOS_2025.tiz_fail_closed_gate_v1 import evaluate_tiz_gate


ROOT = Path(__file__).resolve().parents[2]


def _policy() -> dict:
    path = ROOT / "03_TIZ" / "TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_tiz_is_direction_neutral_and_process_only():
    policy = _policy()
    assert policy["status"] == "AUTHORITATIVE_BOUNDARY"
    assert policy["role"] == "process_only"
    assert policy["direction"] == "NEUTRAL"
    assert policy["market_derived"] is False
    assert policy["producer_kind"] == "PROCESS_EVIDENCE_INTERFACE"
    assert policy["producer_rules"]["no_direction_generation"] is True
    assert policy["producer_rules"]["no_direction_override"] is True


def test_canonical_mode_stays_fail_closed_without_authoritative_tiz():
    result = evaluate_tiz_gate(
        {
            "tiz_process_state": "NOT_EVALUABLE",
            "authoritative": False,
            "direction": "NEUTRAL",
        }
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["execution_allowed"] is False


def test_optional_oos_mode_explicitly_allows_unverified_tiz_only():
    result = evaluate_execution_eligibility(
        {
            "evaluation_mode": "TIZ_OPTIONAL_EVAL",
            "nison_evidence_available": True,
            "risk_pass": True,
            "tiz_status": "NOT_EVALUABLE",
        }
    )
    assert result["execution_eligible"] is True
    assert result["tiz_verified"] is False
    assert result["reason"] == "TIZ_UNAVAILABLE_UNVERIFIED"


def test_optional_mode_never_turns_non_neutral_tiz_into_direction():
    result = evaluate_execution_eligibility(
        {
            "evaluation_mode": "TIZ_OPTIONAL_EVAL",
            "nison_evidence_available": True,
            "risk_pass": True,
            "tiz_status": "PASS",
        }
    )
    assert result["execution_eligible"] is True
    assert result["tiz_verified"] is True
