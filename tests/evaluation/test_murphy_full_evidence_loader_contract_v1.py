from pathlib import Path

import pandas as pd
import pytest

from OOS_2025.build_murphy_2025_full_evidence_v1 import read_csv


def _write_csv(tmp_path: Path, rows: list[dict]) -> Path:
    path = tmp_path / "evidence.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_source_rule_output_allows_same_timestamp_for_distinct_rules(tmp_path: Path):
    path = _write_csv(
        tmp_path,
        [
            {"timestamp": "2025-01-02T00:00:00Z", "rule_id": "MURPHY_0022", "status": "PASS"},
            {"timestamp": "2025-01-02T00:00:00Z", "rule_id": "MURPHY_0023", "status": "FAIL"},
        ],
    )

    df = read_csv(path, {"timestamp", "rule_id", "status"}, unique_by=("timestamp", "rule_id"))

    assert len(df) == 2
    assert df["timestamp"].nunique() == 1
    assert set(df["rule_id"]) == {"MURPHY_0022", "MURPHY_0023"}


def test_source_rule_output_rejects_duplicate_timestamp_rule_pair(tmp_path: Path):
    path = _write_csv(
        tmp_path,
        [
            {"timestamp": "2025-01-02T00:00:00Z", "rule_id": "MURPHY_0022", "status": "PASS"},
            {"timestamp": "2025-01-02T00:00:00Z", "rule_id": "MURPHY_0022", "status": "FAIL"},
        ],
    )

    with pytest.raises(ValueError, match="duplicated timestamp, rule_id keys"):
        read_csv(path, {"timestamp", "rule_id", "status"}, unique_by=("timestamp", "rule_id"))
