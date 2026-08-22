"""Runtime implementations grounded in the frozen 0006/0007 operational contract."""

def _not_evaluable(rule_id, reason):
    return {"rule_id": rule_id, "status": "NOT_EVALUABLE", "direction": None, "reason": reason}

def evaluate_0006(events, line_price_at):
    return _evaluate_trendline("MURPHY_0006", events, line_price_at, family="LOW", direction="UP")

def evaluate_0007(events, line_price_at):
    return _evaluate_trendline("MURPHY_0007", events, line_price_at, family="HIGH", direction="DOWN")

def _evaluate_trendline(rule_id, events, line_price_at, family, direction):
    required = ["timestamp", "available_at", "family", "line_available_at", "bar_low", "bar_high"]
    if not events or line_price_at is None:
        return _not_evaluable(rule_id, "missing evidence")
    if any(any(k not in e for k in required) for e in events):
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
    return {"rule_id": rule_id, "status": "CONFIRMED", "direction": "BULLISH" if direction == "UP" else "BEARISH", "third_touch_timestamp": third["timestamp"], "confirmed_at": reaction["available_at"]}
