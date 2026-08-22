from compatibility.scenario_engine_contract_adapter_v1 import normalize_scenario


def source_shape_record():
    return {
        "market_state": {
            "pair": "GBPUSD",
            "timestamp": "2025-12-31 16:00:00+00:00",
            "close": 1.334,
            "trend": "TRANSITION",
            "structure": "INSIDE_RANGE",
            "volume": "CONTRACTION",
            "volatility": "NORMAL",
            "location": "NEAR_RESISTANCE",
            "interpretation": "transition structure; volume contraction",
        },
        "scenario_analysis": {
            "scores": {"bullish": 1, "bearish": 2, "neutral": 3},
            "primary_scenario": "NEUTRAL / TWO-SIDED",
            "decision": "WAIT",
            "confidence": 0.5,
            "bullish_evidence": [],
            "bearish_evidence": [],
            "bullish_invalidation": [],
            "bearish_invalidation": [],
            "required_confirmation": [],
        },
    }


def test_source_shape_normalizes_without_decision_generation():
    result = normalize_scenario(source_shape_record())
    assert result.status == "PASS"
    assert result.scenario["oos_status"] == "OOS_2025_READ_ONLY"
    assert result.scenario["source_decision"] == "WAIT"
    assert result.scenario["final_trade_decision"] is None
    assert result.scenario["execution_fields_generated"] is False


def test_missing_required_scenario_field_fails_closed():
    record = source_shape_record()
    del record["scenario_analysis"]["required_confirmation"]
    result = normalize_scenario(record)
    assert result.status == "NOT_EVALUABLE"
    assert result.scenario == {}
