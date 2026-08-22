from __future__ import annotations
from typing import Any, Dict


def _missing(*values: Any) -> bool:
    return any(v is None for v in values)


def evaluate_0008(row: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0008 minimal source-faithful support->resistance role reversal.

    Requires completed-bar event evidence produced by PF-H1/PF-B1 lineage.
    No numeric tolerance, ATR, percentage, pip, or volume threshold is used.
    """
    direction = row.get("direction")
    level = row.get("level_price")
    breakout_ts = row.get("breakout_timestamp")
    retest_ts = row.get("retest_timestamp")
    reversal_ts = row.get("role_reversal_timestamp")
    if _missing(direction, level, breakout_ts, retest_ts, reversal_ts):
        return {"rule_id":"MURPHY_0008","status":"NOT_EVALUABLE","directional_confirmation":"UNKNOWN"}
    if not (breakout_ts < retest_ts < reversal_ts):
        return {"rule_id":"MURPHY_0008","status":"NOT_EVALUABLE","directional_confirmation":"UNKNOWN","reason":"Event timestamps are not strictly ordered."}
    if direction not in {"UPSIDE", "DOWNSIDE"}:
        return {"rule_id":"MURPHY_0008","status":"NOT_EVALUABLE","directional_confirmation":"UNKNOWN","reason":"Unknown breakout direction."}
    return {"rule_id":"MURPHY_0008","status":"PASS","directional_confirmation":"BEARISH"}
