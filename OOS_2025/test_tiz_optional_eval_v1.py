from OOS_2025.tiz_optional_eval_v1 import evaluate_execution_eligibility


def test_tiz_state_is_metadata_only_when_nison_and_risk_pass():
    base = {"evaluation_mode": "TIZ_OPTIONAL_EVAL", "nison_evidence_available": True, "risk_pass": True}
    results = [evaluate_execution_eligibility({**base, "tiz_status": state}) for state in ("PASS", "FAIL", "NOT_EVALUABLE")]
    assert all(result["execution_eligible"] is True for result in results)
    assert all(result["reason"] == "NISON_AND_RISK_PASS" for result in results)
    assert all(result["tiz_decision_authority"] is False for result in results)


def test_optional_eval_requires_nison():
    result = evaluate_execution_eligibility({"evaluation_mode": "TIZ_OPTIONAL_EVAL", "nison_evidence_available": False, "risk_pass": True})
    assert result["execution_eligible"] is False
    assert result["reason"] == "MISSING_NISON_EVIDENCE"


def test_optional_eval_requires_risk_pass():
    result = evaluate_execution_eligibility({"evaluation_mode": "TIZ_OPTIONAL_EVAL", "nison_evidence_available": True, "risk_pass": False})
    assert result["execution_eligible"] is False
    assert result["reason"] == "RISK_FAIL"


def test_wrong_evaluation_mode_is_rejected():
    result = evaluate_execution_eligibility({"evaluation_mode": "CANONICAL_THREE_BOOK", "nison_evidence_available": True, "risk_pass": True})
    assert result["execution_eligible"] is False
    assert result["reason"] == "WRONG_EVALUATION_MODE"
