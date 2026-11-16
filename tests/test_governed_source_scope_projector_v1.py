from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "BACKTEST"))

from GOVERNED_SOURCE_SCOPE_PROJECTOR_V1 import project_all, project_source


class GovernedSourceScopeProjectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, columns, rows):
        path = self.root / name
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_market_state_and_context_exclude_2025_without_mutating_source(self):
        rows = [
            {"timestamp": "2024-12-31T12:00:00+00:00", "context_signature": "a"},
            {"timestamp": "2025-01-01T12:00:00+00:00", "context_signature": "b"},
        ]
        src = self.write("context.csv", ["timestamp", "context_signature"], rows)
        original = src.read_bytes()
        report = project_source("historical_context", src, self.root / "context_projected.csv")
        with (self.root / "context_projected.csv").open(encoding="utf-8", newline="") as handle:
            projected = list(csv.DictReader(handle))
        self.assertEqual(len(projected), 1)
        self.assertEqual(projected[0]["context_signature"], "a")
        self.assertEqual(src.read_bytes(), original)
        self.assertEqual(report["excluded_outside_development_year_counts"], {"2025": 1})
        self.assertFalse(report["source_rows_modified"])

    def test_outcome_rows_whose_48h_horizon_crosses_2025_are_excluded(self):
        columns = ["timestamp", "context_signature", "return_6h", "return_12h", "return_24h", "return_48h"]
        rows = [
            {"timestamp": "2024-12-29T23:00:00+00:00", "context_signature": "mature", "return_6h": "1", "return_12h": "1", "return_24h": "1", "return_48h": "1"},
            {"timestamp": "2024-12-30T00:00:00+00:00", "context_signature": "crosses", "return_6h": "1", "return_12h": "1", "return_24h": "1", "return_48h": "1"},
            {"timestamp": "2025-01-01T00:00:00+00:00", "context_signature": "oos", "return_6h": "1", "return_12h": "1", "return_24h": "1", "return_48h": "1"},
        ]
        src = self.write("outcome.csv", columns, rows)
        report = project_source("historical_outcome", src, self.root / "outcome_projected.csv")
        with (self.root / "outcome_projected.csv").open(encoding="utf-8", newline="") as handle:
            projected = list(csv.DictReader(handle))
        self.assertEqual([r["context_signature"] for r in projected], ["mature"])
        self.assertEqual(report["excluded_outcome_rows_not_mature_before_2025"], 1)
        self.assertEqual(report["excluded_outside_development_year_counts"], {"2025": 1})

    def test_naive_timestamp_fails_closed(self):
        src = self.write("context_naive.csv", ["timestamp", "context_signature"], [
            {"timestamp": "2024-12-31T12:00:00", "context_signature": "x"},
        ])
        with self.assertRaisesRegex(ValueError, "TIMEZONE_PROVENANCE_UNRESOLVED"):
            project_source("historical_context", src, self.root / "naive_out.csv")

    def test_project_all_writes_audit_manifest(self):
        market = self.write("market.csv", ["timestamp"], [{"timestamp": "2024-01-01T00:00:00+00:00"}])
        context = self.write("context.csv", ["timestamp", "context_signature"], [{"timestamp": "2024-01-01T00:00:00+00:00", "context_signature": "x"}])
        outcome = self.write("outcome.csv", ["timestamp", "context_signature", "return_6h", "return_12h", "return_24h", "return_48h"], [
            {"timestamp": "2024-01-01T00:00:00+00:00", "context_signature": "x", "return_6h": "1", "return_12h": "1", "return_24h": "1", "return_48h": "1"}
        ])
        report = project_all({"market_state": market, "historical_context": context, "historical_outcome": outcome}, self.root / "out", self.root / "report.json")
        self.assertEqual(report["status"], "PASS_GOVERNED_SCOPE_PROJECTION_ONLY")
        self.assertFalse(report["full_backtest_authorized"])
        self.assertTrue((self.root / "report.json").is_file())


if __name__ == "__main__":
    unittest.main()
