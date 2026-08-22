"""Source-mapped runtime evaluators for CANDLE_RULE_0011..0020.

All qualitative relationships are represented as upstream categorical facts.
No numeric tolerance is invented for source phrases such as 'nearly equal' or
'approximately equal'. Rules remain Nison confirmation/evidence only.
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
    shadow_relation: str = ""
    doji_isolated: bool = False
    open_inside_previous_body: bool = False
    equal_extreme: bool = False
    close_near_low: bool = False


def _result(rule_id: str, status: str, reason: str) -> Dict[str, Any]:
    return {"rule_id": rule_id, "status": status, "reason": reason,
            "provenance": {"source": "Steve Nison", "lookahead": "none",
                           "numeric_thresholds_invented": False}}


def _trend(ctx: Dict[str, Any]) -> str:
    return str(ctx.get("trend", ""))


def _confirm(ctx: Dict[str, Any]) -> bool:
    return bool(ctx.get("confirmation", {}).get("confirmed", False))


def eval_rule(rule_id: str, candles: list[Candle], ctx: Dict[str, Any]) -> Dict[str, Any]:
    counts = {"CANDLE_RULE_0011": 3, "CANDLE_RULE_0012": 3,
              "CANDLE_RULE_0013": 2, "CANDLE_RULE_0014": 2,
              "CANDLE_RULE_0015": 2, "CANDLE_RULE_0016": 2,
              "CANDLE_RULE_0017": 3, "CANDLE_RULE_0018": 3,
              "CANDLE_RULE_0019": 2, "CANDLE_RULE_0020": 2}
    if rule_id not in counts:
        return _result(rule_id, "NOT_EVALUABLE", "unsupported rule id")
    if len(candles) != counts[rule_id]:
        return _result(rule_id, "NOT_EVALUABLE", f"requires exactly {counts[rule_id]} candles")

    a, b = candles[0], candles[1]
    c = candles[2] if len(candles) == 3 else None

    if rule_id == "CANDLE_RULE_0011":
        if _trend(ctx) != "Uptrend": return _result(rule_id, "FAIL", "requires Uptrend")
        if not (a.body_class == "long" and a.color == "bullish" and b.color == "doji"
                and c.color == "bearish" and c.body_class in {"strong", "long"}):
            return _result(rule_id, "FAIL", "evening doji star formation not satisfied")
        if not _confirm(ctx): return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "evening doji star source-mapped formation")

    if rule_id == "CANDLE_RULE_0012":
        trend = _trend(ctx)
        if trend not in {"Uptrend", "Downtrend"}:
            return _result(rule_id, "NOT_EVALUABLE", "trend must be Uptrend or Downtrend")
        bullish = trend == "Downtrend"
        colors_ok = (a.color == "bearish" and c.color == "bullish") if bullish else (a.color == "bullish" and c.color == "bearish")
        gaps_ok = (b.gap_class == "gap_below_first" and c.gap_class == "gap_above_doji") if bullish else (b.gap_class == "gap_above_first" and c.gap_class == "gap_below_doji")
        if not (a.body_class == "long" and b.color == "doji" and b.doji_isolated and colors_ok and gaps_ok):
            return _result(rule_id, "FAIL", "abandoned baby formation not satisfied")
        if not _confirm(ctx): return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "abandoned baby source-mapped formation")

    if rule_id in {"CANDLE_RULE_0013", "CANDLE_RULE_0014"}:
        if _trend(ctx) not in {"Uptrend", "Downtrend"}:
            return _result(rule_id, "FAIL", "requires existing trend")
        if not (a.body_class == "long" and b.open_inside_previous_body):
            return _result(rule_id, "FAIL", "second real body must remain inside first body")
        if rule_id == "CANDLE_RULE_0014" and b.color != "doji":
            return _result(rule_id, "FAIL", "second candle must be Doji")
        if rule_id == "CANDLE_RULE_0013" and b.body_class != "small":
            return _result(rule_id, "FAIL", "second candle must have a small body")
        if rule_id == "CANDLE_RULE_0013" and not _confirm(ctx):
            return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "harami/harami cross source-mapped formation")

    if rule_id == "CANDLE_RULE_0015":
        if _trend(ctx) != "Uptrend": return _result(rule_id, "FAIL", "requires Uptrend")
        if not a.equal_extreme or not b.equal_extreme:
            return _result(rule_id, "FAIL", "requires equal/nearly-equal highs supplied as categorical fact")
        if not _confirm(ctx): return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "tweezers top source-mapped formation")

    if rule_id == "CANDLE_RULE_0016":
        if _trend(ctx) != "Downtrend": return _result(rule_id, "FAIL", "requires Downtrend")
        if not a.equal_extreme or not b.equal_extreme:
            return _result(rule_id, "FAIL", "requires equal/nearly-equal lows supplied as categorical fact")
        if not _confirm(ctx): return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "tweezers bottom source-mapped formation")

    if rule_id == "CANDLE_RULE_0017":
        if _trend(ctx) != "Uptrend": return _result(rule_id, "FAIL", "requires Uptrend")
        if not (a.body_class == "long" and a.color == "bullish" and b.color == "bearish" and c.color == "bearish"
                and b.gap_class == "gap_above_first" and c.gap_class == "inside_gap_area"):
            return _result(rule_id, "FAIL", "upside gap two crows formation not satisfied")
        if not _confirm(ctx): return _result(rule_id, "FAIL", "confirmation required by source contract")
        return _result(rule_id, "PASS", "upside gap two crows source-mapped formation")

    if rule_id == "CANDLE_RULE_0018":
        if _trend(ctx) != "Uptrend": return _result(rule_id, "FAIL", "requires Uptrend")
        if not all(x.color == "bearish" and x.open_inside_previous_body for x in (b, c)):
            return _result(rule_id, "FAIL", "each candle must open inside previous real body")
        if not all(x.close_near_low for x in (a, b, c)):
            return _result(rule_id, "FAIL", "each candle must close near its own low")
        return _result(rule_id, "PASS", "three black crows source-mapped formation")

    if rule_id == "CANDLE_RULE_0019":
        if _trend(ctx) != "Downtrend": return _result(rule_id, "FAIL", "requires Downtrend")
        ok = (a.color == "bearish" and a.body_class == "long" and b.gap_class == "gap_below_previous_close"
              and b.close_relation == "approximately_equal_previous_close")
        return _result(rule_id, "PASS" if ok else "FAIL", "bullish counterattack lines source-mapped qualitative relation")

    if rule_id == "CANDLE_RULE_0020":
        if _trend(ctx) != "Uptrend": return _result(rule_id, "FAIL", "requires Uptrend")
        ok = (a.color == "bullish" and a.body_class == "long" and b.gap_class == "gap_above_previous_close"
              and b.close_relation == "approximately_equal_previous_close")
        return _result(rule_id, "PASS" if ok else "FAIL", "bearish counterattack lines source-mapped qualitative relation")

    return _result(rule_id, "NOT_EVALUABLE", "unreachable")


def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    candles = [Candle(**c) for c in payload.get("candles", [])]
    return eval_rule(rule_id, candles, payload.get("context", {}))
