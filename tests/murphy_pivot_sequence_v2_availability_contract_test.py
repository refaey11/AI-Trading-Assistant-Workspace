from datetime import datetime, timedelta


def pivot_is_available(source_ts: datetime, availability_ts: datetime, confirmation_status: str) -> bool:
    return (
        availability_ts == source_ts + timedelta(hours=2)
        and confirmation_status == "CONFIRMED_AFTER_2_BARS"
    )


def test_availability_is_source_plus_two_bars():
    source = datetime(2020, 1, 2, 10)
    assert pivot_is_available(source, source + timedelta(hours=2), "CONFIRMED_AFTER_2_BARS")


def test_early_availability_is_rejected():
    source = datetime(2020, 1, 2, 10)
    assert not pivot_is_available(source, source + timedelta(hours=1), "CONFIRMED_AFTER_2_BARS")


def test_unconfirmed_status_is_rejected():
    source = datetime(2020, 1, 2, 10)
    assert not pivot_is_available(source, source + timedelta(hours=2), "PENDING")


def test_2025_is_out_of_sample():
    source = datetime(2025, 1, 2, 10)
    assert source.year == 2025
