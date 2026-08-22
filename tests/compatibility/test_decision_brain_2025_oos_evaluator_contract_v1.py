from evaluation.decision_brain_2025_oos_evaluator_contract_v1 import validate_oos_batch


def _record():
    return {
        "timestamp": "2025-01-02T10:00:00Z",
        "direction": "NO_TRADE",
        "source_rule_ids": ["NISON_0001"],
        "trading_zone": {"process_state": "READY"},
        "risk_engine": {"risk_pass": True},
    }


def test_accepts_clean_2025_oos_batch():
    result = validate_oos_batch(year=2025, mode="oos_evaluation", records=[_record()])
    assert result["status"] == "ACCEPTED"


def test_rejects_tuning_on_2025():
    result = validate_oos_batch(year=2025, mode="oos_evaluation", records=[_record()], tuning=True)
    assert result["status"] == "REJECTED"
    assert result["reason"] == "OOS_INTEGRITY_VIOLATION"


def test_rejects_wrong_mode():
    result = validate_oos_batch(year=2025, mode="development", records=[_record()])
    assert result["status"] == "REJECTED"
    assert result["reason"] == "2025_OOS_ONLY"


def test_rejects_incomplete_frozen_decision_record():
    bad = _record()
    del bad["risk_engine"]
    result = validate_oos_batch(year=2025, mode="oos_evaluation", records=[bad])
    assert result["status"] == "REJECTED"
    assert result["reason"] == "MISSING_FROZEN_DECISION_FIELDS"
