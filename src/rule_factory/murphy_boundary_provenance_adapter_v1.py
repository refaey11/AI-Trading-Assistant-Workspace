"""Boundary provenance gate for Murphy 0013/0014/0018/0019/0020.

The adapter does not construct pivots or boundaries. It only verifies that
all upstream artifacts were available by the decision timestamp. Missing
provenance is fail-closed as NOT_EVALUABLE.
"""
from typing import Any, Dict, Iterable
from datetime import datetime


def _parse_time(value: Any):
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate_boundary_provenance(boundary: Dict[str, Any], decision_time: Any) -> Dict[str, Any]:
    """Return PASS/NOT_EVALUABLE without inferring missing timestamps."""
    decision = _parse_time(decision_time)
    if decision is None or not isinstance(boundary, dict):
        return {"status": "NOT_EVALUABLE", "reason": "missing_or_invalid_decision_time"}

    pivots = boundary.get("pivots")
    if not isinstance(pivots, Iterable) or isinstance(pivots, (str, bytes)):
        return {"status": "NOT_EVALUABLE", "reason": "missing_pivot_provenance"}

    pivots = list(pivots)
    if not pivots:
        return {"status": "NOT_EVALUABLE", "reason": "empty_pivot_provenance"}

    for pivot in pivots:
        if not isinstance(pivot, dict):
            return {"status": "NOT_EVALUABLE", "reason": "invalid_pivot_record"}
        available = _parse_time(pivot.get("availability_timestamp"))
        if available is None:
            return {"status": "NOT_EVALUABLE", "reason": "missing_pivot_availability_timestamp"}
        if available > decision:
            return {"status": "NOT_EVALUABLE", "reason": "pivot_not_available_at_decision_time"}

    return {"status": "PASS"}
