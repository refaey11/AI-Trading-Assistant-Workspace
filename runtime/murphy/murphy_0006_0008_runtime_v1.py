"""Runtime implementations grounded in frozen project artifacts.
0006/0007 implement the approved operational contract.
0008 fails closed because the project has no approved definition of 'decisively broken'.
"""

def _not_evaluable(rule_id, reason):
    return {"rule_id": rule_id, "status": "NOT_EVALUABLE", "direction": None, "reason": reason}

def evaluate_0006(events, line_price_at):
    return _evaluate_trendline("MURPHY_0006", events, line_price_at, family="LOW", slope="UP")

def evaluate_0007(events, line_price_at):
    return _evaluate_trendline("MURPHY_0007", events, line_price_at, family="HIGH", slope="DOWN")

def _evaluate_trendline(rule_id, events, line_price_at, family, slope):
    required = ["timestamp", "available_at", "family", "line_available_at", "bar_low", "bar_high"]
    if not events or line_price_at is None:
        return _not_evaluable(rule_id, "missing evidence")
    for e in events:
        if any(k not in e for k in required):
            return _not_evaluable(rule_id, "missing required event evidence")
    ordered = sorted(events, key=lambda e: e["timestamp"])
    eligible = [e for e in ordered if e["family"] == family and e["timestamp"] >= e["line_available_at"] and e["available_at"] >= e["line_available_at"]]
    if not eligible:
        return _not_evaluable(rule_id, "no eligible same-family third-touch candidate")
    third = eligible[0]
    lp = line_price_at(third["timestamp"])
    if not (third["bar_low"] <= lp <= third["bar_high"]):
        return _not_evaluable(rule_id, "first candidate does not intersect trendline")
    for e in ordered:
        if e["timestamp"] >= third["timestamp"]:
            p = line_price_at(e["timestamp"])
            if rule_id == "MURPHY_0006" and e["bar_low"] < p:
                return _not_evaluable(rule_id, "confirmed line-hold violation")
            if rule_id == "MURPHY_0007" and e["bar_high"] > p:
                return _not_evaluable(rule_id, "confirmed line-hold violation")
    opposite = "HIGH" if family == "LOW" else "LOW"
    reactions = [e for e in ordered if e["family"] == opposite and e["timestamp"] > third["timestamp"] and e["available_at"] >= third["available_at"]]
    if not reactions:
        return _not_evaluable(rule_id, "missing eligible reaction evidence")
    reaction = reactions[0]
    return {"rule_id": rule_id, "status": "CONFIRMED", "direction": "BULLISH" if slope == "UP" else "BEARISH", "third_touch_timestamp": third["timestamp"], "confirmed_at": reaction["available_at"]}

def evaluate_0008(*_args, **_kwargs):
    return _not_evaluable("MURPHY_0008", "approved decisive-break definition is absent; fail closed")
