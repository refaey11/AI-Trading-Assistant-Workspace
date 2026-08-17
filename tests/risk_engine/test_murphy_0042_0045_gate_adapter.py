from risk_engine.murphy_0042_0045_risk_adapter import normalize_risk_gate


def test_pass_evidence_maps_to_pass():
    result = normalize_risk_gate(rule_id="MURPHY_0042", risk_status="PASS", risk_available=True)
    assert result["available"] is True
    assert result["gate"] == "pass"


def test_fail_evidence_is_hard_block():
    result = normalize_risk_gate(rule_id="MURPHY_0043", risk_status="FAIL", risk_available=True)
    assert result["available"] is True
    assert result["gate"] == "fail"


def test_missing_evidence_needs_review():
    result = normalize_risk_gate(rule_id="MURPHY_0044", risk_status="NOT_EVALUABLE", risk_available=False)
    assert result["available"] is False
    assert result["gate"] == "needs_review"


def test_unknown_status_never_becomes_pass():
    result = normalize_risk_gate(rule_id="MURPHY_0045", risk_status="UNKNOWN", risk_available=True)
    assert result["available"] is False
    assert result["gate"] == "needs_review"
