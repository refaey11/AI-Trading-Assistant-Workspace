from typing import Dict, Any


def evaluate_0028(row: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0028 exact evaluator recovered from the preserved Workspace artifact."""
    div = row.get("divergence_type")
    pivot = row.get("pivot_type")
    if div is None or pivot is None:
        return {"rule_id":"MURPHY_0028","status":"NOT_EVALUABLE","reason":"Missing divergence evidence."}
    ok = str(div).upper() == "BEARISH" and str(pivot).upper() == "HIGH"
    return {
        "rule_id":"MURPHY_0028",
        "status":"PASS" if ok else "FAIL",
        "directional_confirmation":"BEARISH_WARNING" if ok else "NONE",
        "reason":"Confirmed bearish price/RSI divergence on a high-pivot sequence."
    }


def evaluate_0029(row: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0029 exact evaluator recovered from the preserved Workspace artifact."""
    div = row.get("divergence_type")
    pivot = row.get("pivot_type")
    if div is None or pivot is None:
        return {"rule_id":"MURPHY_0029","status":"NOT_EVALUABLE","reason":"Missing divergence evidence."}
    ok = str(div).upper() == "BULLISH" and str(pivot).upper() == "LOW"
    return {
        "rule_id":"MURPHY_0029",
        "status":"PASS" if ok else "FAIL",
        "directional_confirmation":"BULLISH_WARNING" if ok else "NONE",
        "reason":"Confirmed bullish price/RSI divergence on a low-pivot sequence."
    }
