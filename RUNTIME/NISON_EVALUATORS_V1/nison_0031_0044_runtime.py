"""Source-mapped governed runtime evaluators for Nison 0031-0044.

0031-0038 are candlestick continuation patterns. 0039-0044 are frozen
methodology/topic modules. This runtime implements only facts supported by
the existing integrated Nison knowledge base. Qualitative source language
such as "near", "noticeably smaller", and "similar" is represented as an
explicit upstream categorical fact rather than a newly invented numeric
tolerance. Nison remains confirmation/context evidence only.
"""
from __future__ import annotations

from typing import Any, Dict, Sequence

PATTERN_RULES = {f"CANDLE_RULE_{i:04d}" for i in range(31, 39)}
MODULE_RULES = {f"NISON_MODULE_{i:04d}" for i in range(39, 45)}


def _result(rule_id: str, status: str, reason: str) -> Dict[str, Any]:
    return {"rule_id": rule_id, "status": status, "reason": reason, "provenance": {"source": "Steve Nison", "lookahead": "none", "numeric_thresholds_invented": False, "standalone_direction": False}}


def _ctx(payload: Dict[str, Any]) -> Dict[str, Any]:
    value = payload.get("context", {}) or {}
    return dict(value) if isinstance(value, dict) else {}


def _confirmed(ctx: Dict[str, Any]) -> bool:
    return bool((ctx.get("confirmation") or {}).get("confirmed", False))


def _candles(payload: Dict[str, Any], minimum: int) -> Sequence[Dict[str, Any]] | None:
    candles = payload.get("candles", []) or []
    return candles if len(candles) >= minimum else None


def _color(c: Dict[str, Any]) -> str:
    return str(c.get("color", ""))


def _body(c: Dict[str, Any]) -> str:
    return str(c.get("body_class", ""))


def _inside_range(c: Dict[str, Any], first: Dict[str, Any]) -> bool:
    return c.get("high") <= first.get("high") and c.get("low") >= first.get("low")


def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx = _ctx(payload)

    if rule_id in MODULE_RULES:
        if ctx.get("evidence_available") is not True:
            return _result(rule_id, "NOT_EVALUABLE", "methodology evidence is not available")
        if ctx.get("role") not in {"confirmation", "context"}:
            return _result(rule_id, "NOT_EVALUABLE", "Nison module role must be confirmation/context")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "frozen methodology module accepted as context/confirmation evidence")

    if rule_id not in PATTERN_RULES:
        return _result(rule_id, "NOT_EVALUABLE", "unsupported rule id")

    if rule_id == "CANDLE_RULE_0038":
        prev = ctx.get("previous_session") or {}
        cur = ctx.get("current_session") or {}
        direction = ctx.get("direction")
        if not prev or not cur or direction not in {"bullish", "bearish"}:
            return _result(rule_id, "NOT_EVALUABLE", "requires previous/current session OHLC and direction")
        ok = prev.get("high") < cur.get("low") if direction == "bullish" else cur.get("high") < prev.get("low")
        return _result(rule_id, "PASS" if ok else "FAIL", "source-mapped Window structural geometry; sessionization remains upstream")

    if rule_id == "CANDLE_RULE_0036":
        trend = ctx.get("trend")
        if trend is None:
            return _result(rule_id, "NOT_EVALUABLE", "requires existing trend")
        if trend not in {"Uptrend", "Downtrend"}:
            return _result(rule_id, "FAIL", "requires existing trend")
        if ctx.get("window_formed") is not True:
            return _result(rule_id, "NOT_EVALUABLE", "requires source-backed Window formation fact")
        if ctx.get("window_closed") is True:
            return _result(rule_id, "FAIL", "Window is completely closed")
        if ctx.get("window_held_as_support_or_resistance") is not True:
            return _result(rule_id, "NOT_EVALUABLE", "requires upstream Window support/resistance hold fact")
        if ctx.get("trend_resumed") is not True:
            return _result(rule_id, "NOT_EVALUABLE", "requires upstream trend-resumption fact")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "Gapping Play source-backed continuation formation")

    candles = _candles(payload, 2)
    if candles is None:
        return _result(rule_id, "NOT_EVALUABLE", "insufficient candle history")

    if rule_id == "CANDLE_RULE_0031":
        if len(candles) < 5:
            return _result(rule_id, "NOT_EVALUABLE", "requires five-candle continuation structure")
        a, b, c, d, e = candles[-5:]
        if ctx.get("trend") != "Downtrend":
            return _result(rule_id, "FAIL", "requires existing Downtrend")
        if not (_body(a) == "long" and _color(a) == "bearish"):
            return _result(rule_id, "FAIL", "first candle must be long bearish")
        for x in (b, c, d):
            if _color(x) not in {"bullish", "bearish"} or not _inside_range(x, a):
                return _result(rule_id, "FAIL", "three small correction candles must remain inside first candle range")
            if _body(x) not in {"small", "doji"}:
                return _result(rule_id, "FAIL", "correction candles must be small")
        if not (_body(e) == "long" and _color(e) == "bearish"):
            return _result(rule_id, "FAIL", "final candle must be long bearish")
        if not (e.get("open", 0) < d.get("close", 0) and e.get("close", 0) < a.get("close", 0)):
            return _result(rule_id, "FAIL", "final candle completion conditions not satisfied")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "Three Falling Methods source-backed formation")

    if rule_id == "CANDLE_RULE_0032":
        if len(candles) < 3:
            return _result(rule_id, "NOT_EVALUABLE", "requires three candles")
        a, b, c = candles[-3:]
        if not all(_color(x) == "bullish" and _body(x) == "long" for x in (a, b, c)):
            return _result(rule_id, "FAIL", "requires three consecutive long white candles")
        if not (b.get("close", 0) > a.get("close", 0) and c.get("close", 0) > b.get("close", 0)):
            return _result(rule_id, "FAIL", "closes must progress higher")
        if not all(x.get("close_at_high") is True for x in (a, b, c)):
            return _result(rule_id, "NOT_EVALUABLE", "source phrase 'at or near its high' requires upstream categorical fact")
        if not all(x.get("open_within_or_near_previous_body") is True for x in (b, c)):
            return _result(rule_id, "NOT_EVALUABLE", "source phrase 'within or near previous body' requires upstream categorical fact")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "Three White Soldiers source-backed formation")

    if rule_id == "CANDLE_RULE_0033":
        if len(candles) < 3:
            return _result(rule_id, "NOT_EVALUABLE", "requires three candles")
        a, b, c = candles[-3:]
        if not all(_color(x) == "bullish" for x in (a, b, c)):
            return _result(rule_id, "FAIL", "requires three white candles")
        if not (b.get("high", 0) > a.get("high", 0) and c.get("high", 0) > b.get("high", 0)):
            return _result(rule_id, "FAIL", "second and third candles must make higher highs")
        if _body(b) != "long":
            return _result(rule_id, "FAIL", "second candle must be long")
        if c.get("noticeably_smaller_than_previous") is not True:
            return _result(rule_id, "NOT_EVALUABLE", "source phrase 'noticeably smaller' requires upstream categorical fact")
        if not (c.get("is_star_above_previous") is True or c.get("opens_on_previous_shoulder") is True):
            return _result(rule_id, "NOT_EVALUABLE", "source describes final candle as star or shoulder-open; upstream classification required")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "Advance Block source-backed formation")

    if rule_id == "CANDLE_RULE_0034":
        a, b = candles[-2:]
        if ctx.get("trend") != "Uptrend":
            return _result(rule_id, "FAIL", "requires existing Uptrend")
        if not (_color(a) == "bearish" and _color(b) == "bullish"):
            return _result(rule_id, "FAIL", "requires opposite-color black then white candles")
        if a.get("open") != b.get("open"):
            return _result(rule_id, "FAIL", "second candle must open at the same price")
        if b.get("close", 0) <= b.get("open", 0):
            return _result(rule_id, "FAIL", "second candle must close above its open")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "Separating Lines source-backed formation")

    if rule_id == "CANDLE_RULE_0035":
        if len(candles) < 3:
            return _result(rule_id, "NOT_EVALUABLE", "requires three candles")
        _, b, c = candles[-3:]
        trend = ctx.get("trend")
        if trend == "Uptrend":
            if not (_color(b) == "bullish" and _color(c) == "bearish"):
                return _result(rule_id, "FAIL", "bullish Tasuki requires bullish window candle then bearish counter-candle")
            if b.get("gap_class") != "gap_above_previous_high":
                return _result(rule_id, "NOT_EVALUABLE", "bullish Window fact required upstream")
            if not (c.get("open_inside_previous_body") is True and c.get("close_inside_window") is True and c.get("window_closed") is False):
                return _result(rule_id, "NOT_EVALUABLE", "Tasuki window-open/inside-window categorical facts required upstream")
        elif trend == "Downtrend":
            if not (_color(b) == "bearish" and _color(c) == "bullish"):
                return _result(rule_id, "FAIL", "bearish Tasuki requires bearish window candle then bullish counter-candle")
            if b.get("gap_class") != "gap_below_previous_low":
                return _result(rule_id, "NOT_EVALUABLE", "bearish Window fact required upstream")
            if not (c.get("open_inside_previous_body") is True and c.get("close_inside_window") is True and c.get("window_closed") is False):
                return _result(rule_id, "NOT_EVALUABLE", "Tasuki window-open/inside-window categorical facts required upstream")
        else:
            return _result(rule_id, "FAIL", "requires existing Uptrend or Downtrend")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "Tasuki Gap source-backed continuation formation")

    if rule_id == "CANDLE_RULE_0037":
        a, b = candles[-2:]
        if ctx.get("trend") != "Uptrend":
            return _result(rule_id, "FAIL", "bullish Side-by-Side White Lines requires Uptrend")
        if ctx.get("window_formed") is not True or ctx.get("window_closed") is True:
            return _result(rule_id, "NOT_EVALUABLE", "requires an open bullish Window fact")
        if not (_color(a) == "bullish" and _color(b) == "bullish"):
            return _result(rule_id, "FAIL", "requires two white candles")
        if not (a.get("opens_at_approximately_same_price_as_previous") is True and b.get("opens_at_approximately_same_price_as_previous") is True):
            return _result(rule_id, "NOT_EVALUABLE", "source phrase 'approximately the same price' requires upstream categorical fact")
        if not (a.get("body_similar_to_previous") is True and b.get("body_similar_to_previous") is True):
            return _result(rule_id, "NOT_EVALUABLE", "source phrase 'similar in size' requires upstream categorical fact")
        if not _confirmed(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "Side-by-Side White Lines source-backed continuation formation")

    return _result(rule_id, "NOT_EVALUABLE", "unreachable")
