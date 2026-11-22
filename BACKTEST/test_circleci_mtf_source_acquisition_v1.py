"""Synthetic schema-contract tests; fixtures are not market data or regime definitions."""
from pathlib import Path

import pandas as pd
import pytest

from BACKTEST.CIRCLECI_ACQUIRE_GOVERNED_SOURCES import FILES, build_canonical_mtf_source
from BACKTEST.mtf_source_contract_gate_v1 import REQUIRED

SENTINEL = 987654.321  # schema sentinel only; not a market value or regime encoding


def _write_year(
    root: Path,
    year: int,
    *,
    timestamp: str | None = None,
    missing_field: str | None = None,
    categorical_field: str | None = None,
    duplicate_timestamp: str | None = None,
) -> None:
    path = root / f"year_{year}" / f"GBPUSD_M5_MTF_ALIGNMENT_{year}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"timestamp": timestamp or f"{year}-01-02T00:00:00+00:00"}
    row.update({field: SENTINEL for field in REQUIRED})
    if missing_field:
        row[missing_field] = None
    if categorical_field:
        row[categorical_field] = "BULL_TREND"
    if duplicate_timestamp:
        row["timestamp"] = duplicate_timestamp
    pd.DataFrame([row]).to_csv(path, index=False)


def _write_all_years(
    root: Path,
    *,
    naive_year: int | None = None,
    missing_field: str | None = None,
    categorical_field: str | None = None,
    duplicate_2017_timestamp: str | None = None,
) -> None:
    for year in range(2016, 2025):
        timestamp = (
            f"{year}-01-02 00:00:00"
            if year == naive_year
            else f"{year}-01-02T00:00:00+00:00"
        )
        _write_year(
            root,
            year,
            timestamp=timestamp,
            missing_field=missing_field if year == 2024 else None,
            categorical_field=categorical_field if year == 2024 else None,
            duplicate_timestamp=duplicate_2017_timestamp if year == 2017 else None,
        )


def test_acquisition_uses_canonical_six_timeframe_archive_not_legacy_reader() -> None:
    assert FILES["mtf.zip"] == "/MTF_ALIGNMENT_GBPUSD_V1.zip"


def test_assembles_only_2016_to_2024_source_files_without_transforming_values(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_all_years(source)
    output = build_canonical_mtf_source(source, tmp_path / "artifacts" / "mtf_2016_2024.csv")

    result = pd.read_csv(output)
    assert len(result) == 9
    assert sorted(pd.to_datetime(result["timestamp"], utc=True).dt.year.unique().tolist()) == list(range(2016, 2025))
    assert result[list(REQUIRED)].eq(SENTINEL).all().all()


def test_missing_annual_source_fails_closed_without_output(tmp_path: Path) -> None:
    source = tmp_path / "source"
    for year in range(2016, 2024):
        _write_year(source, year)
    output = tmp_path / "artifacts" / "mtf.csv"

    with pytest.raises(SystemExit, match="MTF_FILE_COUNT_FAIL:2024"):
        build_canonical_mtf_source(source, output)
    assert not output.exists()


def test_naive_source_timestamp_fails_closed(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_all_years(source, naive_year=2024)

    with pytest.raises(SystemExit, match="BLOCKED_MTF_TIMEZONE_PROVENANCE_UNRESOLVED"):
        build_canonical_mtf_source(source, tmp_path / "artifacts" / "mtf.csv")


def test_missing_source_feature_fails_closed(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_all_years(source, missing_field="D1_trend_regime")

    with pytest.raises(SystemExit, match="BLOCKED_MTF_MISSING_SOURCE_VALUE:D1_trend_regime"):
        build_canonical_mtf_source(source, tmp_path / "artifacts" / "mtf.csv")


def test_categorical_regime_token_is_not_mapped_to_numeric(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_all_years(source, categorical_field="M15_trend_regime")

    with pytest.raises(SystemExit, match="BLOCKED_MTF_NON_NUMERIC_SOURCE_FIELD:M15_trend_regime"):
        build_canonical_mtf_source(source, tmp_path / "artifacts" / "mtf.csv")


def test_duplicate_timestamps_across_annual_files_fail_closed(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_all_years(source, duplicate_2017_timestamp="2016-01-02T00:00:00+00:00")

    with pytest.raises(SystemExit, match="MTF_GLOBAL_TIMESTAMP_DUPLICATE_FAIL"):
        build_canonical_mtf_source(source, tmp_path / "artifacts" / "mtf.csv")
