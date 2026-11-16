from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from BACKTEST.MTF_PRODUCER_SOURCE_ARCHIVE_SEARCH_V1 import search_archive


class MTFProducerSourceArchiveSearchTests(unittest.TestCase):
    def test_finds_producer_like_code_but_does_not_read_csv_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive_path = root / "project.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr(
                    "src/mtf_builder.py",
                    "def build():\n    mtf_trend_score = 0\n    df = pd.merge_asof(a, b)\n    return mtf_trend_score\n",
                )
                archive.writestr("data/GBPUSD_2025.csv", "mtf_trend_score\nSECRET_DATA\n")
                archive.writestr("docs/mtf_contract.md", "Higher timeframe candle_close alignment is required.")
            report = search_archive(archive_path, root / "report.json")
            self.assertEqual(report["status"], "PASS_ARCHIVE_SEARCH_ONLY")
            self.assertEqual(len(report["producer_candidates"]), 1)
            self.assertEqual(report["producer_candidates"][0]["path"], "src/mtf_builder.py")
            self.assertFalse(report["data_policy"]["csv_parquet_hdf5_feather_xlsx_data_files_read"])
            self.assertFalse(any("2025" in item["path"] for item in report["producer_candidates"]))

    def test_no_producer_code_is_reported_when_only_docs_and_data_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive_path = root / "project.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("docs/mtf_notes.md", "MTF alignment and timeframe context.")
                archive.writestr("data/market.csv", "timestamp,close\n")
            report = search_archive(archive_path, root / "report.json")
            self.assertEqual(report["producer_candidates"], [])
            self.assertEqual(len(report["other_relevant_text_files"]), 1)


if __name__ == "__main__":
    unittest.main()
