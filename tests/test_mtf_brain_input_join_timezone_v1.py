from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from RUNTIME.DECISION_RUNTIME_V1.mtf_brain_input_join_v1 import _load_timestamped


class MtfBrainInputJoinTimezoneTests(unittest.TestCase):
    def _write_csv(self, root: Path, timestamp: str) -> Path:
        path = root / "source.csv"
        pd.DataFrame({"timestamp": [timestamp]}).to_csv(path, index=False)
        return path

    def test_naive_source_timestamp_is_rejected_without_utc_assumption(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_csv(Path(tmp), "2024-01-02T00:00:00")
            with self.assertRaisesRegex(ValueError, "TIMEZONE_PROVENANCE_UNRESOLVED"):
                _load_timestamped(path, {"timestamp"})

    def test_explicitly_aware_source_timestamp_is_normalized_to_utc(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_csv(Path(tmp), "2024-01-02T03:00:00+03:00")
            frame = _load_timestamped(path, {"timestamp"})
            self.assertEqual(str(frame.loc[0, "timestamp"]), "2024-01-02 00:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
