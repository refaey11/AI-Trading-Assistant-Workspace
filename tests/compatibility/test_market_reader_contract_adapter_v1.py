from compatibility.market_reader_contract_adapter_v1 import normalize_market_reading


def _state():
    return {
        "trend": "BULL_TREND",
        "structure": "INSIDE_RANGE",
        "volatility": "NORMAL",
        "volume": "EXPANSION",
    }


def test_valid_contract_normalizes_without_trade_decision():
    r = normalize_market_reading(
        symbol="GBPUSD",
        timeframe="H1",
        market_state=_state(),
        evidence=[{"type": "trend"}],
        scenarios=[{"scenario": "neutral"}],
        confidence=0.7,
        decision="WAIT",
    )
    assert r.status == "PASS"
    assert r.output["symbol"] == "GBPUSD"
    assert r.output["timeframe"] == "H1"
    assert r.final_trade_decision is None


def test_missing_market_state_fails_closed():
    r = normalize_market_reading(
        symbol="GBPUSD",
        timeframe="H1",
        market_state={"trend": "BULL_TREND"},
    )
    assert r.status == "NOT_EVALUABLE"


def test_invalid_decision_fails_closed():
    r = normalize_market_reading(
        symbol="GBPUSD",
        timeframe="H1",
        market_state=_state(),
        decision="BUY NOW",
    )
    assert r.status == "NOT_EVALUABLE"


def test_confidence_out_of_range_fails_closed():
    r = normalize_market_reading(
        symbol="GBPUSD",
        timeframe="H1",
        market_state=_state(),
        confidence=1.5,
    )
    assert r.status == "NOT_EVALUABLE"
