from __future__ import annotations
from typing import Any, Dict

from src.murphy_0030_0032.pnf_3box_reference import bullish_support_reference, stop_reference


def evaluate_0030(payload: Dict[str, Any]) -> Dict[str, Any]:
    columns = payload.get("columns")
    if not isinstance(columns, list):
        return {"rule_id": "MURPHY_0030", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    ref = bullish_support_reference(columns)
    if ref is None:
        return {"rule_id": "MURPHY_0030", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    return {**ref, "rule_id": "MURPHY_0030", "status": "PASS", "directional_confirmation": "NEUTRAL"}


def evaluate_0031(payload: Dict[str, Any]) -> Dict[str, Any]:
    columns = payload.get("columns")
    if not isinstance(columns, list):
        return {"rule_id": "MURPHY_0031", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    ref = stop_reference(columns, "BULLISH")
    if ref is None:
        return {"rule_id": "MURPHY_0031", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    return {**ref, "rule_id": "MURPHY_0031", "status": "PASS", "directional_confirmation": "NEUTRAL"}


def evaluate_0032(payload: Dict[str, Any]) -> Dict[str, Any]:
    columns = payload.get("columns")
    if not isinstance(columns, list):
        return {"rule_id": "MURPHY_0032", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    ref = stop_reference(columns, "BEARISH")
    if ref is None:
        return {"rule_id": "MURPHY_0032", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    return {**ref, "rule_id": "MURPHY_0032", "status": "PASS", "directional_confirmation": "NEUTRAL"}
