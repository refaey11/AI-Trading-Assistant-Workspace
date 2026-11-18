import unittest
from producer_feature_lineage_contract_v1 import (
    FeatureLineageError, canonical_payload_hash, verify_mtf_feature_lineage)

AS_OF = "2026-11-18T12:00:00Z"

def raw_bar(**changes):
    p = {"symbol":"EURUSD","timeframe":"M5","bar_time_utc":"2026-11-18T11:50:00Z",
         "source":"feed-1","producer":"mt5-raw-v1","open":1.08,"high":1.081,
         "low":1.079,"close":1.0805,"tick_volume":120}
    p.update(changes)
    return {**{k:p[k] for k in ("symbol","timeframe","bar_time_utc","source","producer")},
            "payload":p,"payload_hash":canonical_payload_hash(p)}

def feature(raws):
    first=raws[0]
    p={"symbol":first["symbol"],"timeframe":first["timeframe"],
       "bar_time_utc":first["bar_time_utc"],"source":first["source"],
       "producer":"mtf-feature-v1","feature_name":"M5_trend_regime","value":1}
    return {**{k:p[k] for k in ("symbol","timeframe","bar_time_utc","source","producer")},
       "feature_id":"EURUSD:M5:trend:2026-11-18T11:50:00Z",
       "transform_id":"mtf-trend-regime","transform_version":"1.0.0",
       "computed_at_utc":"2026-11-18T11:51:00Z","payload":p,
       "payload_hash":canonical_payload_hash(p),
       "input_refs":[{"raw_payload_hash":r["payload_hash"],"symbol":r["symbol"],
          "timeframe":r["timeframe"],"bar_time_utc":r["bar_time_utc"]} for r in raws]}

class LineageTests(unittest.TestCase):
    def test_accepts_valid_lineage(self):
        r=raw_bar(); out=verify_mtf_feature_lineage(feature([r]),[r],decision_as_of=AS_OF)
        self.assertEqual(out.transform_id,"mtf-trend-regime")
    def test_hash_is_key_order_independent(self):
        self.assertEqual(canonical_payload_hash({"a":1,"b":2}),canonical_payload_hash({"b":2,"a":1}))
    def test_rejects_tampered_raw_payload(self):
        r=raw_bar(); r["payload"]["close"]=1.09
        with self.assertRaisesRegex(FeatureLineageError,"RAW_BAR_PAYLOAD_HASH_MISMATCH"):
            verify_mtf_feature_lineage(feature([r]),[r],decision_as_of=AS_OF)
    def test_rejects_tampered_feature_payload(self):
        r=raw_bar(); f=feature([r]); f["payload"]["value"]=9
        with self.assertRaisesRegex(FeatureLineageError,"FEATURE_PAYLOAD_HASH_MISMATCH"):
            verify_mtf_feature_lineage(f,[r],decision_as_of=AS_OF)
    def test_rejects_missing_raw_input(self):
        r=raw_bar()
        with self.assertRaisesRegex(FeatureLineageError,"FEATURE_INPUT_RAW_BAR_NOT_FOUND"):
            verify_mtf_feature_lineage(feature([r]),[],decision_as_of=AS_OF)
    def test_rejects_cross_symbol_input(self):
        r=raw_bar(); other=raw_bar(symbol="GBPUSD"); f=feature([r])
        f["input_refs"].append({"raw_payload_hash":other["payload_hash"],"symbol":"GBPUSD",
          "timeframe":"M5","bar_time_utc":other["bar_time_utc"]})
        with self.assertRaisesRegex(FeatureLineageError,"FEATURE_INPUT_SYMBOL_MISMATCH"):
            verify_mtf_feature_lineage(f,[r,other],decision_as_of=AS_OF)
    def test_rejects_cross_timeframe_input(self):
        r=raw_bar(); other=raw_bar(timeframe="H1"); f=feature([r])
        f["input_refs"].append({"raw_payload_hash":other["payload_hash"],"symbol":"EURUSD",
          "timeframe":"H1","bar_time_utc":other["bar_time_utc"]})
        with self.assertRaisesRegex(FeatureLineageError,"FEATURE_INPUT_TIMEFRAME_MISMATCH"):
            verify_mtf_feature_lineage(f,[r,other],decision_as_of=AS_OF)
    def test_rejects_duplicate_refs(self):
        r=raw_bar(); f=feature([r]); f["input_refs"].append(dict(f["input_refs"][0]))
        with self.assertRaisesRegex(FeatureLineageError,"FEATURE_INPUT_REF_DUPLICATE"):
            verify_mtf_feature_lineage(f,[r],decision_as_of=AS_OF)
    def test_rejects_naive_bar_time(self):
        r=raw_bar(bar_time_utc="2026-11-18T11:50:00")
        with self.assertRaisesRegex(FeatureLineageError,"TIMEZONE_AWARE_REQUIRED"):
            verify_mtf_feature_lineage(feature([r]),[r],decision_as_of=AS_OF)
    def test_rejects_future_bar(self):
        r=raw_bar(bar_time_utc="2026-11-18T12:01:00Z")
        with self.assertRaisesRegex(FeatureLineageError,"RAW_BAR_AFTER_DECISION_AS_OF"):
            verify_mtf_feature_lineage(feature([r]),[r],decision_as_of=AS_OF)
    def test_rejects_compute_before_input(self):
        r=raw_bar(); f=feature([r]); f["computed_at_utc"]="2026-11-18T11:40:00Z"
        with self.assertRaisesRegex(FeatureLineageError,"FEATURE_COMPUTED_BEFORE_INPUT_BAR"):
            verify_mtf_feature_lineage(f,[r],decision_as_of=AS_OF)
    def test_rejects_compute_after_decision(self):
        r=raw_bar(); f=feature([r]); f["computed_at_utc"]="2026-11-18T12:01:00Z"
        with self.assertRaisesRegex(FeatureLineageError,"FEATURE_COMPUTED_AFTER_DECISION_AS_OF"):
            verify_mtf_feature_lineage(f,[r],decision_as_of=AS_OF)
    def test_rejects_non_finite_payload(self):
        with self.assertRaisesRegex(FeatureLineageError,"PAYLOAD_NOT_CANONICAL_JSON"):
            canonical_payload_hash({"x":float("nan")})

if __name__ == "__main__": unittest.main()
