from __future__ import annotations

from datetime import datetime, timezone

from full_brain_runtime_bridge_v1 import run_full_brain_cycle


def base_kwargs():
    return {
        "row": {"mtf_trend_score": 0.7, "M5_trend_regime": 0.4, "M15_trend_regime": 0.3, "M30_trend_regime": 0.2, "H1_trend_regime": 0.4, "H4_trend_regime": 0.5, "D1_trend_regime": 0.3, "volume_available": True, "M5_volume_regime": 0.2, "M15_volume_regime": 0.2, "M30_volume_regime": 0.1, "H1_volume_regime": 0.1, "H4_volume_regime": 0.2, "D1_volume_regime": 0.2},
        "query_as_of": datetime(2024, 12, 31, tzinfo=timezone.utc),
        "murphy_evidence": {"status": "PASS", "direction": "BULLISH"},
        "nison_evidence": {"confirmation": "CONFIRMED", "contradiction": False},
        "tiz_evidence": {"authoritative": True, "process_state": "READY"},
        "risk_evidence": {"authoritative": True, "risk_pass": True, "stop_loss": "1.2450", "take_profit": "1.2600", "rr": 2.0},
        "historical_evidence": {"retrieval_status": "PASS", "candidate_count": 10},
        "source_rule_ids": ["MURPHY_0003"],
        "entry_price": 1.25,
        "atr": 0.005,
        "mode": "development",
    }


def test_missing_tiz_is_fail_closed():
    kw = base_kwargs()
    kw["tiz_evidence"] = {"authoritative": False, "process_state": "READY"}
    result = run_full_brain_cycle(**kw)
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "TIZ_NOT_PRODUCTION_AUTHORIZED"


def test_missing_risk_is_fail_closed():
    kw = base_kwargs()
    kw["risk_evidence"] = {"authoritative": False, "risk_pass": False}
    result = run_full_brain_cycle(**kw)
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "RISK_NOT_PRODUCTION_AUTHORIZED"


def test_2025_stays_locked():
    kw = base_kwargs()
    kw["query_as_of"] = datetime(2025, 1, 2, tzinfo=timezone.utc)
    result = run_full_brain_cycle(**kw)
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "NOT_EXECUTABLE" or result["reason"] == "2025_OOS_LOCKED"
