from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).with_name("mtf_brain_input_join_v1.py")
SPEC = importlib.util.spec_from_file_location("mtf_brain_input_join_v1", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_explicit_offsets_are_normalized_to_utc() -> None:
    values = pd.Series(["2024-01-02T10:00:00+02:00", "2024-01-02T09:00:00Z"])
    parsed = MODULE._parse_aware_timestamps(values, label="test")
    assert str(parsed.dtype) == "datetime64[ns, UTC]"
    assert parsed.iloc[0] == pd.Timestamp("2024-01-02T08:00:00Z")
    assert parsed.iloc[1] == pd.Timestamp("2024-01-02T09:00:00Z")


def test_naive_timestamp_is_rejected() -> None:
    values = pd.Series(["2024-01-02 10:00:00"])
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED"):
        MODULE._parse_aware_timestamps(values, label="test")


def test_mixed_aware_and_naive_timestamps_are_rejected() -> None:
    values = pd.Series(["2024-01-02T10:00:00+02:00", "2024-01-02 09:00:00"])
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED"):
        MODULE._parse_aware_timestamps(values, label="test")


def test_invalid_timestamp_is_rejected() -> None:
    values = pd.Series(["not-a-timestamp"])
    with pytest.raises(ValueError, match="invalid timestamp"):
        MODULE._parse_aware_timestamps(values, label="test")


def test_different_offsets_that_resolve_to_same_instant_are_detected_as_duplicate() -> None:
    events = pd.DataFrame({"timestamp": ["2024-01-02T10:00:00+02:00"]})
    mtf = pd.DataFrame(
        {
            "timestamp": ["2024-01-02T08:00:00Z", "2024-01-02T10:00:00+02:00"],
            **{field: [1, 1] for field in MODULE.REQUIRED_MTF_FIELDS},
        }
    )
    with pytest.raises(ValueError, match="mtf: duplicate timestamps"):
        MODULE.join_mtf_to_events(events, mtf)


def test_asof_join_uses_latest_non_future_mtf_row() -> None:
    events = pd.DataFrame(
        {"timestamp": ["2024-01-02T08:30:00Z", "2024-01-02T09:30:00Z"]}
    )
    mtf = pd.DataFrame(
        {
            "timestamp": ["2024-01-02T08:00:00Z", "2024-01-02T09:00:00Z"],
            **{field: [1, 2] for field in MODULE.REQUIRED_MTF_FIELDS},
        }
    )
    joined = MODULE.join_mtf_to_events(events, mtf)
    assert joined["mtf_trend_score"].tolist() == [1, 2]
    assert joined["M5_trend_regime"].tolist() == [1, 2]


BUILDER_PATH = MODULE_PATH.parents[2] / "tools" / "gate3c_build_single_event_bundle_v1.py"
BUILDER_SPEC = importlib.util.spec_from_file_location("gate3c_build_single_event_bundle_v1", BUILDER_PATH)
assert BUILDER_SPEC is not None and BUILDER_SPEC.loader is not None
BUILDER = importlib.util.module_from_spec(BUILDER_SPEC)
BUILDER_SPEC.loader.exec_module(BUILDER)


def test_gate3c_builder_rejects_naive_source_timestamp() -> None:
    with pytest.raises(ValueError, match="BLOCKED_TIMEZONE_PROVENANCE_UNRESOLVED"):
        BUILDER.parse_aware_timestamp("2024-01-02 10:00:00", source="fixture")


def test_gate3c_builder_normalizes_explicit_offset_to_utc() -> None:
    parsed = BUILDER.parse_aware_timestamp("2024-01-02T10:00:00+02:00", source="fixture")
    assert parsed == pd.Timestamp("2024-01-02T08:00:00Z")


def test_gate3c_builder_rejects_mixed_naive_and_aware_source_rows(tmp_path: Path) -> None:
    source = tmp_path / "mixed.csv"
    source.write_text(
        "timestamp,value\n2024-01-02T10:00:00+02:00,1\n2024-01-02 09:00:00,2\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="BLOCKED_TIMEZONE_PROVENANCE_UNRESOLVED"):
        BUILDER.read_rows_at(source, pd.Timestamp("2024-01-02T08:00:00Z"), exact=False)
