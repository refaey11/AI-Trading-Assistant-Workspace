"""Contract-only evaluator boundary for the frozen Decision Brain 2025 OOS run.

This module does not generate signals, tune rules, select thresholds, or modify
Decision Brain V1. It validates that an already-produced frozen decision stream
is eligible to be evaluated against 2025 market data.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable

REQUIRED_DECISION_FIELDS = {
    "timestamp",
    "direction",
    "source_rule_ids",
    "trading_zone",
    "risk_engine",
}


def validate_oos_record(record: Dict[str, Any]) -> Dict[str, Any]:
    missing = sorted(REQUIRED_DECISION_FIELDS - set(record))
    if missing:
        return {
            "status": "REJECTED",
            "execution_allowed": False,
            "reason": "MISSING_FROZEN_DECISION_FIELDS",
            "missing": missing,
        }
    return {"status": "ACCEPTED", "execution_allowed": True}


def validate_oos_batch(*, year: int, mode: str, records: Iterable[Dict[str, Any]],
                       tuning: bool = False, calibration: bool = False,
                       threshold_selection: bool = False, future_data: bool = False) -> Dict[str, Any]:
    if year != 2025 or mode != "oos_evaluation":
        return {"status": "REJECTED", "reason": "2025_OOS_ONLY"}
    if any((tuning, calibration, threshold_selection, future_data)):
        return {"status": "REJECTED", "reason": "OOS_INTEGRITY_VIOLATION"}

    checked = 0
    for record in records:
        checked += 1
        result = validate_oos_record(record)
        if result["status"] != "ACCEPTED":
            return {"status": "REJECTED", "reason": result["reason"], "checked": checked, **result}

    return {"status": "ACCEPTED", "year": 2025, "mode": mode, "records_checked": checked}
