from evaluation.frozen_decision_execution_bridge_v1 import (
    evaluate_entry_eligibility,
    validate_oos_context,
)


def test_long_requires_process_and_risk_gates():
    result = evaluate_entry_eligibility({
        "direction": "LONG",
        "source_rule_ids": ["NISON_0001", "MURPHY_0030"],
        "trading_zone": {"process_state": "READY"},
        "risk_engine": {"risk_pass": True},
    })
    assert result["execution_allowed"] is True
    assert result["status"] == "EXECUTABLE"


def test_process_gate_blocks():
    result = evaluate_entry_eligibility({
        "direction": "SHORT",
        "source_rule_ids": ["NISON_0002"],
        "trading_zone": {"process_state": "NOT_READY"},
        "risk_engine": {"risk_pass": True},
    })
    assert result == {"status": "BLOCKED", "execution_allowed": False, "reason": "PROCESS_GATE"}


def test_risk_gate_blocks():
    result = evaluate_entry_eligibility({
        "direction": "LONG",
        "source_rule_ids": ["MURPHY_0031"],
        "trading_zone": {"process_state": "READY"},
        "risk_engine": {"risk_pass": False},
    })
    assert result == {"status": "BLOCKED", "execution_allowed": False, "reason": "RISK_GATE"}


def test_no_trade_stays_no_trade():
    result = evaluate_entry_eligibility({
        "direction": "NO_TRADE",
        "source_rule_ids": [],
        "trading_zone": {"process_state": "READY"},
        "risk_engine": {"risk_pass": True},
    })
    assert result["status"] == "NO_TRADE"
    assert result["execution_allowed"] is False


def test_unknown_rule_is_rejected():
    try:
        evaluate_entry_eligibility({
            "direction": "LONG",
            "source_rule_ids": ["UNKNOWN_RULE_999"],
            "trading_zone": {"process_state": "READY"},
            "risk_engine": {"risk_pass": True},
        })
    except ValueError as exc:
        assert "RULE_REJECTED_OUTSIDE_ALLOWLIST" in str(exc)
    else:
        raise AssertionError("Unknown rule unexpectedly passed the frozen allowlist")


def test_2025_oos_context_accepts_clean_evaluation():
    assert validate_oos_context(year=2025, mode="oos_evaluation") == {
        "status": "ACCEPTED", "year": 2025, "mode": "oos_evaluation"
    }


def test_2025_oos_context_rejects_tuning_and_future_data():
    result = validate_oos_context(
        year=2025,
        mode="oos_evaluation",
        tuning=True,
        future_data=True,
    )
    assert result == {"status": "REJECTED", "reason": "OOS_INTEGRITY_VIOLATION"}
