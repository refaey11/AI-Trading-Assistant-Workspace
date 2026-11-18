import io, csv, unittest
from mt5_raw_capture_contract_v1_3 import CaptureV13Error, validate_raw_bar_v13
from mt5_csv_ingest_v1_3 import EXPECTED_COLUMNS, read_and_validate_csv_v13

def sample(**overrides):
    row = {"symbol":"EURUSD","timeframe":"M5","bar_time_epoch_seconds_raw":1794816000,
      "bar_time_source_clock":"MT5_MQLRATES_DATETIME_RAW","bar_time_utc_status":"UNVERIFIED",
      "terminal_time_server_observed":"2026.11.16 10:05:02",
      "terminal_time_current_server_observed":"2026.11.16 10:05:01",
      "host_gmt_estimate_observed":"2026.11.16 08:05:02",
      "host_local_time_observed":"2026.11.16 10:05:02","broker_server_id":"Demo-Server",
      "source_id":"MT5-Terminal","capture_version":"1.3.0","is_closed":True,
      "open":1.08,"high":1.081,"low":1.079,"close":1.0805,"tick_volume":100,
      "real_volume":0,"spread_points":12,"volume_type":"TICK",
      "observed_server_minus_host_gmt_seconds":7200}
    row.update(overrides); return row

def csv_text(**overrides):
    row = sample(**overrides); row["is_closed"] = "true" if row["is_closed"] else "false"
    stream = io.StringIO(); writer = csv.DictWriter(stream, fieldnames=EXPECTED_COLUMNS)
    writer.writeheader(); writer.writerow(row); return stream.getvalue()

class RawCaptureV13Tests(unittest.TestCase):
    def test_accepts_raw_unverified_timestamp(self):
        bar=validate_raw_bar_v13(sample()); self.assertEqual(bar.timeframe,"M5")
        self.assertEqual(bar.bar_time_epoch_seconds_raw,1794816000); self.assertEqual(len(bar.payload_hash),64)
    def test_supports_all_six_native_timeframes(self):
        for tf in ("M5","M15","M30","H1","H4","D1"): self.assertEqual(validate_raw_bar_v13(sample(timeframe=tf)).timeframe,tf)
    def test_rejects_any_utc_claim(self):
        with self.assertRaisesRegex(CaptureV13Error,"UTC_ALIGNMENT_FIELD_FORBIDDEN"):
            validate_raw_bar_v13(sample(bar_time_utc="2026-11-16T08:00:00Z"))
    def test_rejects_wrong_clock_status(self):
        with self.assertRaisesRegex(CaptureV13Error,"BAR_TIME_MUST_REMAIN_UNVERIFIED"):
            validate_raw_bar_v13(sample(bar_time_utc_status="VERIFIED"))
    def test_rejects_invalid_raw_epoch(self):
        with self.assertRaisesRegex(CaptureV13Error,"RAW_BAR_EPOCH_INVALID"):
            validate_raw_bar_v13(sample(bar_time_epoch_seconds_raw="2026-11-16T08:00:00Z"))
    def test_rejects_unfinished_bar(self):
        with self.assertRaisesRegex(CaptureV13Error,"UNFINISHED_BAR_REJECTED"):
            validate_raw_bar_v13(sample(is_closed=False))
    def test_rejects_offset_wall_clock(self):
        with self.assertRaisesRegex(CaptureV13Error,"INVALID_SERVER_WALL_TIME"):
            validate_raw_bar_v13(sample(terminal_time_server_observed="2026-11-16T10:05:02Z"))
    def test_rejects_invalid_ohlc(self):
        with self.assertRaisesRegex(CaptureV13Error,"OHLC_GEOMETRY_INVALID"):
            validate_raw_bar_v13(sample(high=1.0795))
    def test_csv_ingest_preserves_raw_epoch_and_status(self):
        rows=read_and_validate_csv_v13(io.StringIO(csv_text()))
        self.assertEqual(rows[0]["bar_time_epoch_seconds_raw"],1794816000)
        self.assertEqual(rows[0]["bar_time_utc_status"],"UNVERIFIED")
        self.assertEqual(len(rows[0]["payload_hash"]),64)
    def test_csv_rejects_legacy_utc_schema(self):
        bad=csv_text().replace("bar_time_epoch_seconds_raw","bar_time_mt5_utc",1)
        with self.assertRaisesRegex(CaptureV13Error,"CSV_HEADER_MISMATCH"):
            read_and_validate_csv_v13(io.StringIO(bad))
if __name__ == "__main__": unittest.main()
