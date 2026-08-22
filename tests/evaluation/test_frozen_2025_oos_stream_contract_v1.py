import pytest

from evaluation.frozen_2025_oos_stream_contract_v1 import (
    OOSStreamError,
    summarize,
    validate_event_stream,
)

HASH = "bac280e9537c0eed20f51297a64e8c05f12a54775e5a32ad417d05cd71e0bbed"


def event(**overrides):
    row = {
        "timestamp": "2025-01-02T10:00:00Z",
        "mode": "oos_evaluation",
        "decision": "BUY",
        "entry_price": "1.2500",
        "exit_price": "1.2520",
        "outcome_r": "1.5",
        "cost_r": "0.1",
        "source_rule_ids": "MURPHY_0003,NISON_0001",
        "tiz_process_state": "READY",
        "risk_pass": "true",
        "data_source_hash": HASH,
    }
    row.update(overrides)
    return row


def test_clean_2025_event_passes():
    rows = validate_event_stream([event()], expected_data_source_hash=HASH)
    assert rows[0]["net_r"] == "1.4"


def test_wrong_year_is_rejected():
    with pytest.raises(OOSStreamError, match="outside 2025"):
        validate_event_stream([event(timestamp="2024-12-31T23:00:00Z")], expected_data_source_hash=HASH)


def test_future_data_is_rejected():
    with pytest.raises(OOSStreamError, match="outside 2025"):
        validate_event_stream([event(timestamp="2026-01-01T00:00:00Z")], expected_data_source_hash=HASH)


def test_non_oos_mode_is_rejected():
    with pytest.raises(OOSStreamError, match="mode must be oos_evaluation"):
        validate_event_stream([event(mode="development")], expected_data_source_hash=HASH)


def test_hash_mismatch_is_rejected():
    with pytest.raises(OOSStreamError, match="fingerprint mismatch"):
        validate_event_stream([event(data_source_hash="wrong")], expected_data_source_hash=HASH)


def test_unknown_rule_is_rejected_for_executable_decision():
    with pytest.raises(OOSStreamError, match="rule allowlist rejection"):
        validate_event_stream([event(source_rule_ids="MURPHY_9999")], expected_data_source_hash=HASH)


def test_failed_risk_is_rejected_for_executable_decision():
    with pytest.raises(OOSStreamError, match="risk_pass=true"):
        validate_event_stream([event(risk_pass="false")], expected_data_source_hash=HASH)


def test_not_ready_tiz_is_rejected_for_executable_decision():
    with pytest.raises(OOSStreamError, match="READY TIZ"):
        validate_event_stream([event(tiz_process_state="NOT_READY")], expected_data_source_hash=HASH)


def test_duplicate_timestamp_is_rejected():
    with pytest.raises(OOSStreamError, match="duplicate timestamp"):
        validate_event_stream([event(), event()], expected_data_source_hash=HASH)


def test_summary_uses_net_r_after_costs():
    rows = validate_event_stream(
        [
            event(timestamp="2025-01-02T10:00:00Z", outcome_r="1.5", cost_r="0.1"),
            event(timestamp="2025-01-02T11:00:00Z", decision="SELL", outcome_r="-1.0", cost_r="0.1"),
        ],
        expected_data_source_hash=HASH,
    )
    result = summarize(rows)
    assert result["events"] == 2
    assert result["wins"] == 1
    assert result["losses"] == 1
    assert result["total_r"] == pytest.approx(0.3)
    assert result["expectancy_r"] == pytest.approx(0.15)
