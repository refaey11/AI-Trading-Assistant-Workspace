from datetime import date, datetime

from cftc_6b_oi_2025_acquisition import _parse_oi, _parse_report_date, _parse_updated_date, conservative_available_time


def test_parse_report_date():
    html = "FUTURES ONLY POSITIONS AS OF 11/25/25"
    assert _parse_report_date(html) == date(2025, 11, 25)


def test_parse_open_interest_for_096742():
    html = "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE Code-096742\nOPEN INTEREST:      315,550"
    assert _parse_oi(html) == 315550


def test_parse_updated_date():
    assert _parse_updated_date("Updated December 15, 2025") == date(2025, 12, 15)


def test_conservative_availability_boundary():
    value = conservative_available_time(date(2025, 12, 15))
    assert value == datetime(2025, 12, 16, 0, 0, tzinfo=value.tzinfo)


def test_future_report_cannot_be_marked_available_same_day():
    published = date(2025, 12, 15)
    assert conservative_available_time(published).date() > published
