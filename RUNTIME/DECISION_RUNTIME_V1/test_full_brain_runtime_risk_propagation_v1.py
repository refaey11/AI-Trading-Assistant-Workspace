from datetime import datetime, timezone

from full_brain_runtime_bridge_v1 import run_full_brain_cycle


def base_kwargs():
    return {
        "row": {
            "mtf_trend_score": 0.7,
            "M5_trend_regime": 0.4,
            "M15_trend_regime": 0.3,
            "M30_trend_regime": 0.2,
            "H1_trend_regime": 0.4,
            "H4_trend_regime": 0.5,
            "D1_trend_regime": 0.3,
            "volume_available": True,
            "M5_volume_regime": 0.2,
            "M15_volume_regime": 0.2,
            "M30_volume_regime": 0.1,
            "H1_volume_regime": 0.1,
            "H4_volume_regime": 0.2,
            "D1_volume_regime": 0.2,
        },
        "query_as_of": datetime(2024, 12, 31, tzinfo=timezone.utc),
        "murphy_evidence": {"status": "PASS", "direction": "BULLISH"},
        "nison_evidence": {"confirmation": "CONFIRMED", "contradiction": False},
        "tiz_evidence": {"authoritative": False, "process_state": "NOT_EVALUABLE"},
        "risk_evidence": {
            "authoritative": True,
            "risk_pass": True,
            "stop_loss": 1.2450,
            "take_profit": 1.2600,
            "rr": 3.0,
        },
        "historical_evidence": {"retrieval_status": "PASS", "candidate_count": 10},
        "source_rule_ids": ["MURPHY_0003"],
        "entry_price": 1.25,
        "atr": 0.005,
        "mode": "development",
    }


def test_authoritative_risk_false_cannot_be_upgraded_by_assembler():
    kw = base_kwargs()
    kw["risk_evidence"] = {
        "authoritative": True,
        "risk_pass": False,
        "stop_loss": 1.2450,
        "take_profit": 1.2600,
        "rr": 3.0,
    }
    result = run_full_brain_cycle(**kw)
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["execution_plan"]["reason"] == "risk_gate_not_passed"
