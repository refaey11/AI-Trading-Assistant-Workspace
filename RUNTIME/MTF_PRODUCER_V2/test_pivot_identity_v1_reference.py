import unittest

from RUNTIME.MTF_PRODUCER_V2.pivot_identity_v1_reference import (
    DOMAIN_SEPARATOR,
    canonical_payload_bytes,
    make_pivot_id,
)


BASE = {
    "config_fingerprint": "a" * 64,
    "detector_version": "MTF_PIVOT_V2",
    "pivot_kind": "HIGH",
    "source_bar_id": "synthetic-bar-0001",
    "symbol": "GBPUSD",
    "timeframe": "M5",
}


class PivotIdentityReferenceTests(unittest.TestCase):
    def test_golden_high_vector(self):
        self.assertEqual(
            make_pivot_id(BASE),
            "mpv2_085ff8182376fbe8110fbd596eb032e328fb1774976f4bec89682643850f2430",
        )

    def test_golden_low_vector_is_distinct(self):
        low = dict(BASE, pivot_kind="LOW")
        self.assertEqual(
            make_pivot_id(low),
            "mpv2_7325cf0f9aaa9c9f64815474c52e16041df70a559967c2eee43e40ee3522cdca",
        )
        self.assertNotEqual(make_pivot_id(BASE), make_pivot_id(low))

    def test_canonical_key_order_is_stable(self):
        reversed_fields = dict(reversed(list(BASE.items())))
        self.assertEqual(canonical_payload_bytes(BASE), canonical_payload_bytes(reversed_fields))
        self.assertEqual(make_pivot_id(BASE), make_pivot_id(reversed_fields))

    def test_each_identity_input_changes_payload(self):
        for key in BASE:
            changed = dict(BASE)
            changed[key] = ("b" * 64) if key == "config_fingerprint" else changed[key] + "_changed"
            with self.subTest(field=key):
                self.assertNotEqual(make_pivot_id(BASE), make_pivot_id(changed))

    def test_rejects_missing_extra_empty_and_wrong_types(self):
        for fields in (
            {k: v for k, v in BASE.items() if k != "symbol"},
            dict(BASE, extra="no"),
            dict(BASE, symbol=""),
            dict(BASE, timeframe=None),
            dict(BASE, pivot_kind="MIDDLE"),
            dict(BASE, config_fingerprint="A" * 64),
        ):
            with self.subTest(fields=fields):
                with self.assertRaises(ValueError):
                    make_pivot_id(fields)

    def test_domain_separation_is_explicit(self):
        self.assertEqual(DOMAIN_SEPARATOR, b"MTF_PIVOT_V2_ID_V1\n")
        self.assertTrue(make_pivot_id(BASE).startswith("mpv2_"))

    def test_no_silent_normalization(self):
        spaced = dict(BASE, source_bar_id=" synthetic-bar-0001")
        self.assertNotEqual(make_pivot_id(BASE), make_pivot_id(spaced))


if __name__ == "__main__":
    unittest.main()
