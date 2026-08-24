from OOS_2025.decision_brain_profitability_event_adapter_v1 import build_profitability_events


def test_build_event_from_unambiguous_murphy_and_absent_nison():
    rows = [
        {"timestamp": "2025-01-02T01:00:00Z", "rule_id": "MURPHY_0021", "status": "PASS", "direction": "BULLISH"},
        {"timestamp": "2025-01-02T01:00:00Z", "rule_id": "MURPHY_0022", "status": "FAIL", "direction": "BEARISH"},
        {"timestamp": "2025-01-02T01:00:00Z", "rule_id": "NISON_0001", "status": "NOT_EVALUABLE"},
    ]
    market = [{"timestamp": "2025-01-02T01:00:00Z", "close": 1.25, "atr20": 0.005}]

    events = build_profitability_events(
        timestamps=["2025-01-02T01:00:00Z"], rule_stream=rows, market_rows=market
    )

    assert events == [{
        "timestamp": "2025-01-02T01:00:00+00:00",
        "murphy_pass": 1,
        "directional_confirmation": "BULLISH",
        "nison_status": "NOT_EVALUABLE",
        "entry_price": 1.25,
        "atr20": 0.005,
        "candidate_source": "frozen_78_rule_stream",
        "2025_tuning": False,
    }]


def test_nison_contradiction_is_preserved_as_blocking_state():
    rows = [
        {"timestamp": "2025-01-02T02:00:00Z", "rule_id": "MURPHY_0021", "status": "PASS", "direction": "BEARISH"},
        {"timestamp": "2025-01-02T02:00:00Z", "rule_id": "NISON_0001", "status": "FAIL", "reason": "NISON_CONTRADICTION"},
    ]
    market = [{"timestamp": "2025-01-02T02:00:00Z", "close": 1.24, "atr20": 0.004}]

    event = build_profitability_events(
        timestamps=["2025-01-02T02:00:00Z"], rule_stream=rows, market_rows=market
    )[0]

    assert event["murphy_pass"] == 1
    assert event["directional_confirmation"] == "BEARISH"
    assert event["nison_status"] == "CONTRADICTORY"


def test_no_murphy_pass_does_not_create_a_candidate():
    rows = [
        {"timestamp": "2025-01-02T03:00:00Z", "rule_id": "MURPHY_0021", "status": "FAIL", "direction": "BULLISH"},
        {"timestamp": "2025-01-02T03:00:00Z", "rule_id": "NISON_0001", "status": "PASS"},
    ]
    market = [{"timestamp": "2025-01-02T03:00:00Z", "close": 1.23, "atr20": 0.004}]

    event = build_profitability_events(
        timestamps=["2025-01-02T03:00:00Z"], rule_stream=rows, market_rows=market
    )[0]

    assert event["murphy_pass"] == 0
    assert event["directional_confirmation"] == "UNKNOWN"
