from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "BACKTEST"))

from GOVERNED_SOURCE_INPUT_PREFLIGHT_V1 import MTF_NUMERIC_FIELDS, run_preflight


def write_csv(path: Path, columns: list[str], rows: list[dict[str, str]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return path


class GovernedSourceInputPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.inputs = self._valid_inputs()

    def tearDown(self):
        self.tmp.cleanup()

    def _valid_inputs(self):
        result = {}
        h1_rows = []
        market_rows = []
        mtf_rows = []
        for year in range(2016, 2025):
            ts = f"{year}-06-01T12:00:00+00:00"
            h1_rows.append({"timestamp": ts, "open": "1.2500", "high": "1.2600", "low": "1.2400", "close": "1.2550"})
            market_rows.append({"timestamp": ts, "trend": "BULL_TREND"})
            mtf_row = {"timestamp": ts}
            mtf_row.update({field: "0.5" for field in MTF_NUMERIC_FIELDS})
            mtf_rows.append(mtf_row)

        result["h1"] = write_csv(self.root / "h1.csv", ["timestamp", "open", "high", "low", "close"], h1_rows)
        result["market_state"] = write_csv(self.root / "market.csv", ["timestamp", "trend"], market_rows)
        result["mtf"] = write_csv(self.root / "mtf.csv", ["timestamp", *MTF_NUMERIC_FIELDS], mtf_rows)

        evidence_rows = [
            {"timestamp": "2016-06-01T12:00:00+00:00"},
            {"timestamp": "2024-06-01T12:00:00+00:00"},
        ]
        result["murphy"] = write_csv(
            self.root / "murphy.csv",
            ["timestamp", "status", "direction", "source_rule_id"],
            [{**r, "status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0021"} for r in evidence_rows],
        )
        result["nison"] = write_csv(
            self.root / "nison.csv",
            ["timestamp", "status", "direction", "rule_id"],
            [{**r, "status": "PASS", "direction": "BULLISH", "rule_id": "NISON_0001"} for r in evidence_rows],
        )
        result["historical_context"] = write_csv(
            self.root / "hc.csv",
            ["timestamp", "context_signature"],
            [{**r, "context_signature": "sig"} for r in evidence_rows],
        )
        result["historical_outcome"] = write_csv(
            self.root / "ho.csv",
            ["timestamp", "context_signature"],
            [{**r, "context_signature": "sig"} for r in evidence_rows],
        )
        return result

    def run_gate(self):
        return run_preflight(self.inputs, self.root / "out" / "manifest.json")

    def test_clean_inputs_pass_shape_only(self):
        report = self.run_gate()
        self.assertEqual(report["status"], "PASS_INPUT_PREFLIGHT_ONLY")
        self.assertFalse(report["promotion_allowed"])
        self.assertEqual(report["checks_not_performed"]["full_backtest"], "NOT_RUN")

    def test_h1_2025_rows_are_counted_but_excluded(self):
        path = self.inputs["h1"]
        with path.open("a", encoding="utf-8") as handle:
            handle.write("2025-06-01T12:00:00+00:00,1.25,1.26,1.24,1.255\n")
        report = self.run_gate()
        self.assertEqual(report["status"], "PASS_INPUT_PREFLIGHT_ONLY")
        self.assertEqual(report["sources"]["h1"]["rows_excluded_oos_2025"], 1)
        self.assertEqual(report["oos_2025"]["used_for_development"], False)

    def test_2025_in_non_h1_source_blocks(self):
        path = self.inputs["mtf"]
        with path.open("a", encoding="utf-8") as handle:
            row = {"timestamp": "2025-01-02T12:00:00+00:00"}
            row.update({field: "0.5" for field in MTF_NUMERIC_FIELDS})
            handle.write(",".join(row[k] for k in ["timestamp", *MTF_NUMERIC_FIELDS]) + "\n")
        report = self.run_gate()
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("ROWS_OUTSIDE_ALLOWED_DEVELOPMENT_WINDOW", report["sources"]["mtf"]["errors"])

    def test_missing_mtf_numeric_field_blocks(self):
        path = self.inputs["mtf"]
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        columns = ["timestamp", *[x for x in MTF_NUMERIC_FIELDS if x != "D1_trend_regime"]]
        write_csv(path, columns, [{k: row[k] for k in columns} for row in rows])
        report = self.run_gate()
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(any("MISSING_REQUIRED_COLUMNS" in x for x in report["sources"]["mtf"]["errors"]))

    def test_duplicate_h1_timestamp_blocks(self):
        path = self.inputs["h1"]
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        rows.append(dict(rows[0]))
        write_csv(path, ["timestamp", "open", "high", "low", "close"], rows)
        report = self.run_gate()
        self.assertEqual(report["status"], "BLOCKED")
        self.assertGreater(report["sources"]["h1"]["duplicate_timestamps"], 0)

    def test_naive_timestamp_blocks(self):
        path = self.inputs["h1"]
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        rows[0]["timestamp"] = "2016-06-01T12:00:00"
        write_csv(path, ["timestamp", "open", "high", "low", "close"], rows)
        report = self.run_gate()
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMPS", report["sources"]["h1"]["errors"])

    def test_invalid_ohlc_blocks(self):
        path = self.inputs["h1"]
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        rows[0]["high"] = "1.20"
        write_csv(path, ["timestamp", "open", "high", "low", "close"], rows)
        report = self.run_gate()
        self.assertEqual(report["status"], "BLOCKED")
        self.assertGreater(report["sources"]["h1"]["ohlc_violations"], 0)


if __name__ == "__main__":
    unittest.main()
