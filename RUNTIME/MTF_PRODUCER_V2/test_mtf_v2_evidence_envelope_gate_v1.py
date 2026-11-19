import hashlib
import unittest

from mtf_v2_evidence_envelope_gate_v1 import (
    EvidenceEnvelopeError, REQUIRED_TIMEFRAMES,
    validate_timeframe_envelope, validate_six_timeframe_bundle,
)


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def envelope(tf="M5", symbol="GBPUSD", available="2024-01-01T00:05:00+00:00"):
    return {
        "symbol": symbol,
        "timeframe": tf,
        "producer_version": "2.0.0",
        "schema_version": "mtf_v2.structure.v1",
        "source_payload_sha256": digest("source"),
        "clock_policy_id": "broker-clock-policy-ref",
        "clock_evidence_sha256": digest("clock-evidence"),
        "rows": [{
            "bar_index": 1,
            "bar_open_time": "2024-01-01T00:00:00+00:00",
            "bar_close_time": "2024-01-01T00:05:00+00:00",
            "available_at": available,
        }],
    }


DECISION = "2024-01-01T00:06:00+00:00"


class EvidenceEnvelopeGateTests(unittest.TestCase):
    def test_valid_envelope_is_not_authentication_or_production_approval(self):
        result = validate_timeframe_envelope(envelope(), decision_time=DECISION)
        self.assertEqual(result["status"], "STRUCTURALLY_VALID_NOT_AUTHENTICATED")
        self.assertFalse(result["production_eligible"])
        self.assertTrue(result["authentication_required"])

    def test_rejects_naive_timestamp(self):
        item = envelope()
        item["rows"][0]["bar_open_time"] = "2024-01-01T00:00:00"
        with self.assertRaises(EvidenceEnvelopeError):
            validate_timeframe_envelope(item, decision_time=DECISION)

    def test_rejects_future_availability(self):
        item = envelope(available="2024-01-01T00:07:00+00:00")
        with self.assertRaises(EvidenceEnvelopeError):
            validate_timeframe_envelope(item, decision_time=DECISION)

    def test_rejects_availability_before_close(self):
        item = envelope(available="2024-01-01T00:04:59+00:00")
        with self.assertRaises(EvidenceEnvelopeError):
            validate_timeframe_envelope(item, decision_time=DECISION)

    def test_rejects_bad_hash(self):
        item = envelope()
        item["source_payload_sha256"] = "not-a-hash"
        with self.assertRaises(EvidenceEnvelopeError):
            validate_timeframe_envelope(item, decision_time=DECISION)

    def test_rejects_missing_clock_evidence(self):
        item = envelope()
        del item["clock_evidence_sha256"]
        with self.assertRaises(EvidenceEnvelopeError):
            validate_timeframe_envelope(item, decision_time=DECISION)

    def test_rejects_non_contiguous_indices(self):
        item = envelope()
        item["rows"].append({
            "bar_index": 3,
            "bar_open_time": "2024-01-01T00:05:00+00:00",
            "bar_close_time": "2024-01-01T00:10:00+00:00",
            "available_at": "2024-01-01T00:10:00+00:00",
        })
        with self.assertRaises(EvidenceEnvelopeError):
            validate_timeframe_envelope(item, decision_time="2024-01-01T00:11:00+00:00")

    def test_requires_exact_six_timeframe_coverage(self):
        items = [envelope(tf) for tf in REQUIRED_TIMEFRAMES[:-1]]
        with self.assertRaises(EvidenceEnvelopeError):
            validate_six_timeframe_bundle(items, decision_time=DECISION)

    def test_rejects_duplicate_timeframe(self):
        items = [envelope(tf) for tf in REQUIRED_TIMEFRAMES]
        items[-1] = envelope("H4")
        with self.assertRaises(EvidenceEnvelopeError):
            validate_six_timeframe_bundle(items, decision_time=DECISION)

    def test_rejects_cross_symbol_bundle(self):
        items = [envelope(tf) for tf in REQUIRED_TIMEFRAMES]
        items[-1] = envelope("D1", symbol="EURUSD")
        with self.assertRaises(EvidenceEnvelopeError):
            validate_six_timeframe_bundle(items, decision_time=DECISION)

    def test_bundle_is_never_production_authorized(self):
        result = validate_six_timeframe_bundle(
            [envelope(tf) for tf in REQUIRED_TIMEFRAMES], decision_time=DECISION
        )
        self.assertEqual(result["timeframes"], list(REQUIRED_TIMEFRAMES))
        self.assertFalse(result["production_eligible"])
        self.assertTrue(result["authentication_required"])


if __name__ == "__main__":
    unittest.main()
