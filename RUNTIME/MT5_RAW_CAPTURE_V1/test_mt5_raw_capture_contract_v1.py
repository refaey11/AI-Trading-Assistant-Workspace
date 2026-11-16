import unittest
from datetime import datetime, timezone
from mt5_raw_capture_contract_v1 import (
    CaptureValidationError, canonical_payload_hash, validate_batch, validate_raw_bar,
)


def sample(**overrides):
    row = {
        "symbol": "GBPUSD", "timeframe": "M5",
        "bar_time_server": "2026-11-16 10:00:00",
        "bar_time_utc": "2026-11-16T08:00:00Z",
        "bar_close_time_utc": "2026-11-16T08:05:00Z",
        "retrieved_at_utc": "2026-11-16T08:05:02Z",
        "source_id": "mt5-terminal-01", "broker_server_id": "broker-demo",
        "timezone_policy_id": "broker-policy-v1", "capture_version": "1.0.0",
        "timezone_conversion_confirmed": True, "is_closed": True,
        "open": 1.25, "high": 1.251, "low": 1.249, "close": 1.2505,
        "tick_volume": 100, "real_volume": 0, "spread_points": 12,
        "volume_type": "TICK",
    }
    row.update(overrides)
    return row


class RawCaptureContractTests(unittest.TestCase):
    def test_accepts_closed_bar_with_explicit_aware_utc(self):
        result = validate_raw_bar(sample())
        self.assertEqual(result.timeframe, "M5")
        self.assertEqual(len(result.payload_hash), 64)

    def test_all_six_timeframes_are_supported(self):
        for tf in ("M5", "M15", "M30", "H1", "H4", "D1"):
            self.assertEqual(validate_raw_bar(sample(timeframe=tf)).timeframe, tf)

    def test_rejects_unknown_timeframe(self):
        with self.assertRaisesRegex(CaptureValidationError, "UNSUPPORTED_TIMEFRAME"):
            validate_raw_bar(sample(timeframe="W1"))

    def test_rejects_naive_utc_timestamp(self):
        with self.assertRaisesRegex(CaptureValidationError, "NAIVE_TIMESTAMP_REJECTED"):
            validate_raw_bar(sample(bar_time_utc="2026-11-16 08:00:00"))

    def test_rejects_unconfirmed_timezone_conversion(self):
        with self.assertRaisesRegex(CaptureValidationError, "TIMEZONE_CONVERSION_NOT_CONFIRMED"):
            validate_raw_bar(sample(timezone_conversion_confirmed=False))

    def test_rejects_unfinished_bar(self):
        with self.assertRaisesRegex(CaptureValidationError, "UNFINISHED_BAR_REJECTED"):
            validate_raw_bar(sample(is_closed=False))

    def test_rejects_bar_not_closed_at_retrieval(self):
        with self.assertRaisesRegex(CaptureValidationError, "BAR_NOT_CLOSED_AT_RETRIEVAL"):
            validate_raw_bar(sample(retrieved_at_utc="2026-11-16T08:04:59Z"))

    def test_rejects_future_bar_as_of(self):
        with self.assertRaisesRegex(CaptureValidationError, "FUTURE_BAR_NOT_AVAILABLE_AS_OF"):
            validate_raw_bar(sample(), query_as_of="2026-11-16T08:04:00Z")

    def test_rejects_invalid_ohlc_geometry(self):
        with self.assertRaisesRegex(CaptureValidationError, "OHLC_GEOMETRY_INVALID"):
            validate_raw_bar(sample(high=1.2495))

    def test_preserves_tick_and_real_volume_as_distinct_fields(self):
        row = sample(tick_volume=100, real_volume=25, volume_type="BOTH")
        self.assertEqual(validate_raw_bar(row).timeframe, "M5")

    def test_identical_duplicate_is_idempotent(self):
        row = sample()
        self.assertEqual(len(validate_batch([row, dict(row)])), 1)

    def test_conflicting_duplicate_is_rejected(self):
        first = sample()
        second = sample(close=1.2507)
        with self.assertRaisesRegex(CaptureValidationError, "CONFLICTING_DUPLICATE_BAR"):
            validate_batch([first, second])

    def test_payload_hash_mismatch_is_rejected(self):
        row = sample(payload_hash="0" * 64)
        with self.assertRaisesRegex(CaptureValidationError, "PAYLOAD_HASH_MISMATCH"):
            validate_raw_bar(row)


if __name__ == "__main__":
    unittest.main()
