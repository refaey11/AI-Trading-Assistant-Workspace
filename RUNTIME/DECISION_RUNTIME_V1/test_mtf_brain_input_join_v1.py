from __future__ import annotations

import pandas as pd  # pandas is installed by the GitHub Actions workflow
import pytest

from RUNTIME.DECISION_RUNTIME_V1.mtf_brain_input_join_v1 import (
    REQUIRED_MTF_FIELDS,
    join_mtf_to_events,
)


def _frames():
    events = pd.DataFrame({"timestamp": ["2026-11-16T02:00:00Z"]})
    mtf = pd.DataFrame(
        {
            "timestamp": ["2026-11-16T01:59:00Z"],
            **{field: [1.0] for field in REQUIRED_MTF_FIELDS},
        }
    )
    return events, mtf


def test_join_accepts_finite_source_backed_mtf_values():
    events, mtf = _frames()
    result = join_mtf_to_events(events, mtf)
    assert len(result) == 1
    assert all(pd.notna(result[field].iloc[0]) for field in REQUIRED_MTF_FIELDS)


@pytest.mark.parametrize("field", REQUIRED_MTF_FIELDS)
@pytest.mark.parametrize("bad_value", [float("inf"), float("-inf")])
def test_join_rejects_positive_and_negative_infinity_for_every_mtf_field(field, bad_value):
    events, mtf = _frames()
    mtf.loc[0, field] = bad_value

    with pytest.raises(ValueError, match="non-finite"):
        join_mtf_to_events(events, mtf)


@pytest.mark.parametrize("field", REQUIRED_MTF_FIELDS)
def test_join_rejects_nan_for_every_mtf_field(field):
    events, mtf = _frames()
    mtf.loc[0, field] = float("nan")

    with pytest.raises(ValueError, match="non-numeric/NaN"):
        join_mtf_to_events(events, mtf)
