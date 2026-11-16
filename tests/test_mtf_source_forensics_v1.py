from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from BACKTEST.MTF_SOURCE_FORENSICS_V1 import BRAIN_FIELDS, run_forensics


class MTFSourceForensicsTests(unittest.TestCase):
    def _write_year(self, root: Path, year: int, rows: list[dict[str, str]]) -> None:
        path = root / f"GBPUSD_M5_MTF_ALIGNMENT_{year}.csv"
        fields = ["timestamp", *BRAIN_FIELDS, "mtf_context"]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_profiles_only_2016_to_2024_and_ignores_oos_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for year in range(2016, 2025):
                self._write_year(root, year, [{
                    "timestamp": f"{year}-01-01T00:00:00",
                    "mtf_trend_score": "0.5",
                    "M5_trend_regime": "1",
                    "M15_trend_regime": "",
                    "M30_trend_regime": "0",
                    "H1_trend_regime": "-1",
                    "H4_trend_regime": "1",
                    "D1_trend_regime": "0",
                    "mtf_context": "MIXED",
                }])
            (root / "GBPUSD_M5_MTF_ALIGNMENT_2025.csv").write_text("must not be read", encoding="utf-8")
            report = run_forensics(root, root / "report.json")
            self.assertEqual(report["status"], "PASS_FORENSICS_ONLY")
            self.assertEqual(report["annual_file_count"], 9)
            self.assertEqual(report["oos_policy"]["2025"], "LOCKED_NOT_READ")
            self.assertEqual(report["annual_files"][0]["brain_and_aggregate_field_profile"]["M15_trend_regime"]["blank"], 1)
            self.assertEqual(report["annual_files"][0]["timestamp_modes"], {"naive": 1})
            self.assertFalse(report["transformations_applied"]["source_mutation"])

    def test_reports_aware_timestamps_and_nonblank_value_distributions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for year in range(2016, 2025):
                self._write_year(root, year, [{
                    "timestamp": f"{year}-01-01T00:00:00+03:00",
                    "mtf_trend_score": "2",
                    "M5_trend_regime": "1",
                    "M15_trend_regime": "1",
                    "M30_trend_regime": "0",
                    "H1_trend_regime": "-1",
                    "H4_trend_regime": "1",
                    "D1_trend_regime": "0",
                    "mtf_context": "BULLISH",
                }])
            report = run_forensics(root, root / "report.json")
            profile = report["annual_files"][0]
            self.assertEqual(profile["timestamp_modes"], {"aware": 1})
            values = profile["brain_and_aggregate_field_profile"]["mtf_trend_score"]["top_values"]
            self.assertEqual(values[0], {"value": "2", "count": 1})

    def test_missing_development_year_blocks_forensics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_year(root, 2016, [{
                "timestamp": "2016-01-01T00:00:00",
                **{field: "1" for field in BRAIN_FIELDS},
                "mtf_context": "BULLISH",
            }])
            report = run_forensics(root, root / "report.json")
            self.assertEqual(report["status"], "BLOCKED_FORENSICS")
            self.assertEqual(len(report["missing_development_years"]), 8)


if __name__ == "__main__":
    unittest.main()
