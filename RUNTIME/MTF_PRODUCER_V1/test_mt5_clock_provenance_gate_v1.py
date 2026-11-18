import unittest
from mt5_clock_provenance_gate_v1 import (
    ClockProvenanceError,
    verify_bar_clock_lineage,
)


def sample(**overrides):
    row = {
        "bar_time_source_clock": "BROKER_SERVER",
        "bar_time_server": "2026-11-18T10:00:00",
        "bar_time_utc": "2026-11-18T08:00:00Z",
        "timezone_offset_seconds": 7200,
        "timezone_policy_id": "BROKER_TZ_POLICY_DEMO_V1",
        "timezone_evidence_ref": "broker-clock-observation-batch-0001",
        "observed_at_utc": "2026-11-18T10:05:00Z",
    }
    row.update(overrides)
    return row


class MT5ClockProvenanceGateTests(unittest.TestCase):
    def test_accepts_explicit_per_bar_offset_and_policy_evidence(self):
        result = verify_bar_clock_lineage(sample())
        self.assertEqual(result.bar_time_utc.isoformat(), "2026-11-18T08:00:00+00:00")
        self.assertEqual(result.timezone_offset_seconds, 7200)

    def test_accepts_negative_offset(self):
        row = sample(
            bar_time_server="2026-11-18T05:00:00",
            bar_time_utc="2026-11-18T08:00:00Z",
            timezone_offset_seconds=-10800,
            observed_at_utc="2026-11-18T08:05:00Z",
        )
        self.assertEqual(verify_bar_clock_lineage(row).bar_time_utc.hour, 8)

    def test_rejects_legacy_utc_label_without_broker_clock_lineage(self):
        row = {
            "bar_time_mt5_utc": "2026-11-18T10:00:00Z",
            "host_gmt_estimate_utc": "2026-11-18T08:05:00Z",
        }
        with self.assertRaisesRegex(ClockProvenanceError, "BAR_TIME_SOURCE_CLOCK_NOT_BROKER_SERVER"):
            verify_bar_clock_lineage(row)

    def test_rejects_missing_broker_server_wall_time(self):
        with self.assertRaisesRegex(ClockProvenanceError, "BAR_TIME_SERVER_MISSING"):
            verify_bar_clock_lineage(sample(bar_time_server=None))

    def test_rejects_offset_bearing_server_wall_time(self):
        with self.assertRaisesRegex(ClockProvenanceError, "BAR_TIME_SERVER_MUST_BE_UNOFFSET_WALL_TIME"):
            verify_bar_clock_lineage(sample(bar_time_server="2026-11-18T10:00:00+02:00"))

    def test_rejects_missing_timezone_policy(self):
        with self.assertRaisesRegex(ClockProvenanceError, "TIMEZONE_POLICY_ID_MISSING"):
            verify_bar_clock_lineage(sample(timezone_policy_id=""))

    def test_rejects_missing_timezone_evidence_reference(self):
        with self.assertRaisesRegex(ClockProvenanceError, "TIMEZONE_EVIDENCE_REF_MISSING"):
            verify_bar_clock_lineage(sample(timezone_evidence_ref=""))

    def test_rejects_utc_arithmetic_mismatch(self):
        with self.assertRaisesRegex(ClockProvenanceError, "BAR_TIME_UTC_OFFSET_MISMATCH"):
            verify_bar_clock_lineage(sample(bar_time_utc="2026-11-18T09:00:00Z"))

    def test_rejects_naive_utc_value(self):
        with self.assertRaisesRegex(ClockProvenanceError, "BAR_TIME_UTC_MUST_BE_TIMEZONE_AWARE"):
            verify_bar_clock_lineage(sample(bar_time_utc="2026-11-18T08:00:00"))

    def test_rejects_naive_observation_time(self):
        with self.assertRaisesRegex(ClockProvenanceError, "OBSERVED_AT_UTC_MUST_BE_TIMEZONE_AWARE"):
            verify_bar_clock_lineage(sample(observed_at_utc="2026-11-18T10:05:00"))

    def test_rejects_observation_before_bar_open(self):
        with self.assertRaisesRegex(ClockProvenanceError, "OBSERVATION_PRECEDES_BAR_OPEN"):
            verify_bar_clock_lineage(sample(observed_at_utc="2026-11-18T07:59:00Z"))

    def test_rejects_boolean_or_out_of_range_offset(self):
        with self.assertRaisesRegex(ClockProvenanceError, "TIMEZONE_OFFSET_SECONDS_INVALID"):
            verify_bar_clock_lineage(sample(timezone_offset_seconds=True))
        with self.assertRaisesRegex(ClockProvenanceError, "TIMEZONE_OFFSET_SECONDS_OUT_OF_RANGE"):
            verify_bar_clock_lineage(sample(timezone_offset_seconds=90000))


if __name__ == "__main__":
    unittest.main()
