from existing_oi_bridge_v1 import adapt_row


def test_available_existing_oi_row():
    row = {
        "bar_close_timestamp": "2024-01-09T00:00:00+00:00",
        "safe_availability_timestamp": "2024-01-09T00:00:00+00:00",
        "oi_direction": "UP",
        "open_interest": "120000",
        "oi_change": "1500",
    }
    out = adapt_row(row, source_file="GBPUSD_H1_OI_ALIGNED_2020_2024.csv")
    assert out["status"] == "AVAILABLE"
    assert out["quality"] == "AUTHORITATIVE"
    assert out["value"]["oi_direction"] == "UP"
    assert out["source"] == "CFTC_FUTURES_ONLY"
    assert out["instrument"] == "GBP_FUTURES_096742"


def test_missing_oi_fails_closed():
    row = {
        "bar_close_timestamp": "2024-01-09T00:00:00+00:00",
        "safe_availability_timestamp": "2024-01-09T00:00:00+00:00",
        "oi_direction": "",
        "open_interest": "",
        "oi_change": "",
    }
    out = adapt_row(row, source_file="GBPUSD_H1_OI_ALIGNED_2020_2024.csv")
    assert out["status"] == "NOT_EVALUABLE"
    assert out["quality"] == "MISSING"


def test_future_availability_is_rejected():
    row = {
        "bar_close_timestamp": "2024-01-09T00:00:00+00:00",
        "safe_availability_timestamp": "2024-01-09T01:00:00+00:00",
        "oi_direction": "UP",
        "open_interest": "120000",
        "oi_change": "1500",
    }
    out = adapt_row(row, source_file="GBPUSD_H1_OI_ALIGNED_2020_2024.csv")
    assert out["status"] == "NOT_AVAILABLE"
    assert out["quality"] == "INVALID"
