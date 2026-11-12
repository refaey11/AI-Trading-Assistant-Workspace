from __future__ import annotations

from math import isfinite
from typing import Any, Dict

from src.murphy_0030_0032.pnf_3box_reference import (
    PNFColumn,
    bullish_support_reference,
    stop_reference,
)


def _normalize_columns(payload: Dict[str, Any]) -> list[PNFColumn] | None:
    raw_columns = payload.get("columns")
    if not isinstance(raw_columns, list) or not raw_columns:
        return None

    columns: list[PNFColumn] = []
    for raw in raw_columns:
        if isinstance(raw, PNFColumn):
            columns.append(raw)
            continue
        if not isinstance(raw, dict):
            return None
        kind = raw.get("kind")
        boxes = raw.get("boxes")
        if kind not in {"X", "O"} or not isinstance(boxes, list) or not boxes:
            return None
        try:
            numeric_boxes = [float(value) for value in boxes]
        except (TypeError, ValueError):
            return None
        if not all(isfinite(value) for value in numeric_boxes):
            return None
        columns.append(PNFColumn(
            kind=kind,
            boxes=numeric_boxes,
            first_timestamp=str(raw.get("first_timestamp", "")),
            last_timestamp=str(raw.get("last_timestamp", "")),
        ))
    return columns


def _not_evaluable(rule_id: str) -> Dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": "NOT_EVALUABLE",
        "directional_confirmation": "UNKNOWN",
    }


def evaluate_0030(payload: Dict[str, Any]) -> Dict[str, Any]:
    columns = _normalize_columns(payload)
    if columns is None:
        return _not_evaluable("MURPHY_0030")
    ref = bullish_support_reference(columns)
    if ref is None:
        return _not_evaluable("MURPHY_0030")
    return {**ref, "rule_id": "MURPHY_0030", "status": "PASS", "directional_confirmation": "NEUTRAL"}


def evaluate_0031(payload: Dict[str, Any]) -> Dict[str, Any]:
    columns = _normalize_columns(payload)
    if columns is None:
        return _not_evaluable("MURPHY_0031")
    ref = stop_reference(columns, "BULLISH")
    if ref is None:
        return _not_evaluable("MURPHY_0031")
    return {**ref, "rule_id": "MURPHY_0031", "status": "PASS", "directional_confirmation": "NEUTRAL"}


def evaluate_0032(payload: Dict[str, Any]) -> Dict[str, Any]:
    columns = _normalize_columns(payload)
    if columns is None:
        return _not_evaluable("MURPHY_0032")
    ref = stop_reference(columns, "BEARISH")
    if ref is None:
        return _not_evaluable("MURPHY_0032")
    return {**ref, "rule_id": "MURPHY_0032", "status": "PASS", "directional_confirmation": "NEUTRAL"}
