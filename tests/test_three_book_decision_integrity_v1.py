from evaluation.three_book_decision_evaluator_v1 import evaluate_three_book_decision


def _base(nison_rows):
    return dict(
        brain_assessment={"directional_bias": "BULLISH", "confidence": 0.999},
        murphy_evidence={"status": "PASS", "direction": "BULLISH"},
        nison_evidence={"status": "PASS", "confirmation": "PASS", "rows": nison_rows},
        tiz_evidence={"authoritative": False, "status": "NOT_EVALUABLE"},
        risk_evidence={"risk_pass": True, "stop_loss": "1.0"},
        source_rule_ids=["MURPHY_0025", "NISON_0001"],
        timestamp="2016-11-10T13:00:00Z",
    )


def test_summary_pass_cannot_override_failed_or_not_evaluable_rows():
    rows = [
        {"source_rule_id": "NISON_0001", "status": "FAIL", "conflict": "neutral"},
        {"source_rule_id": "NISON_0002", "status": "NOT_EVALUABLE", "conflict": "insufficient"},
    ]
    result = evaluate_three_book_decision(**_base(rows))
    assert result["signal"]["direction"] == "NO_TRADE"
    assert result["signal"]["status"] == "REJECTED"
    assert result["decision"]["reasons_against"] == ["NISON_CONFIRMATION_INSUFFICIENT"]
    assert result["nison"]["status"] == "FAILED"
    assert result["nison"]["rule_summary"] == {
        "PASS": 0,
        "FAIL": 1,
        "NOT_EVALUABLE": 1,
        "OTHER": 0,
    }


def test_only_clean_nison_confirmation_is_executable():
    rows = [
        {"source_rule_id": "NISON_0001", "status": "PASS", "conflict": "neutral"},
        {"source_rule_id": "NISON_0002", "status": "PASS", "conflict": "neutral"},
    ]
    result = evaluate_three_book_decision(**_base(rows))
    assert result["signal"]["direction"] == "BUY"
    assert result["signal"]["status"] == "EXECUTABLE"
    assert result["nison"]["status"] == "CONFIRMED"
    assert result["nison"]["confirmation"] == "CONFIRMED"
