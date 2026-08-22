"""Nison source-mapped runtime evaluators for CANDLE_RULE_0003..0010.

Qualitative source language is supplied as categorical upstream facts; no
new numeric tolerances are invented here.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class Candle:
    open: float
    high: float
    low: float
    close: float
    body_class: str = ""
    color: str = ""
    gap_class: str = ""
    close_relation: str = ""

def _result(rule_id: str, status: str, reason: str) -> Dict[str, Any]:
    return {"rule_id": rule_id, "status": status, "reason": reason, "provenance": {"source":"Steve Nison","lookahead":"none","numeric_thresholds_invented":False}}

def _require_trend(ctx: Dict[str, Any], expected: str) -> bool:
    return ctx.get("trend") == expected

def eval_rule(rule_id: str, candles: list[Candle], ctx: Dict[str, Any]) -> Dict[str, Any]:
    if rule_id in {"CANDLE_RULE_0003","CANDLE_RULE_0004","CANDLE_RULE_0005","CANDLE_RULE_0006","CANDLE_RULE_0007"}:
        if len(candles) != 2: return _result(rule_id,"NOT_EVALUABLE","requires exactly 2 candles")
        a,b=candles
    elif rule_id in {"CANDLE_RULE_0008","CANDLE_RULE_0009","CANDLE_RULE_0010"}:
        if len(candles) != 3: return _result(rule_id,"NOT_EVALUABLE","requires exactly 3 candles")
        a,b,c=candles
    else:
        return _result(rule_id,"NOT_EVALUABLE","unsupported rule id")

    if rule_id == "CANDLE_RULE_0003":
        midpoint = (a.open + a.close) / 2.0
        ok = (_require_trend(ctx, "Uptrend") and a.body_class == "long" and a.color == "bullish"
              and b.open > a.high and b.color == "bearish" and b.close < midpoint
              and not (b.open <= a.close and b.close >= a.open))
        return _result(rule_id, "PASS" if ok else "FAIL", "dark cloud cover formation")

    if rule_id == "CANDLE_RULE_0004":
        midpoint = (a.open + a.close) / 2.0
        ok = (_require_trend(ctx, "Downtrend") and a.body_class == "long" and a.color == "bearish"
              and b.open < a.low and b.color == "bullish" and b.close > midpoint
              and not (b.open <= a.close and b.close >= a.open))
        return _result(rule_id, "PASS" if ok else "FAIL", "piercing pattern formation")

    if rule_id == "CANDLE_RULE_0005":
        midpoint = (a.open + a.close) / 2.0
        ok = (_require_trend(ctx, "Downtrend") and a.body_class == "long" and a.color == "bearish"
              and b.open < a.low and b.color == "bullish"
              and b.close_relation == "near_previous_close" and b.close <= midpoint)
        return _result(rule_id, "PASS" if ok else "FAIL", "on neck source-mapped qualitative relation")

    if rule_id == "CANDLE_RULE_0006":
        midpoint = (a.open + a.close) / 2.0
        ok = (_require_trend(ctx, "Downtrend") and a.body_class == "long" and a.color == "bearish"
              and b.open < a.low and b.color == "bullish"
              and b.close_relation == "slightly_above_previous_close" and b.close < midpoint
              and not (b.open <= a.close and b.close >= a.open))
        return _result(rule_id, "PASS" if ok else "FAIL", "in neck source-mapped qualitative relation")

    if rule_id == "CANDLE_RULE_0007":
        midpoint = (a.open + a.close) / 2.0
        ok = (_require_trend(ctx, "Downtrend") and a.body_class == "long" and a.color == "bearish"
              and b.open < a.low and b.color == "bullish"
              and b.close_relation == "well_into_body" and b.close < midpoint
              and not (b.open <= a.close and b.close >= a.open))
        return _result(rule_id, "PASS" if ok else "FAIL", "thrusting source-mapped qualitative relation")

    if rule_id == "CANDLE_RULE_0008":
        midpoint = (a.open + a.close) / 2.0
        ok = (_require_trend(ctx, "Downtrend") and a.body_class == "long" and a.color == "bearish"
              and b.body_class == "small" and c.color == "bullish" and c.body_class == "strong"
              and c.close > midpoint)
        return _result(rule_id, "PASS" if ok else "FAIL", "morning star formation")

    if rule_id == "CANDLE_RULE_0009":
        midpoint = (a.open + a.close) / 2.0
        ok = (_require_trend(ctx, "Uptrend") and a.body_class == "long" and a.color == "bullish"
              and b.body_class == "small" and c.color == "bearish" and c.body_class == "strong"
              and c.close < midpoint)
        return _result(rule_id, "PASS" if ok else "FAIL", "evening star formation")

    if rule_id == "CANDLE_RULE_0010":
        midpoint = (a.open + a.close) / 2.0
        ok = (_require_trend(ctx, "Downtrend") and a.body_class == "long" and a.color == "bearish"
              and b.color == "doji" and c.color == "bullish" and c.body_class == "strong"
              and c.close > midpoint)
        return _result(rule_id, "PASS" if ok else "FAIL", "morning doji star formation")

    return _result(rule_id, "NOT_EVALUABLE", "unreachable")

def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return eval_rule(rule_id, [Candle(**c) for c in payload.get("candles", [])], payload.get("context", {}))
