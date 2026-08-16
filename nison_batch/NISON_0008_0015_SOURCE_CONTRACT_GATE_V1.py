"""Fail-closed source contract gate for Nison rules 0008-0015.

This module records only clauses explicitly present in the integrated Nison
registry. It does not invent candle-size, doji, gap, equality, or confirmation
comparators. Where the registry does not provide an approved operator, the
result remains NOT_EVALUABLE.
"""

RULES = {
    "NISON_0008": {"name": "Morning Star", "candles": 3, "trend": "downtrend", "operator": None},
    "NISON_0009": {"name": "Evening Star", "candles": 3, "trend": "uptrend", "operator": None},
    "NISON_0010": {"name": "Morning Doji Star", "candles": 3, "trend": "downtrend", "operator": None},
    "NISON_0011": {"name": "Evening Doji Star", "candles": 3, "trend": "uptrend", "operator": None},
    "NISON_0012": {"name": "Abandoned Baby", "candles": None, "trend": "both", "operator": None},
    "NISON_0013": {"name": "Harami", "candles": 2, "trend": "uptrend_or_downtrend", "operator": None},
    "NISON_0014": {"name": "Harami Cross", "candles": 2, "trend": "uptrend_or_downtrend", "operator": None},
    "NISON_0015": {"name": "Tweezers Top", "candles": 2, "trend": "uptrend", "operator": None},
}


def evaluate(rule_id: str, candle_count: int | None, trend: str | None) -> dict:
    rule = RULES[rule_id]
    if candle_count is None or trend is None:
        return {"rule_id": rule_id, "status": "NOT_EVALUABLE", "reason": "Missing source-declared context"}

    expected = rule["candles"]
    if expected is not None and candle_count != expected:
        return {"rule_id": rule_id, "status": "FAIL", "reason": "Source-declared candle count is not satisfied"}

    trend_ok = (
        rule["trend"] == "both"
        or (rule["trend"] == "downtrend" and trend == "downtrend")
        or (rule["trend"] == "uptrend" and trend == "uptrend")
        or (rule["trend"] == "uptrend_or_downtrend" and trend in {"uptrend", "downtrend"})
    )
    if not trend_ok:
        return {"rule_id": rule_id, "status": "FAIL", "reason": "Source-declared trend context is not satisfied"}

    return {"rule_id": rule_id, "status": "NOT_EVALUABLE", "reason": "No approved source-bounded pattern operator is available for this rule"}
