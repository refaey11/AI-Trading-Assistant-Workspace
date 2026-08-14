from datetime import datetime, timedelta

from murphy_event_operator_v1 import D1Bar, Line, PivotEvent, evaluate_event_chain

BASE = datetime(2024, 1, 1)


def ts(days):
    return BASE + timedelta(days=days)


def test_0006_valid_chain():
    line = Line("LOW", "UP", ts(1))
    pivots = [
        PivotEvent(ts(2), ts(4), "LOW", 100.0),
        PivotEvent(ts(4), ts(6), "LOW", 101.0),
        PivotEvent(ts(6), ts(8), "HIGH", 110.0),
    ]
    bars = [
        D1Bar(ts(2), 105, 100),
        D1Bar(ts(4), 108, 102),
        D1Bar(ts(6), 112, 106),
    ]
    out = evaluate_event_chain(
        "MURPHY_0006", line,
        lambda t: 100.0 + 1.0 * (t - ts(2)).days,
        pivots, bars,
    )
    assert out is not None
    assert out.third_touch.pivot_type == "LOW"
    assert out.reaction.pivot_type == "HIGH"
    assert out.confirmation_available_at == ts(8)


def test_0007_valid_chain():
    line = Line("HIGH", "DOWN", ts(1))
    pivots = [
        PivotEvent(ts(2), ts(4), "HIGH", 110.0),
        PivotEvent(ts(4), ts(6), "HIGH", 109.0),
        PivotEvent(ts(6), ts(8), "LOW", 100.0),
    ]
    bars = [
        D1Bar(ts(2), 110, 104),
        D1Bar(ts(4), 106, 101),
        D1Bar(ts(6), 103, 99),
    ]
    out = evaluate_event_chain(
        "MURPHY_0007", line,
        lambda t: 110.0 - 1.0 * (t - ts(2)).days,
        pivots, bars,
    )
    assert out is not None
    assert out.third_touch.pivot_type == "HIGH"
    assert out.reaction.pivot_type == "LOW"


def test_touch_without_intersection_does_not_confirm():
    line = Line("LOW", "UP", ts(1))
    pivots = [
        PivotEvent(ts(2), ts(4), "LOW", 90),
        PivotEvent(ts(4), ts(6), "HIGH", 110),
    ]
    bars = [
        D1Bar(ts(2), 95, 91),
        D1Bar(ts(4), 100, 95),
        D1Bar(ts(6), 112, 105),
    ]
    out = evaluate_event_chain(
        "MURPHY_0006", line, lambda t: 100.0, pivots, bars
    )
    assert out is None


def test_break_after_touch_blocks_confirmation():
    line = Line("LOW", "UP", ts(1))
    pivots = [
        PivotEvent(ts(2), ts(4), "LOW", 100),
        PivotEvent(ts(4), ts(6), "HIGH", 110),
    ]
    bars = [
        D1Bar(ts(2), 105, 100),
        D1Bar(ts(4), 102, 99),
        D1Bar(ts(6), 112, 106),
    ]
    out = evaluate_event_chain(
        "MURPHY_0006", line, lambda t: 100.0, pivots, bars
    )
    assert out is None


def test_line_availability_prevents_lookahead():
    line = Line("LOW", "UP", ts(5))
    pivots = [
        PivotEvent(ts(2), ts(3), "LOW", 100),
        PivotEvent(ts(4), ts(6), "HIGH", 110),
    ]
    bars = [
        D1Bar(ts(4), 105, 100),
        D1Bar(ts(5), 108, 102),
        D1Bar(ts(6), 112, 106),
    ]
    out = evaluate_event_chain(
        "MURPHY_0006", line, lambda t: 100.0, pivots, bars
    )
    assert out is None


def test_market_event_ordering_is_not_availability_ordering():
    line = Line("LOW", "UP", ts(1))
    # Earlier market event has later availability; it must remain first.
    pivots = [
        PivotEvent(ts(2), ts(10), "LOW", 100.0),
        PivotEvent(ts(3), ts(5), "LOW", 100.0),
        PivotEvent(ts(4), ts(11), "HIGH", 110.0),
    ]
    bars = [
        D1Bar(ts(2), 101, 100),
        D1Bar(ts(3), 102, 101),
        D1Bar(ts(4), 112, 106),
    ]
    out = evaluate_event_chain(
        "MURPHY_0006", line, lambda t: 100.0, pivots, bars
    )
    assert out is not None
    assert out.third_touch.timestamp == ts(2)


def test_first_same_family_candidate_cannot_be_skipped_even_if_later_one_would_pass():
    line = Line("LOW", "UP", ts(1))
    # The first eligible LOW misses the line. A later LOW touches and has a
    # valid reaction, but it must NOT replace the first candidate.
    pivots = [
        PivotEvent(ts(2), ts(4), "LOW", 90.0),
        PivotEvent(ts(3), ts(5), "LOW", 100.0),
        PivotEvent(ts(4), ts(6), "HIGH", 110.0),
    ]
    bars = [
        D1Bar(ts(2), 95, 91),
        D1Bar(ts(3), 101, 99),
        D1Bar(ts(4), 112, 106),
    ]
    out = evaluate_event_chain(
        "MURPHY_0006", line, lambda t: 100.0, pivots, bars
    )
    assert out is None


def test_reaction_must_be_strictly_after_touch_timestamp():
    line = Line("LOW", "UP", ts(1))
    pivots = [
        PivotEvent(ts(2), ts(4), "LOW", 100.0),
        PivotEvent(ts(2), ts(5), "HIGH", 110.0),
        PivotEvent(ts(3), ts(6), "HIGH", 111.0),
    ]
    bars = [
        D1Bar(ts(2), 105, 100),
        D1Bar(ts(3), 112, 106),
    ]
    out = evaluate_event_chain(
        "MURPHY_0006", line, lambda t: 100.0, pivots, bars
    )
    assert out is not None
    assert out.reaction.timestamp == ts(3)
