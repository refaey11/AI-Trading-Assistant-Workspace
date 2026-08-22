import json
from pathlib import Path

from compatibility.market_state_contract_adapter_v1 import normalize_market_state


FIXTURE = Path(__file__).parents[1] / "fixtures" / "market_state_contract_fixture_2016_2024.json"


def test_source_derived_fixture_normalizes_without_trade_decision():
    rows = json.loads(FIXTURE.read_text())
    assert len(rows) == 5
    for item in rows:
        result = normalize_market_state(item["row"])
        assert result.status == "PASS"
        assert result.final_trade_decision is None
        assert result.market_state["trend"] in {"BULL_TREND", "BEAR_TREND", "TRANSITION", "UNKNOWN"}


def test_zero_volume_fails_closed_for_volume_semantics():
    rows = json.loads(FIXTURE.read_text())
    for item in rows:
        result = normalize_market_state(item["row"])
        assert result.volume_evaluable is False
        assert result.market_state["volume_state"] == "UNKNOWN"


def test_missing_required_field_is_not_evaluable():
    rows = json.loads(FIXTURE.read_text())
    row = dict(rows[0]["row"])
    row.pop("trend")
    result = normalize_market_state(row)
    assert result.status == "NOT_EVALUABLE"


def test_unknown_trend_is_not_evaluable():
    rows = json.loads(FIXTURE.read_text())
    row = dict(rows[0]["row"])
    row["trend"] = "MADE_UP_TREND"
    result = normalize_market_state(row)
    assert result.status == "NOT_EVALUABLE"
