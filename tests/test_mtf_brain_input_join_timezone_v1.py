from __future__ import annotations

import pandas as pd
import pytest

from RUNTIME.DECISION_RUNTIME_V1.mtf_brain_input_join_v1 import _load_timestamped


def _write_csv(tmp_path, timestamp: str):
    path = tmp_path / "source.csv"
    pd.DataFrame({"timestamp": [timestamp]}).to_csv(path, index=False)
    return path


def test_naive_source_timestamp_is_rejected_without_utc_assumption(tmp_path):
    path = _write_csv(tmp_path, "2024-01-02T00:00:00")
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED"):
        _load_timestamped(path, {"timestamp"})


def test_explicitly_aware_source_timestamp_is_normalized_to_utc(tmp_path):
    path = _write_csv(tmp_path, "2024-01-02T03:00:00+03:00")
    frame = _load_timestamped(path, {"timestamp"})
    assert str(frame.loc[0, "timestamp"]) == "2024-01-02 00:00:00+00:00"
