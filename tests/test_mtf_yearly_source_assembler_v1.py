from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "BACKTEST"))

from MTF_YEARLY_SOURCE_ASSEMBLER_V1 import REQUIRED_FIELDS, assemble_yearly_mtf


def write_year(root: Path, year: int, timestamps: list[str] | None = None, header: list[str] | None = None) -> Path:
    path = root / f"GBPUSD_M5_MTF_ALIGNMENT_{year}.csv"
    columns = header or list(REQUIRED_FIELDS)
    values = timestamps or [f"{year}-01-01T00:00:00+00:00"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        for ts in values:
            row = {name: "0.25" for name in columns}
            row["timestamp"] = ts
            writer.writerow([row[name] for name in columns])
    return path


class MTFYearlyAssemblerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.output = self.root / "out" / "mtf.csv"

    def tearDown(self):
        self.tmp.cleanup()

    def seed_all_dev_years(self):
        for year in range(2016, 2025):
            write_year(self.source, year)

    def test_assembles_exactly_2016_to_2024_and_excludes_oos_files(self):
        self.seed_all_dev_years()
        write_year(self.source, 2025)
        write_year(self.source, 2026)
        report = assemble_yearly_mtf(self.source, self.output)
        self.assertEqual(report["status"], "PASS_MTF_YEARLY_ASSEMBLY_ONLY")
        self.assertEqual(report["rows"], 9)
        self.assertEqual([x["year"] for x in report["source_years"]], list(range(2016, 2025)))
        self.assertEqual({x["year"] for x in report["excluded_oos_files"]}, {2025, 2026})
        with self.output.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 9)
        self.assertTrue(all(row["timestamp"].startswith(tuple(f"{y}-" for y in range(2016, 2025))) for row in rows))
        self.assertFalse(report["2025_oos_used"])
        self.assertFalse(report["source_rows_rewritten_or_transformed"])

    def test_missing_development_year_blocks(self):
        for year in range(2016, 2024):
            write_year(self.source, year)
        with self.assertRaisesRegex(ValueError, "MTF_YEAR_FILE_SET_INVALID"):
            assemble_yearly_mtf(self.source, self.output)

    def test_mismatched_header_blocks(self):
        self.seed_all_dev_years()
        columns = list(REQUIRED_FIELDS[:-1])
        write_year(self.source, 2020, header=columns)
        with self.assertRaisesRegex(ValueError, "MTF_REQUIRED_FIELDS_MISSING"):
            assemble_yearly_mtf(self.source, self.output)

    def test_file_with_wrong_year_content_blocks(self):
        self.seed_all_dev_years()
        write_year(self.source, 2019, timestamps=["2020-01-01T00:00:00+00:00"])
        with self.assertRaisesRegex(ValueError, "MTF_YEAR_CONTENT_MISMATCH"):
            assemble_yearly_mtf(self.source, self.output)

    def test_naive_timestamp_is_preserved_and_marked_unresolved(self):
        for year in range(2016, 2025):
            write_year(self.source, year, timestamps=[f"{year}-01-01T00:00:00"])
        report = assemble_yearly_mtf(self.source, self.output)
        self.assertEqual(report["status"], "PASS_MTF_YEARLY_ASSEMBLY_ONLY")
        self.assertFalse(report["timezone_provenance_resolved"])
        self.assertEqual(report["timestamp_mode"], "NAIVE_UNRESOLVED")
        self.assertEqual(report["naive_timestamp_rows"], 9)

    def test_duplicate_timestamp_across_year_files_blocks(self):
        self.seed_all_dev_years()
        # A 2017 row cannot validly duplicate a 2016 timestamp, so the year mismatch
        # guard rejects this before it can be admitted into the development output.
        write_year(self.source, 2017, timestamps=["2016-01-01T00:00:00+00:00"])
        with self.assertRaisesRegex(ValueError, "MTF_YEAR_CONTENT_MISMATCH"):
            assemble_yearly_mtf(self.source, self.output)


if __name__ == "__main__":
    unittest.main()
