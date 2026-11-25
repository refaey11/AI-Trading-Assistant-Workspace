from __future__ import annotations

from copy import deepcopy

from RUNTIME.DECISION_RUNTIME_V1.live_decision_runtime_v1 import run_live_event


AS_OF = "2026-11-16T02:00:00Z"
AVAILABLE = "2026-11-16T01:59:00Z"
NISON_IDS = [f"NISON_{i:04d}" for i in range(1, 45)]


def valid_event():
    brain_row = {
        "mtf_trend_score": 1.0,
        "M5_trend_regime": 1.0,
        "M15_trend_regime": 1.0,
        "M30_trend_regime": 1.0,
        "H1_trend_regime": 1.0,
        "H4_trend_regime": 1.0,
        "D1_trend_regime": 1.0,
        "volume_available": False,
    }
    mtf_fields = dict(brain_row)
    murphy_rows = [{"source_rule_id": "MURPHY_0021", "status": "PASS"}]
    nison_rows = [{"source_rule_id": rule_id, "status": "PASS"} for rule_id in NISON_IDS]
    return {
        "symbol": "EURUSD",
        "query_as_of": AS_OF,
        "brain_row": brain_row,
        "mtf_evidence": {
            "authoritative": True,
            "source": "live-mtf-feed-001",
            "producer": "governed-six-timeframe-producer-v1",
            "available_at": AVAILABLE,
            "fields": mtf_fields,
        },
        "murphy_evidence": {
            "authoritative": True,
            "source": "live-murphy-feed-001",
            "producer": "murphy-runtime-v1",
            "available_at": AVAILABLE,
            "status": "PASS",
            "direction": "BUY",
            "pass_rule_id": "MURPHY_0021",
            "directional_source_rule_id": "MURPHY_0021",
            "rows": murphy_rows,
        },
        "nison_evidence": {
            "authoritative": True,
            "source": "live-nison-feed-001",
            "producer": "nison-44-runtime-v1",
            "available_at": AVAILABLE,
            "confirmation": "CONFIRMED",
            "contradiction": False,
            "rows": nison_rows,
        },
        "source_rule_ids": ["MURPHY_0021", *NISON_IDS],
        "risk_inputs": {
            "authoritative": True,
            "source": "mt5-account-and-risk-snapshot-001",
            "producer": "mt5-risk-snapshot-v1",
            "available_at": AVAILABLE,
            "direction": "BUY",
            "entry_price": 1.2500,
            "stop_loss": 1.2485,
            "take_profit": 1.2545,
            "atr": 0.0020,
            "equity": 10000.0,
            "peak_equity": 10000.0,
            "prior_loss_streak": 0,
        },
        "tiz_evidence": {
            "authoritative": True,
            "source": "operator-process-check-001",
            "producer": "tiz-process-gate-v1",
            "available_at": AVAILABLE,
            "rule_adherence": True,
            "risk_accepted": True,
            "impulse_override": False,
            "loss_chasing": False,
            "revenge_trade": False,
        },
        "historical_evidence": {
            "similarity": {"predicted_return": -999.0},
            "memory_role": "EVIDENCE_ONLY",
        },
    }


def test_live_event_uses_existing_brain_and_returns_signal_only():
    result = run_live_event(valid_event())
    assert result["status"] == "SIGNAL_READY"
    assert result["decision"] == "BUY"
    assert result["risk"]["rr"] == 3.0
    assert result["execution"]["orders_enabled"] is False
    assert result["execution"]["broker_volume"] is None
    assert result["historical_memory"]["passed_to_brain_for_direction"] is False


def test_live_runtime_does_not_rescale_aggregate_mtf_score():
    event = valid_event()
    event["brain_row"]["mtf_trend_score"] = 6.0
    event["mtf_evidence"]["fields"]["mtf_trend_score"] = 6.0
    result = run_live_event(event)
    assert result["status"] == "SIGNAL_READY"


def test_live_runtime_rejects_naive_timestamp():
    event = valid_event()
    event["query_as_of"] = "2026-11-16T02:00:00"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "NAIVE_TIMESTAMP_REJECTED" in result["reason"]


def test_live_runtime_keeps_2025_oos_locked():
    event = valid_event()
    event["query_as_of"] = "2025-12-31T23:59:00Z"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "2025_OOS" in result["reason"]


def test_live_runtime_rejects_future_source_evidence():
    event = valid_event()
    event["mtf_evidence"]["available_at"] = "2026-11-16T02:01:00Z"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "FUTURE_EVIDENCE_NOT_AVAILABLE" in result["reason"]


def test_live_runtime_rejects_mtf_source_brain_row_mismatch():
    event = valid_event()
    event["mtf_evidence"]["fields"]["H4_trend_regime"] = -1.0
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "MTF_BRAIN_ROW_SOURCE_MISMATCH" in result["reason"]


def test_live_runtime_rejects_two_risk_reward():
    event = valid_event()
    event["risk_inputs"]["take_profit"] = 1.2530
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "RR_BELOW_CURRENT_CANONICAL_MINIMUM" in result["reason"]


def test_live_runtime_blocks_nison_contradiction():
    event = valid_event()
    event["nison_evidence"]["contradiction"] = True
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "NISON_CONTRADICTION"


def test_live_runtime_tiz_absent_is_non_blocking_metadata():
    event = valid_event()
    expected = run_live_event(event)
    del event["tiz_evidence"]
    result = run_live_event(event)
    assert result["status"] == expected["status"]
    assert result["decision"] == expected["decision"]
    assert result["brain"]["confidence"] == expected["brain"]["confidence"]
    assert result["risk"] == expected["risk"]
    assert result["tiz"]["state"] == "NOT_EVALUABLE_METADATA_ONLY"


def test_live_runtime_tiz_failed_state_is_non_blocking_metadata():
    event = valid_event()
    expected = run_live_event(event)
    event["tiz_evidence"] = {
        "loss_chasing": True,
        "impulse_override": True,
        "rule_adherence": False,
        "risk_accepted": False,
    }
    result = run_live_event(event)
    assert result["status"] == expected["status"]
    assert result["decision"] == expected["decision"]
    assert result["brain"]["confidence"] == expected["brain"]["confidence"]
    assert result["risk"] == expected["risk"]
    assert result["tiz"]["loss_chasing"] is True
    assert result["tiz"]["role"] == "OPTIONAL_AUDIT_METADATA_ONLY"


def test_live_runtime_malformed_tiz_is_non_blocking_metadata():
    event = valid_event()
    expected = run_live_event(event)
    event["tiz_evidence"] = "not-an-envelope"
    result = run_live_event(event)
    assert result["status"] == expected["status"]
    assert result["decision"] == expected["decision"]
    assert result["brain"]["confidence"] == expected["brain"]["confidence"]
    assert result["risk"] == expected["risk"]
    assert result["tiz"]["state"] == "UNPARSEABLE_METADATA_ONLY"


def test_live_runtime_tiz_cannot_authorize_failed_risk():
    event = valid_event()
    event["risk_inputs"]["take_profit"] = 1.2530
    event["tiz_evidence"] = {
        "rule_adherence": True,
        "risk_accepted": True,
        "impulse_override": False,
        "loss_chasing": False,
        "revenge_trade": False,
    }
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "RR_BELOW_CURRENT_CANONICAL_MINIMUM" in result["reason"]


def test_live_runtime_rejects_missing_mtf_field_without_defaulting():
    event = valid_event()
    del event["brain_row"]["D1_trend_regime"]
    del event["mtf_evidence"]["fields"]["D1_trend_regime"]
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "brain_row.D1_trend_regime" in result["reason"]


def test_live_runtime_rejects_murphy_risk_direction_conflict():
    event = valid_event()
    event["risk_inputs"]["direction"] = "SELL"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "MURPHY_RISK_DIRECTION_CONFLICT"
