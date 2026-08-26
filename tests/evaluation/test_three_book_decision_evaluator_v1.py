from evaluation.three_book_decision_evaluator_v1 import evaluate_three_book_decision
import evaluation.three_book_decision_evaluator_v1 as evaluator


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


def _full_package(murphy_rows, nison_rows):
    return {
        "schema_version": "GOVERNED_78_RULE_ADAPTER_V1",
        "query_as_of": "2024-12-31T23:00:00Z",
        "mode": "development",
        "murphy": {"rule_count": 34, "rows": murphy_rows, "role": "TECHNICAL_CONTEXT"},
        "nison": {"rule_count": 44, "rows": nison_rows, "role": "CONFIRMATION_OR_CONTRADICTION_ONLY"},
        "receipt": {"all_78_rules_present": True, "murphy_rule_count": 34, "nison_rule_count": 44, "sha256": "test-fixture-receipt"},
        "governance": {"2025_oos_unchanged": False, "synthetic_rules_created": False, "not_evaluable_promoted_to_signal": False, "nison_generates_direction": False, "adapter_generates_direction": False},
        "provenance": {},
    }


def _full_rule_inputs(nison_rows, *, legacy_status="PASS", legacy_direction="BULLISH", bullish_pass=True, bearish_pass=False):
    murphy_rows = [{"source_rule_id": f"MURPHY_{i:04d}", "status": "NOT_EVALUABLE", "direction": "NONE"} for i in range(1, 35)]
    if bullish_pass:
        murphy_rows[2] = {"source_rule_id": "MURPHY_0003", "status": "PASS", "direction": "BULLISH"}
    if bearish_pass:
        murphy_rows[3] = {"source_rule_id": "MURPHY_0004", "status": "PASS", "direction": "BEARISH"}
    package = _full_package(murphy_rows, nison_rows)
    return {
        "brain_assessment": {"directional_bias": "bullish", "confidence": 0.8},
        "murphy_evidence": {"status": legacy_status, "direction": legacy_direction, "evidence_set": {row["source_rule_id"]: row for row in murphy_rows}, "governed_78_package": package},
        "nison_evidence": {"confirmation": "ABSENT", "contradiction": False, "evidence_set": {row["source_rule_id"]: row for row in nison_rows}, "governed_78_package": package},
        "tiz_evidence": {"process_state": "READY"},
        "risk_evidence": {"risk_pass": True, "stop_loss": "1.2700", "take_profit": "1.2800", "rr": "2.0"},
        "source_rule_ids": [row["source_rule_id"] for row in murphy_rows + nison_rows],
        "timestamp": "2024-12-31T23:00:00Z",
    }


def _nison_rows(default_confirmation=""):
    return [{"source_rule_id": f"NISON_{i:04d}", "status": "NOT_EVALUABLE", "confirmation": default_confirmation, "contradiction": False, "direction": ""} for i in range(1, 45)]


def test_full_nison_fail_same_direction_is_not_contradiction(monkeypatch):
    nison_rows = _nison_rows()
    nison_rows[0] = {"source_rule_id": "NISON_0001", "status": "FAIL", "direction": "BULLISH", "confirmation": "", "contradiction": False}
    args = _full_rule_inputs(nison_rows)
    monkeypatch.setattr(evaluator, "_allowed_rule_ids", lambda: set(args["source_rule_ids"]))
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "BUY"


def test_full_nison_opposite_direction_fail_is_contradiction(monkeypatch):
    nison_rows = _nison_rows()
    nison_rows[0] = {"source_rule_id": "NISON_0001", "status": "FAIL", "direction": "BEARISH", "confirmation": "", "contradiction": False}
    args = _full_rule_inputs(nison_rows)
    monkeypatch.setattr(evaluator, "_allowed_rule_ids", lambda: set(args["source_rule_ids"]))
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"
    assert result["decision"]["reasons_against"] == ["NISON_FULL_RULE_CONTRADICTION"]


def test_full_rule_envelope_overrides_legacy_murphy_candidate():
    nison_rows = _nison_rows()
    args = _full_rule_inputs(nison_rows, legacy_status="FAIL", legacy_direction="BEARISH", bullish_pass=True)
    monkeypatch = __import__("pytest").MonkeyPatch()
    try:
        monkeypatch.setattr(evaluator, "_allowed_rule_ids", lambda: set(args["source_rule_ids"]))
        result = evaluate_three_book_decision(**args)
    finally:
        monkeypatch.undo()
    assert result["decision"]["final"] == "BUY"
    assert result["audit"]["full_rule_consumer"]["murphy_directional_pass"] is True


def test_full_rule_envelope_with_no_directional_pass_is_explicitly_blocked(monkeypatch):
    nison_rows = _nison_rows()
    args = _full_rule_inputs(nison_rows, bullish_pass=False)
    monkeypatch.setattr(evaluator, "_allowed_rule_ids", lambda: set(args["source_rule_ids"]))
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"
    assert result["decision"]["reasons_against"] == ["MURPHY_FULL_RULE_NO_DIRECTIONAL_PASS"]


def test_full_rule_bullish_and_bearish_is_explicit_conflict(monkeypatch):
    nison_rows = _nison_rows()
    args = _full_rule_inputs(nison_rows, bullish_pass=True, bearish_pass=True)
    monkeypatch.setattr(evaluator, "_allowed_rule_ids", lambda: set(args["source_rule_ids"]))
    result = evaluate_three_book_decision(**args)
    assert result["decision"]["final"] == "NO_TRADE"
    assert result["decision"]["reasons_against"] == ["MURPHY_FULL_RULE_CONFLICT"]
