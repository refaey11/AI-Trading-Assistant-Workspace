from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "gate3c_mtf_bundle_under_test",
    ROOT / "tools" / "gate3c_build_single_event_bundle_v1.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

FIELDS = MODULE.MTF_FIELDS
EVENT = pd.Timestamp("2020-01-02T01:00:00Z")


def write_mtf(path: Path, timestamps: list[str], *, missing: set[str] | None = None):
    missing = missing or set()
    rows = []
    for timestamp in timestamps:
        row = {"timestamp": timestamp}
        for index, field in enumerate(FIELDS):
            row[field] = None if field in missing else index
        rows.append(row)
    pd.DataFrame(rows).to_csv(path, index=False)


def test_event_year_selects_2020_file_not_lexicographically_first_2016(tmp_path):
    write_mtf(
        tmp_path / "GBPUSD_M5_MTF_ALIGNMENT_2016.csv",
        ["2016-12-30T16:55:00Z"],
    )
    write_mtf(
        tmp_path / "GBPUSD_M5_MTF_ALIGNMENT_2020.csv",
        ["2020-01-02T00:55:00Z", "2020-01-02T01:00:00Z"],
    )

    path, row, row_ts = MODULE.read_mtf_row_asof(tmp_path, EVENT)

    assert path.name == "GBPUSD_M5_MTF_ALIGNMENT_2020.csv"
    assert row_ts == EVENT
    assert row["M5_trend_regime"] == 1


def test_missing_event_year_file_fails_closed_without_other_year_fallback(tmp_path):
    write_mtf(
        tmp_path / "GBPUSD_M5_MTF_ALIGNMENT_2016.csv",
        ["2016-12-30T16:55:00Z"],
    )

    with pytest.raises(ValueError, match="BLOCKED_MTF_ANNUAL_SOURCE_CARDINALITY"):
        MODULE.read_mtf_row_asof(tmp_path, EVENT)


def test_mtf_asof_row_older_than_one_m5_interval_is_rejected(tmp_path):
    write_mtf(
        tmp_path / "GBPUSD_M5_MTF_ALIGNMENT_2020.csv",
        ["2020-01-02T00:54:00Z"],
    )

    with pytest.raises(ValueError, match="BLOCKED_MTF_STALE_AS_OF_EVENT"):
        MODULE.read_mtf_row_asof(tmp_path, EVENT)


def test_exactly_one_m5_interval_old_is_accepted(tmp_path):
    write_mtf(
        tmp_path / "GBPUSD_M5_MTF_ALIGNMENT_2020.csv",
        ["2020-01-02T00:55:00Z"],
    )

    path, row, row_ts = MODULE.read_mtf_row_asof(tmp_path, EVENT)

    assert path.name.endswith("_2020.csv")
    assert row_ts == pd.Timestamp("2020-01-02T00:55:00Z")
    assert len(row) == len(FIELDS)


def test_required_mtf_missing_field_remains_blocked(tmp_path):
    write_mtf(
        tmp_path / "GBPUSD_M5_MTF_ALIGNMENT_2020.csv",
        ["2020-01-02T01:00:00Z"],
        missing={"H4_trend_regime", "D1_trend_regime"},
    )

    with pytest.raises(ValueError, match="BLOCKED_MTF_FIELDS"):
        MODULE.read_mtf_row_asof(tmp_path, EVENT)


def test_duplicate_latest_mtf_timestamp_is_rejected_as_ambiguous(tmp_path):
    write_mtf(
        tmp_path / "GBPUSD_M5_MTF_ALIGNMENT_2020.csv",
        ["2020-01-02T01:00:00Z", "2020-01-02T01:00:00Z"],
    )

    with pytest.raises(ValueError, match="BLOCKED_MTF_AMBIGUOUS_AS_OF_ROW"):
        MODULE.read_mtf_row_asof(tmp_path, EVENT)
