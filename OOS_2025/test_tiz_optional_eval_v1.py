from tiz_optional_eval_v1 import evaluate_execution_eligibility


def test_tiz_optional_allows_unverified_tiz_with_nison_and_risk():
    result = evaluate_execution_eligibility({
        "evaluation_mode": "TIZ_OPTIONAL_EVAL",
        "nison_evidence_available": True,
        "risk_pass": True,
        "tiz_status": "NOT_EVALUABLE",
    })
    assert result == {
        "execution_eligible": True,
        "reason": "TIZ_UNAVAILABLE_UNVERIFIED",
        "tiz_verified": False,
    }


def test_tiz_optional_requires_nison():
    result = evaluate_execution_eligibility({
        "evaluation_mode": "TIZ_OPTIONAL_EVAL",
        "nison_evidence_available": False,
        "risk_pass": True,
        "tiz_status": "NOT_EVALUABLE",
    })
    assert result["execution_eligible"] is False
    assert result["reason"] == "MISSING_NISON_EVIDENCE"


def test_tiz_optional_requires_risk_pass():
    result = evaluate_execution_eligibility({
        "evaluation_mode": "TIZ_OPTIONAL_EVAL",
        "nison_evidence_available": True,
        "risk_pass": False,
        "tiz_status": "NOT_EVALUABLE",
    })
    assert result["execution_eligible"] is False
    assert result["reason"] == "RISK_FAIL"


def test_canonical_mode_is_not_bypassed():
    result = evaluate_execution_eligibility({
        "evaluation_mode": "CANONICAL_THREE_BOOK",
        "nison_evidence_available": True,
        "risk_pass": True,
        "tiz_status": "NOT_EVALUABLE",
    })
    assert result["execution_eligible"] is False
    assert result["reason"] == "WRONG_EVALUATION_MODE"
