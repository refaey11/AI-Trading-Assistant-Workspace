from risk_engine.murphy_0042_0045_risk_adapter import evaluate_portfolio, normalize_risk_gate


def test_canonical_risk_path_passes_and_gate_accepts_authoritative_pass():
    portfolio = evaluate_portfolio(
        total_investment=0.50,
        single_market_exposure=0.15,
        risk_per_market=0.05,
        total_margin=0.25,
    )
    assert portfolio["pass"] is True
    assert all(portfolio["checks"].values())

    for rule_id in ("MURPHY_0042", "MURPHY_0043", "MURPHY_0044", "MURPHY_0045"):
        gate = normalize_risk_gate(
            rule_id=rule_id,
            risk_status="PASS",
            risk_available=True,
            risk_evidence={"statement": "Authoritative risk evidence passed."},
        )
        assert gate["available"] is True
        assert gate["gate"] == "pass"


def test_canonical_risk_path_blocks_any_boundary_breach():
    portfolio = evaluate_portfolio(
        total_investment=0.500001,
        single_market_exposure=0.15,
        risk_per_market=0.05,
        total_margin=0.25,
    )
    assert portfolio["pass"] is False
    assert portfolio["checks"]["MURPHY_0042"] is False

    gate = normalize_risk_gate(
        rule_id="MURPHY_0042",
        risk_status="FAIL",
        risk_available=True,
        risk_evidence={"statement": "Authoritative risk evidence failed."},
    )
    assert gate["available"] is True
    assert gate["gate"] == "fail"


def test_canonical_risk_path_never_promotes_missing_or_unknown_evidence():
    for rule_id in ("MURPHY_0042", "MURPHY_0043", "MURPHY_0044", "MURPHY_0045"):
        missing = normalize_risk_gate(
            rule_id=rule_id,
            risk_status="NOT_EVALUABLE",
            risk_available=False,
        )
        unknown = normalize_risk_gate(
            rule_id=rule_id,
            risk_status="UNKNOWN",
            risk_available=True,
        )
        assert missing["gate"] == "needs_review"
        assert unknown["gate"] == "needs_review"
