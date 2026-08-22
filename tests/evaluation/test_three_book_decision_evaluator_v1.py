from evaluation.three_book_decision_evaluator_v1 import evaluate_three_book_decision


RULES = ["MURPHY_0003", "NISON_0001"]


def base_inputs():
    return {
        "brain_assessment": {"directional_bias": "bullish", "confidence": 0.8},
        "murphy_evidence": {"status": "PASS", "direction": "BULLISH"},
        "nison_evidence": {"confirmation": "CONFIRMED", "contradiction": False},
        "tiz_evidence": {"process_state": "READY", "impulse_override": False, "loss_chasing": False, "revenge_trade": False},
        "risk_evidence": {"risk_pass": True, "stop_loss": "1.2700", "take_profit": "1.2800", "rr": "2.0"},
        "source_rule_ids": RULES,
        "timestamp": "2024-12-31T23:00:00Z",
    }


def test_confirmed_bullish_becomes_executable_buy():
    result = evaluate_three_book_decision(**base_inputs())
    assert result["signal"]["direction"] == "BUY"
    assert result["signal"]["status"] == "EXECUTABLE"
    assert result["decision"]["final"] == "BUY"
    assert result["decision"]["logic"] == "strong"


def test_weak_or_absent_nison_is_medium_not_direction_source():
    args = base_inputs()
    args["nison_evidence"] = {"confirmation": "ABSENT", "contradiction": False}
    result = evaluate_three_book_decision(**args)
    assert result["signal"]["direction"] == "BUY"
    assert result["decision"]["logic"] == "medium"


def test_nison_contradiction_rejects():
    args = base_inputs()
    args["nison_evidence"] = {"confirmation": "CONTRADICTION", "contradiction": True}
    result = evaluate_three_book_decision(**args)
    assert result["signal"]["direction"] == "NO_TRADE"
    assert result["decision"]["final"] == "NO_TRADE"


def test_tiz_not_ready_rejects():
    args = base_inputs()
    args["tiz_evidence"] = {"process_state": "NOT_READY"}
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"
    assert result["decision"]["reasons_against"] == ["TIZ_PROCESS_GATE_NOT_READY"]


def test_risk_failure_rejects():
    args = base_inputs()
    args["risk_evidence"] = {"risk_pass": False, "stop_loss": "1.2700"}
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"


def test_missing_stop_loss_rejects():
    args = base_inputs()
    args["risk_evidence"] = {"risk_pass": True, "stop_loss": ""}
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"
    assert result["decision"]["reasons_against"] == ["STOP_LOSS_UNDEFINED"]


def test_unknown_rule_id_is_hard_rejected():
    args = base_inputs()
    args["source_rule_ids"] = ["MURPHY_9999"]
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"
    assert result["decision"]["reasons_against"] == ["RULE_ALLOWLIST_REJECT"]


def test_murphy_direction_conflict_rejects():
    args = base_inputs()
    args["murphy_evidence"] = {"status": "PASS", "direction": "BEARISH"}
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"


def test_brain_neutral_rejects_without_creating_direction():
    args = base_inputs()
    args["brain_assessment"] = {"directional_bias": "neutral", "confidence": 0.9}
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"
