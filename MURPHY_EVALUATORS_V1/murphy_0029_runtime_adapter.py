from __future__ import annotations
from typing import Any, Dict


def _missing(*values: Any) -> bool:
    return any(v is None for v in values)


def evaluate_0029(row: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0029 exact semantics via existing divergence evidence.

    PASS only for BULLISH divergence at LOW pivot. Missing required
    divergence evidence is NOT_EVALUABLE. No thresholds or new semantics.
    """
    divergence_type = row.get("divergence_type")
    pivot_type = row.get("pivot_type")
    if _missing(divergence_type, pivot_type):
        return {
            "rule_id": "MURPHY_0029",
            "status": "NOT_EVALUABLE",
            "directional_confirmation": "UNKNOWN",
        }
    ok = divergence_type == "BULLISH" and pivot_type == "LOW"
    return {
        "rule_id": "MURPHY_0029",
        "status": "PASS" if ok else "FAIL",
        "directional_confirmation": "BULLISH" if ok else "NONE",
    }
