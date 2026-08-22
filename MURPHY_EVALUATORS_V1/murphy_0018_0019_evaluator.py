from __future__ import annotations
from typing import Any, Dict

VALID = {"PASS", "FAIL", "NOT_EVALUABLE", "CONFLICT"}


def _missing(*values: Any) -> bool:
    return any(v is None for v in values)


def evaluate_0018(row: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0018 exact condition: two converging trendlines, both slope downward."""
    converging = row.get("trendlines_converging")
    upper_slope = row.get("upper_slope")
    lower_slope = row.get("lower_slope")
    if _missing(converging, upper_slope, lower_slope):
        return {"rule_id":"MURPHY_0018","status":"NOT_EVALUABLE","directional_confirmation":"UNKNOWN","reason":"Missing convergence or completed trendline slope evidence."}
    ok = bool(converging) and upper_slope < 0 and lower_slope < 0
    return {"rule_id":"MURPHY_0018","status":"PASS" if ok else "FAIL","directional_confirmation":"BULLISH" if ok else "NONE","reason":"Evaluated exact falling-wedge geometry: converging boundaries and both slopes negative; no threshold added."}


def evaluate_0019(row: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0019 exact condition: two converging trendlines, both slope upward."""
    converging = row.get("trendlines_converging")
    upper_slope = row.get("upper_slope")
    lower_slope = row.get("lower_slope")
    if _missing(converging, upper_slope, lower_slope):
        return {"rule_id":"MURPHY_0019","status":"NOT_EVALUABLE","directional_confirmation":"UNKNOWN","reason":"Missing convergence or completed trendline slope evidence."}
    ok = bool(converging) and upper_slope > 0 and lower_slope > 0
    return {"rule_id":"MURPHY_0019","status":"PASS" if ok else "FAIL","directional_confirmation":"BEARISH" if ok else "NONE","reason":"Evaluated exact rising-wedge geometry: converging boundaries and both slopes positive; no threshold added."}


EVALUATORS = {"MURPHY_0018": evaluate_0018, "MURPHY_0019": evaluate_0019}


def dispatch(rule_id: str, row: Dict[str, Any]) -> Dict[str, Any]:
    try:
        return EVALUATORS[rule_id](row)
    except KeyError:
        raise KeyError(f"Unsupported rule_id: {rule_id}")
