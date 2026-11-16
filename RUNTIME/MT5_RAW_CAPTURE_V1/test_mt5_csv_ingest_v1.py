import csv
import io
import unittest

from mt5_csv_ingest_v1 import EXPECTED_COLUMNS, read_and_validate_csv
from mt5_raw_capture_contract_v1 import CaptureValidationError


def csv_text(**overrides):
    row = {
        "symbol": "EURUSD", "timeframe": "M5",
        "bar_time_mt5_utc": "2026-11-16T08:00:00Z",
        "terminal_time_server": "2026.11.16 10:05:02",
        "terminal_time_current_server": "2026.11.16 10:05:01",
        "host_gmt_estimate_utc": "2026-11-16T08:05:02Z",
        "host_local_time_observed": "2026.11.16 10:05:02",
        "broker_server_id": "Broker-Demo-01", "source_id": "MT5-Terminal-01",
        "capture_version": "1.1.2", "is_closed": "true",
        "open": "1.08000", "high": "1.08100", "low": "1.07900",
        "close": "1.08050", "tick_volume": "100", "real_volume": "0",
        "spread_points": "12", "volume_type": "TICK",
        "observed_server_minus_host_gmt_seconds": "7200",
    }
    row.update(overrides)
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=EXPECTED_COLUMNS)
    writer.writeheader()
    writer.writerow(row)
    return stream.getvalue()


class MT5CSVIngestTests(unittest.TestCase):
    def test_parses_and_validates_ea_csv(self):
        records = read_and_validate_csv(io.StringIO(csv_text()))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["symbol"], "EURUSD")
        self.assertIs(records[0]["is_closed"], True)
        self.assertEqual(len(records[0]["payload_hash"]), 64)

    def test_rejects_unfinished_bar(self):
        with self.assertRaisesRegex(CaptureValidationError, "UNFINISHED_BAR_REJECTED"):
            read_and_validate_csv(io.StringIO(csv_text(is_closed="false")))

    def test_rejects_non_numeric_price(self):
        with self.assertRaisesRegex(CaptureValidationError, "NUMERIC_PARSE_FAILED"):
            read_and_validate_csv(io.StringIO(csv_text(open="not-a-price")))

    def test_rejects_header_schema_drift(self):
        source = csv_text().replace("bar_time_mt5_utc", "bar_time_server", 1)
        with self.assertRaisesRegex(CaptureValidationError, "CSV_HEADER_MISMATCH"):
            read_and_validate_csv(io.StringIO(source))

    def test_rejects_negative_volume(self):
        with self.assertRaisesRegex(CaptureValidationError, "NEGATIVE_VOLUME_OR_SPREAD"):
            read_and_validate_csv(io.StringIO(csv_text(tick_volume="-1")))


if __name__ == "__main__":
    unittest.main()
