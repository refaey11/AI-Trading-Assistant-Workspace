from __future__ import annotations

import pandas as pd

from OOS_2025.nison_2025_source_adapter_v1 import build_payload_rows


def _bars() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"timestamp": "2024-12-31T23:58:00Z", "open": 1.0, "high": 1.1, "low": 0.9, "close": 1.05},
            {"timestamp": "2024-12-31T23:59:00Z", "open": 1.05, "high": 1.2, "low": 1.0, "close": 1.1},
            {"timestamp": "2025-01-02T00:00:00Z", "open": 1.1, "high": 1.2, "low": 1.0, "close": 1.15},
        ]
    )


def test_year_parameter_filters_only_requested_fold():
    rows_2024 = build_payload_rows(_bars(), evaluation_year=2024)
    rows_2025 = build_payload_rows(_bars(), evaluation_year=2025)
    assert len(rows_2024) == 2 * 44
    assert len(rows_2025) == 1 * 44
    assert {r["rule_id"] for r in rows_2024} == {f"NISON_{i:04d}" for i in range(1, 45)}
    assert {r["rule_id"] for r in rows_2025} == {f"NISON_{i:04d}" for i in range(1, 45)}
    assert {pd.Timestamp(r["timestamp"]).year for r in rows_2024} == {2024}
    assert {pd.Timestamp(r["timestamp"]).year for r in rows_2025} == {2025}


def test_default_behavior_remains_2025_compatible():
    explicit = build_payload_rows(_bars(), evaluation_year=2025)
    default = build_payload_rows(_bars())
    assert default == explicit
