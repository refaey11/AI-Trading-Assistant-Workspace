"""Source-locked evaluator for Murphy 0025/0026.

Uses the existing Four-Week Lookback reference values. It does not choose a
 time frame or substitute a fixed bar count.
"""

from typing import Any, Dict


def evaluate_0025(bar: Dict[str, Any]) -> Dict[str, Any]:
    """New four-week high: current high >= preceding four completed weeks high."""
    ref = bar.get("four_week_high")
    high = bar.get("high")
    if ref is None or high is None:
        return {"rule_id": "0025", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    passed = float(high) >= float(ref)
    return {
        "rule_id": "0025",
        "status": "PASS" if passed else "FAIL",
        "directional_confirmation": "BULLISH" if passed else "NONE",
        "reason": "current high >= preceding four completed calendar weeks high" if passed else "current high below preceding four completed calendar weeks high",
    }


def evaluate_0026(bar: Dict[str, Any]) -> Dict[str, Any]:
    """New four-week low: current low <= preceding four completed weeks low."""
    ref = bar.get("four_week_low")
    low = bar.get("low")
    if ref is None or low is None:
        return {"rule_id": "0026", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    passed = float(low) <= float(ref)
    return {
        "rule_id": "0026",
        "status": "PASS" if passed else "FAIL",
        "directional_confirmation": "BEARISH" if passed else "NONE",
        "reason": "current low <= preceding four completed calendar weeks low" if passed else "current low above preceding four completed calendar weeks low",
    }
