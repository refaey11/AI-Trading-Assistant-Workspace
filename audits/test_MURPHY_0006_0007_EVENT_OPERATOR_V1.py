from datetime import datetime, timedelta

from MURPHY_0006_0007_EVENT_OPERATOR_V1 import D1Bar, Line, PivotEvent, evaluate_event_chain


def _base(rule_id):
    t0 = datetime(2024, 1, 2)
    touch_type = "LOW" if rule_id == "MURPHY_0006" else "HIGH"
    reaction_type = "HIGH" if rule_id == "MURPHY_0006" else "LOW"
    direction = "UP" if rule_id == "MURPHY_0006" else "DOWN"
    touch_price = 1.20 if rule_id == "MURPHY_0006" else 1.30
    reaction_price = 1.25 if rule_id == "MURPHY_0006" else 1.25
    line_price = 1.20 if rule_id == "MURPHY_0006" else 1.30
    line = Line(touch_type, direction, t0)
    pivots = [
        PivotEvent(t0, t0, touch_type, touch_price),
        PivotEvent(t0 + timedelta(days=2), t0 + timedelta(days=2), reaction_type, reaction_price),
    ]
    bars = [
        D1Bar(t0, high=line_price + 0.02, low=line_price),
        D1Bar(t0 + timedelta(days=1), high=line_price + 0.04 if rule_id == "MURPHY_0006" else line_price - 0.01,
              low=line_price + 0.01 if rule_id == "MURPHY_0006" else line_price - 0.04),
        D1Bar(t0 + timedelta(days=2), high=line_price + 0.05 if rule_id == "MURPHY_0006" else line_price - 0.01,
              low=line_price + 0.02 if rule_id == "MURPHY_0006" else line_price - 0.05),
    ]
    return line, pivots, bars, lambda _ts: line_price


def test_0006_valid_chain():
    line, pivots, bars, lp = _base("MURPHY_0006")
    out = evaluate_event_chain("MURPHY_0006", line, lp, pivots, bars)
    assert out is not None
    assert out.rule_id == "MURPHY_0006"


def test_0007_valid_chain():
    line, pivots, bars, lp = _base("MURPHY_0007")
    out = evaluate_event_chain("MURPHY_0007", line, lp, pivots, bars)
    assert out is not None
    assert out.rule_id == "MURPHY_0007"


def test_touch_without_intersection_rejected():
    line, pivots, bars, lp = _base("MURPHY_0006")
    bars[0] = D1Bar(bars[0].timestamp, 1.22, 1.21)
    assert evaluate_event_chain("MURPHY_0006", line, lp, pivots, bars) is None


def test_line_break_rejected():
    line, pivots, bars, lp = _base("MURPHY_0006")
    bars[1] = D1Bar(bars[1].timestamp, 1.24, 1.19)
    assert evaluate_event_chain("MURPHY_0006", line, lp, pivots, bars) is None


def test_wrong_family_rejected():
    line, pivots, bars, lp = _base("MURPHY_0006")
    wrong = Line("HIGH", "DOWN", line.available_at)
    assert evaluate_event_chain("MURPHY_0006", wrong, lp, pivots, bars) is None
