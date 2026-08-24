from datetime import datetime, timezone

import pytest

from evidence.ADAPTERS.cme_6b_open_interest_adapter_v1 import (
    adapt_cme_6b_oi,
    latest_available_oi,
    direction,
)


def dt(hour: int, minute: int = 0) -> datetime:
    return datetime(2025, 1, 2, hour, minute, tzinfo=timezone.utc)


def test_rejects_missing_availability_time():
    with pytest.raises(KeyError):
        adapt_cme_6b_oi([
            {"event_time": dt(18), "open_interest": 100000}
        ])


def test_rejects_availability_before_event():
    with pytest.raises(ValueError):
        adapt_cme_6b_oi([
            {"event_time": dt(18), "available_time": dt(17), "open_interest": 100000}
        ])


def test_latest_available_never_uses_future_evidence():
    records = adapt_cme_6b_oi([
        {"event_time": dt(18), "available_time": dt(19), "open_interest": 100000},
        {"event_time": datetime(2025, 1, 3, 18, tzinfo=timezone.utc),
         "available_time": datetime(2025, 1, 3, 19, tzinfo=timezone.utc),
         "open_interest": 101000},
    ])
    assert latest_available_oi(records, dt(18, 30)) is None
    chosen = latest_available_oi(records, dt(19, 30))
    assert chosen is not None
    assert chosen.open_interest == 100000


def test_direction_is_derived_only_from_authoritative_oi():
    records = adapt_cme_6b_oi([
        {"event_time": dt(18), "available_time": dt(19), "open_interest": 100000},
        {"event_time": datetime(2025, 1, 3, 18, tzinfo=timezone.utc),
         "available_time": datetime(2025, 1, 3, 19, tzinfo=timezone.utc),
         "open_interest": 101000},
    ])
    assert direction(records[1], records[0]) == "UP"
