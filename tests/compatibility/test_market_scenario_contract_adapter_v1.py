from compatibility.market_scenario_contract_adapter_v1 import normalize_scenario


FIXTURES = [
    {"pair": "EURUSD", "primary_scenario": "NEUTRAL / TWO-SIDED", "decision": "WAIT", "confidence": 0.5, "bullish_score": 0, "bearish_score": 2, "neutral_score": 2},
    {"pair": "GBPUSD", "primary_scenario": "NEUTRAL / TWO-SIDED", "decision": "WAIT", "confidence": 0.5, "bullish_score": 1, "bearish_score": 2, "neutral_score": 3},
    {"pair": "USDJPY", "primary_scenario": "NEUTRAL / TWO-SIDED", "decision": "WAIT", "confidence": 0.5, "bullish_score": 2, "bearish_score": 0, "neutral_score": 2},
]


def test_source_derived_shape_normalizes_without_trade_decision():
    for row in FIXTURES:
        result = normalize_scenario(row)
        assert result.status == "PASS"
        assert result.final_trade_decision is None
        assert result.scenario["decision"] == "WAIT"


def test_missing_field_fails_closed():
    row = dict(FIXTURES[0])
    row.pop("confidence")
    result = normalize_scenario(row)
    assert result.status == "NOT_EVALUABLE"


def test_unknown_scenario_fails_closed():
    row = dict(FIXTURES[0])
    row["primary_scenario"] = "INVENTED_SCENARIO"
    result = normalize_scenario(row)
    assert result.status == "NOT_EVALUABLE"


def test_invalid_numeric_evidence_fails_closed():
    row = dict(FIXTURES[0])
    row["bearish_score"] = "not-a-number"
    result = normalize_scenario(row)
    assert result.status == "NOT_EVALUABLE"
