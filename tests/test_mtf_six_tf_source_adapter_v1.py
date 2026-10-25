from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "BACKTEST" / "MTF_SIX_TF_SOURCE_ADAPTER_V1.py"
SPEC = importlib.util.spec_from_file_location("mtf_source_adapter", MODULE_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


class MultiSymbolSourceInspectorTests(unittest.TestCase):
    def test_supported_symbols_are_explicit(self):
        self.assertEqual(
            set(adapter.SUPPORTED_SYMBOLS),
            {"GBPUSD", "EURUSD", "USDCAD", "USDJPY", "XAUUSD"},
        )

    def test_symbol_inference_recognizes_each_supported_symbol(self):
        for symbol in adapter.SUPPORTED_SYMBOLS:
            with self.subTest(symbol=symbol):
                self.assertEqual(adapter.infer_symbol_from_text(f"archive_{symbol}_M1.csv"), symbol)

    def test_symbol_inference_does_not_accept_unknown_six_letter_token(self):
        self.assertIsNone(adapter.infer_symbol_from_text("archive_AUDCAD_M1.csv"))

    def test_timeframe_inference_recognizes_all_declared_timeframes(self):
        for timeframe in adapter.SIX_TF:
            with self.subTest(timeframe=timeframe):
                self.assertEqual(adapter.infer_tf_from_text(f"prices_{timeframe}.csv"), timeframe)

    def test_inspector_fails_closed_on_duplicate_timestamps(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "GBPUSD_H1.csv"
            path.write_text(
                "timestamp,open,high,low,close,symbol\n"
                "2024-01-01T00:00:00Z,1,2,0.5,1.5,GBPUSD\n"
                "2024-01-01T00:00:00Z,1,2,0.5,1.5,GBPUSD\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate timestamp"):
                adapter.inspect_csv(path, max_rows=10)

    def test_inspector_records_symbol_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "EURUSD_H1.csv"
            path.write_text(
                "timestamp,open,high,low,close,symbol\n"
                "2024-01-01T00:00:00Z,1,2,0.5,1.5,EURUSD\n"
                "2024-01-01T01:00:00Z,1.1,2.1,0.6,1.6,EURUSD\n",
                encoding="utf-8",
            )
            result = adapter.inspect_csv(path, max_rows=10)
            self.assertEqual(result["sampled_symbols"], ["EURUSD"])
            self.assertEqual(result["sampled_rows"], 2)
            self.assertEqual(len(result["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
