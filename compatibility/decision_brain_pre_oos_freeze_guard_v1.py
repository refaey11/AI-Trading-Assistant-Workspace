"""Pre-OOS freeze guard for the Decision Brain.

The guard does not modify source logic. It enforces the project boundary that
2025 may be evaluated only as locked OOS and never used for development,
calibration, threshold selection, or implementation selection.
"""
from __future__ import annotations

LOCKED_OOS_YEAR = 2025


def validate_freeze_manifest(manifest: dict) -> None:
    assert manifest["oos_year"] == LOCKED_OOS_YEAR
    rules = manifest["rules"]
    assert rules["no_2025_tuning"] is True
    assert rules["no_2025_calibration"] is True
    assert rules["no_2025_threshold_selection"] is True
    assert rules["no_future_data"] is True
    assert rules["similarity_is_evidence_only"] is True
    assert rules["historical_memory_is_evidence_only"] is True
    assert rules["tiz_generates_direction"] is False
    assert rules["risk_overridable"] is False


def development_timestamp_allowed(year: int) -> bool:
    return int(year) < LOCKED_OOS_YEAR


def oos_timestamp_allowed(year: int) -> bool:
    return int(year) == LOCKED_OOS_YEAR


def future_timestamp_allowed(year: int) -> bool:
    return int(year) > LOCKED_OOS_YEAR
