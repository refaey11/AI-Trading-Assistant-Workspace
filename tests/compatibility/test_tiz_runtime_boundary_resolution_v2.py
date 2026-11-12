from __future__ import annotations

import json
from pathlib import Path

from OOS_2025.tiz_optional_eval_v1 import evaluate_execution_eligibility
from OOS_2025.tiz_fail_closed_gate_v1 import evaluate_tiz_gate


ROOT = Path(__file__).resolve().parents[2]


def _policy() -> dict:
    path = ROOT / "03_TIZ" / "TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_tiz_policy_has_no_decision_authority():
    policy = _policy()
    assert policy["status"] == "SUPERSEDED_BY_PROJECT_DECISION_2026-11-12"
    assert policy["role"] == "optional_metadata_only"
    assert policy["decision_authority"] is False
    assert all(value is False for value in policy["decision_effects"].values())


def test_legacy_tiz_observer_never_returns_execution_gate():
    result = evaluate_tiz_gate({"tiz_process_state": "NOT_EVALUABLE", "authoritative": False, "direction": "NEUTRAL"})
    assert result["status"] == "METADATA_ONLY"
    assert result["decision_authority"] is False
    assert result["execution_effect"] is False
    assert "execution_allowed" not in result


def test_tiz_state_does_not_change_optional_eval_eligibility():
    base = {"evaluation_mode": "TIZ_OPTIONAL_EVAL", "nison_evidence_available": True, "risk_pass": True}
    results = [evaluate_execution_eligibility({**base, "tiz_status": state}) for state in ("PASS", "FAIL", "NOT_EVALUABLE")]
    assert all(result["execution_eligible"] is True for result in results)
    assert all(result["reason"] == "NISON_AND_RISK_PASS" for result in results)


def test_tiz_cannot_generate_or_override_direction():
    result = evaluate_tiz_gate({"tiz_process_state": "READY", "direction": "BUY"})
    assert result["status"] == "METADATA_ONLY"
    assert result["direction_field_valid"] is False
    assert result["decision_authority"] is False
