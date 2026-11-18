from __future__ import annotations

from copy import deepcopy

import RUNTIME.DECISION_RUNTIME_V1.live_decision_runtime_v1 as runtime_module
from RUNTIME.DECISION_RUNTIME_V1.live_decision_runtime_v1 import run_live_event

# Test-only approved fixture policy. Production runtime keeps its allowlist empty.
runtime_module.APPROVED_TIMEZONE_POLICY_IDS = frozenset({"TEST_POLICY_ONLY"})


AS_OF = "2026-11-16T02:00:00Z"
AVAILABLE = "2026-11-16T01:59:00Z"
NISON_IDS = [f"NISON_{i:04d}" for i in range(1, 45)]



def clock_record(timeframe):
    return {
        "timeframe": timeframe,
        "bar_time_source_clock": "BROKER_SERVER",
        "bar_time_server": "2026-11-16T01:55:00",
        "bar_time_utc": "2026-11-16T01:55:00Z",
        "observed_at_utc": "2026-11-16T01:59:00Z",
        "timezone_offset_seconds": 0,
        "timezone_policy_id": "TEST_POLICY_ONLY",
        "timezone_evidence_ref": "fixture://synthetic-clock-evidence",
        "source": "live-mtf-feed-001",
        "producer": "governed-six-timeframe-producer-v1",
        "payload_hash": "a" * 64,
    }


def valid_clock_provenance():
    return {
        "status": "VERIFIED",
        "by_timeframe": {
            timeframe: clock_record(timeframe)
            for timeframe in ("M5", "M15", "M30", "H1", "H4", "D1")
        },
    }


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
            "clock_provenance": valid_clock_provenance(),
            "fields": mtf_fields,
            "dynamic_mtf": {
                "available_timeframes": ["M5", "M15", "M30", "H1", "H4", "D1"],
                "role_assignments": {
                    "macro_context": "D1",
                    "context": "H4",
                    "setup": "H1",
                    "confirmation": "M30",
                    "execution": "M15",
                },
                "evidence_trace": ["source-backed six-timeframe role assignment"],
            },
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



def test_live_runtime_blocks_missing_clock_provenance():
    event = valid_event()
    del event["mtf_evidence"]["clock_provenance"]
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "MTF_CLOCK_PROVENANCE_MISSING"


def test_live_runtime_blocks_unverified_v1_3_raw_clock():
    event = valid_event()
    event["mtf_evidence"]["clock_provenance"]["status"] = "UNVERIFIED"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "MTF_CLOCK_PROVENANCE_NOT_VERIFIED"


def test_live_runtime_requires_clock_lineage_for_all_six_timeframes():
    event = valid_event()
    del event["mtf_evidence"]["clock_provenance"]["by_timeframe"]["D1"]
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "MTF_CLOCK_PROVENANCE_REQUIRES_ALL_SIX_TIMEFRAMES"


def test_live_runtime_rejects_clock_offset_arithmetic_mismatch():
    event = valid_event()
    event["mtf_evidence"]["clock_provenance"]["by_timeframe"]["H1"]["timezone_offset_seconds"] = 3600
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "BAR_TIME_UTC_OFFSET_MISMATCH" in result["reason"]


def test_live_runtime_rejects_future_clock_observation():
    event = valid_event()
    event["mtf_evidence"]["clock_provenance"]["by_timeframe"]["M5"]["observed_at_utc"] = "2026-11-16T02:01:00Z"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "MTF_CLOCK_FUTURE_OBSERVATION_REJECTED:M5" in result["reason"]


def test_live_runtime_rejects_clock_source_mismatch():
    event = valid_event()
    event["mtf_evidence"]["clock_provenance"]["by_timeframe"]["M30"]["source"] = "other-feed"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "MTF_CLOCK_PROVENANCE_SOURCE_MISMATCH:M30" in result["reason"]




def test_live_runtime_blocks_all_clock_policies_when_approval_registry_is_empty(monkeypatch):
    monkeypatch.setattr(runtime_module, "APPROVED_TIMEZONE_POLICY_IDS", frozenset())
    result = run_live_event(valid_event())
    assert result["status"] == "BLOCKED"
    assert "MTF_CLOCK_TIMEZONE_POLICY_NOT_APPROVED" in result["reason"]


def test_live_runtime_rejects_unapproved_timezone_policy_even_if_claimed_verified():
    event = valid_event()
    event["mtf_evidence"]["clock_provenance"]["by_timeframe"]["D1"]["timezone_policy_id"] = "UNREVIEWED_POLICY"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "MTF_CLOCK_TIMEZONE_POLICY_NOT_APPROVED:D1:UNREVIEWED_POLICY" in result["reason"]


def test_live_runtime_returns_clock_provenance_trace():
    result = run_live_event(valid_event())
    assert result["status"] == "SIGNAL_READY"
    assert result["mtf_clock_provenance"]["status"] == "PASS_POLICY_ALLOWLIST"
    assert set(result["mtf_clock_provenance"]["timeframes"]) == {"M5", "M15", "M30", "H1", "H4", "D1"}
    assert result["mtf_clock_provenance"]["policy_approval"] == "REQUIRES_REVIEWED_REPOSITORY_ALLOWLIST"


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


def test_live_runtime_blocks_tiz_process_failure():
    event = valid_event()
    event["tiz_evidence"]["loss_chasing"] = True
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert "TIZ_PROCESS_GATE" in result["reason"]


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

def test_live_runtime_requires_dynamic_mtf_role_binding():
    event = valid_event()
    del event["mtf_evidence"]["dynamic_mtf"]
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "MTF_DYNAMIC_ROLE_ASSIGNMENTS_MISSING"


def test_live_runtime_rejects_inverted_dynamic_mtf_role_order():
    event = valid_event()
    event["mtf_evidence"]["dynamic_mtf"]["role_assignments"]["macro_context"] = "H4"
    event["mtf_evidence"]["dynamic_mtf"]["role_assignments"]["context"] = "D1"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "MTF_DYNAMIC_ROLE_BINDING_NOT_EVALUABLE"


def test_live_runtime_rejects_unsupported_dynamic_mtf_timeframe():
    event = valid_event()
    event["mtf_evidence"]["dynamic_mtf"]["role_assignments"]["setup"] = "H2"
    result = run_live_event(event)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "MTF_DYNAMIC_ROLE_BINDING_NOT_EVALUABLE"


def test_live_runtime_exposes_dynamic_mtf_role_trace_without_direction_authority():
    result = run_live_event(valid_event())
    assert result["status"] == "SIGNAL_READY"
    assert result["dynamic_mtf"]["status"] == "PASS"
    assert result["dynamic_mtf"]["role_timeframes"]["macro_context"] == "D1"
    assert result["dynamic_mtf"]["role_timeframes"]["execution"] == "M15"
    assert result["execution"]["orders_enabled"] is False
