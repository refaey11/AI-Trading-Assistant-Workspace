from evaluation.direction_arbitration_v2_candidate_v1 import arbitrate


def test_agree_uses_murphy_direction():
    r = arbitrate(
        brain_direction="BULLISH",
        brain_confidence=0.8,
        murphy_direction="BULLISH",
        murphy_has_valid_setup=True,
        nison_confirmation="CONFIRMED",
    )
    assert r["arbitration_classification"] == "AGREE"
    assert r["final"] == "BULLISH"


def test_conflict_is_not_silently_converted_to_trade():
    r = arbitrate(
        brain_direction="BEARISH",
        brain_confidence=0.8,
        murphy_direction="BULLISH",
        murphy_has_valid_setup=True,
    )
    assert r["arbitration_classification"] == "CONFLICT"
    assert r["final"] == "NO_TRADE"


def test_murphy_only_is_allowed_in_development_candidate():
    r = arbitrate(
        brain_direction="NEUTRAL",
        brain_confidence=0.2,
        murphy_direction="BULLISH",
        murphy_has_valid_setup=True,
        nison_confirmation="ABSENT",
    )
    assert r["arbitration_classification"] == "MURPHY_ONLY"
    assert r["final"] == "BULLISH"


def test_nison_contradiction_blocks():
    r = arbitrate(
        brain_direction="BULLISH",
        brain_confidence=0.8,
        murphy_direction="BULLISH",
        murphy_has_valid_setup=True,
        nison_contradiction=True,
    )
    assert r["final"] == "NO_TRADE"
    assert "NISON_CONTRADICTION" in r["blocked_reasons"]


def test_tiz_and_risk_are_hard_gates():
    r = arbitrate(
        brain_direction="BULLISH",
        brain_confidence=0.8,
        murphy_direction="BULLISH",
        murphy_has_valid_setup=True,
        tiz_ready=False,
        risk_pass=False,
    )
    assert r["final"] == "NO_TRADE"
    assert "TIZ_PROCESS_GATE_NOT_READY" in r["blocked_reasons"]
    assert "RISK_GATE_FAIL_OR_NOT_EVALUABLE" in r["blocked_reasons"]


def test_2025_is_explicitly_blocked_from_candidate_policy():
    r = arbitrate(
        brain_direction="BULLISH",
        brain_confidence=0.8,
        murphy_direction="BULLISH",
        murphy_has_valid_setup=True,
    )
    assert r["2025_oos_allowed"] is False
