import copy
import math
import unittest

from confirmed_pivot_consumer_contract_oracle import validate_synthetic_consumer_contract


def fixture():
    stream = {
        "contract_version": "synthetic.consumer.v1",
        "producer_name": "synthetic-pivot-producer",
        "producer_version": "0.0-test",
        "schema_version": "synthetic.pivot.v1",
        "symbol": "GBPUSD",
        "timeframe": "M5",
        "source_namespace": "synthetic-feed",
        "identity_model": "MODEL_A_SYNTHETIC",
        "detector_config_id": "synthetic-config-r3",
        "precision_evidence_ref": "fixture-precision",
        "clock_evidence_ref": "fixture-clock",
        "continuity_evidence_ref": "fixture-continuity",
        "fixture_mode": True,
    }
    history = []
    for i in range(12):
        history.append({
            "bar_id": f"bar-{i}", "index": i, "symbol": "GBPUSD",
            "timeframe": "M5", "source_namespace": "synthetic-feed",
            "open": 10.0, "high": 12.0 + i, "low": 8.0 - i,
            "close": 10.5, "completed": True,
        })
    bars = copy.deepcopy(history[6:12])
    pivot = {
        "pivot_id": "pivot-high-2", "kind": "HIGH", "price": 14.0,
        "source_bar_id": "bar-2", "source_index": 2,
        "final_confirming_bar_id": "bar-5", "final_confirming_index": 5,
        "right_window": 3, "available_index": 5,
        "symbol": "GBPUSD", "timeframe": "M5",
        "source_namespace": "synthetic-feed",
        "producer_name": "synthetic-pivot-producer",
        "producer_version": "0.0-test", "schema_version": "synthetic.pivot.v1",
        "detector_config_id": "synthetic-config-r3",
        "confirmation_status": "CONFIRMED",
        "precision_evidence_ref": "fixture-precision",
        "clock_evidence_ref": "fixture-clock",
        "continuity_evidence_ref": "fixture-continuity",
    }
    return stream, bars, history, pivot


class ConfirmedPivotConsumerContractTests(unittest.TestCase):
    def validate(self, stream, bars, history, pivot, snapshot=8):
        return validate_synthetic_consumer_contract(
            stream=stream, bars=bars, source_history=history,
            pivots=[pivot], decision_snapshot_index=snapshot,
        )

    def test_valid_pre_window_pivot_is_accepted_as_synthetic_warm_start(self):
        stream, bars, history, pivot = fixture()
        out = self.validate(stream, bars, history, pivot)
        self.assertEqual(out["status"], "SYNTHETIC_STRUCTURAL_CHECKS_PASSED")
        self.assertEqual(out["accepted_pivot_ids"], ["pivot-high-2"])
        self.assertFalse(out["production_eligible"])

    def test_legacy_pr139_minimal_pivot_payload_is_rejected(self):
        stream, bars, history, _ = fixture()
        legacy = {"pivot_id": "old", "kind": "HIGH", "price": 14.0,
                  "source_bar_index": 2, "available_bar_index": 5,
                  "confirmation_status": "CONFIRMED"}
        with self.assertRaisesRegex(ValueError, "record is incomplete"):
            self.validate(stream, bars, history, legacy)

    def test_cross_symbol_timeframe_or_source_namespace_is_rejected(self):
        for field, value in (("symbol", "EURUSD"), ("timeframe", "H1"),
                             ("source_namespace", "other-feed")):
            stream, bars, history, pivot = fixture()
            pivot[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "not bound"):
                self.validate(stream, bars, history, pivot)

    def test_pivot_source_price_must_match_original_high(self):
        stream, bars, history, pivot = fixture()
        pivot["price"] = 999.0
        with self.assertRaisesRegex(ValueError, "does not equal"):
            self.validate(stream, bars, history, pivot)

    def test_configured_right_window_is_not_a_universal_two_bar_rule(self):
        stream, bars, history, pivot = fixture()
        self.assertTrue(self.validate(stream, bars, history, pivot)["accepted_pivot_ids"])
        pivot["right_window"] = 2
        with self.assertRaisesRegex(ValueError, "right window"):
            self.validate(stream, bars, history, pivot)

    def test_pivot_cannot_be_used_before_final_confirming_bar(self):
        stream, bars, history, pivot = fixture()
        pivot["available_index"] = 4
        with self.assertRaisesRegex(ValueError, "availability must equal"):
            self.validate(stream, bars, history, pivot)

    def test_pivot_after_decision_snapshot_is_rejected(self):
        stream, bars, history, pivot = fixture()
        with self.assertRaisesRegex(ValueError, "not yet available"):
            self.validate(stream, bars, history, pivot, snapshot=4)

    def test_missing_source_or_confirming_identity_is_rejected(self):
        for field in ("source_bar_id", "final_confirming_bar_id"):
            stream, bars, history, pivot = fixture()
            pivot[field] = "missing"
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "identity is missing"):
                self.validate(stream, bars, history, pivot)

    def test_source_index_must_match_source_identity(self):
        stream, bars, history, pivot = fixture()
        pivot["source_index"] = 3
        pivot["right_window"] = 2
        with self.assertRaisesRegex(ValueError, "source index"):
            self.validate(stream, bars, history, pivot)

    def test_boolean_indices_and_prices_are_rejected(self):
        for field, value in (("source_index", True), ("right_window", False),
                             ("available_index", True), ("price", True)):
            stream, bars, history, pivot = fixture()
            pivot[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.validate(stream, bars, history, pivot)

    def test_nan_and_infinite_pivot_prices_are_rejected(self):
        for value in (math.nan, math.inf, -math.inf):
            stream, bars, history, pivot = fixture()
            pivot["price"] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "finite"):
                self.validate(stream, bars, history, pivot)

    def test_mismatched_evidence_references_are_rejected(self):
        for field in ("precision_evidence_ref", "clock_evidence_ref", "continuity_evidence_ref"):
            stream, bars, history, pivot = fixture()
            pivot[field] = "different-fixture-ref"
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "evidence references"):
                self.validate(stream, bars, history, pivot)

    def test_non_synthetic_oracle_use_is_rejected(self):
        stream, bars, history, pivot = fixture()
        stream["fixture_mode"] = False
        with self.assertRaisesRegex(ValueError, "synthetic fixtures only"):
            self.validate(stream, bars, history, pivot)

    def test_duplicate_pivot_ids_are_rejected(self):
        stream, bars, history, pivot = fixture()
        with self.assertRaisesRegex(ValueError, "pivot IDs must be unique"):
            validate_synthetic_consumer_contract(
                stream=stream, bars=bars, source_history=history,
                pivots=[pivot, copy.deepcopy(pivot)], decision_snapshot_index=8,
            )

    def test_output_never_claims_production_or_provenance_authentication(self):
        stream, bars, history, pivot = fixture()
        out = self.validate(stream, bars, history, pivot)
        self.assertFalse(out["production_eligible"])
        self.assertFalse(out["source_identity_authenticated"])
        self.assertFalse(out["clock_authenticated"])
        self.assertFalse(out["continuity_authenticated"])


if __name__ == "__main__":
    unittest.main()
