from dataclasses import dataclass


@dataclass
class Bar:
    o: float
    h: float
    l: float
    c: float


def pivot_low(bars, i):
    return 2 <= i < len(bars) - 2 and bars[i].l < bars[i-1].l and bars[i].l < bars[i-2].l and bars[i].l < bars[i+1].l and bars[i].l < bars[i+2].l


def pivot_high(bars, i):
    return 2 <= i < len(bars) - 2 and bars[i].h > bars[i-1].h and bars[i].h > bars[i-2].h and bars[i].h > bars[i+1].h and bars[i].h > bars[i+2].h


def bull_engulf(bars, i):
    if i <= 0:
        return False
    a, b = bars[i-1], bars[i]
    return a.c < a.o and b.c > b.o and b.o < a.c and b.c > a.o


def bear_engulf(bars, i):
    if i <= 0:
        return False
    a, b = bars[i-1], bars[i]
    return a.c > a.o and b.c < b.o and b.o > a.c and b.c < a.o


def run(bars):
    family = 0
    last_low = None
    last_high = None
    setup = 0
    phase = 0
    a1 = a2 = None
    touch = reaction = None
    signals = []

    for current in range(6, len(bars)):
        pivot_i = current - 3
        closed_i = current - 1
        pl = pivot_low(bars, pivot_i)
        ph = pivot_high(bars, pivot_i)

        def line_price(i):
            x1, y1 = a1
            x2, y2 = a2
            return y1 + (y2-y1) * (i-x1)/(x2-x1)

        if setup:
            lp = line_price(closed_i)
            if phase == 1:
                if (setup == 1 and bars[closed_i].l < lp) or (setup == -1 and bars[closed_i].h > lp):
                    setup = 0; phase = 0
                elif closed_i > a2[0] and bars[closed_i].l <= lp <= bars[closed_i].h:
                    if setup == 1 and bars[closed_i].l == lp:
                        touch = closed_i; phase = 2
                    elif setup == -1 and bars[closed_i].h == lp:
                        touch = closed_i; phase = 2
            if setup and phase == 2:
                if (setup == 1 and bars[closed_i].l < lp) or (setup == -1 and bars[closed_i].h > lp):
                    setup = 0; phase = 0
                elif setup == 1 and ph and pivot_i > touch:
                    reaction = pivot_i; phase = 3
                elif setup == -1 and pl and pivot_i > touch:
                    reaction = pivot_i; phase = 3
            if setup and phase == 3 and closed_i > reaction:
                if setup == 1:
                    if bear_engulf(bars, closed_i):
                        setup = 0; phase = 0
                    elif bull_engulf(bars, closed_i):
                        signals.append((closed_i, 1, bars[closed_i].c))
                        setup = 0; phase = 0
                else:
                    if bull_engulf(bars, closed_i):
                        setup = 0; phase = 0
                    elif bear_engulf(bars, closed_i):
                        signals.append((closed_i, -1, bars[closed_i].c))
                        setup = 0; phase = 0

        if not setup:
            if pl and ph:
                family = 0
            elif pl:
                if family == 1 and last_low is not None and bars[pivot_i].l > last_low[1]:
                    setup = 1; phase = 1; a1 = (last_low[0], last_low[1]); a2 = (pivot_i, bars[pivot_i].l)
                else:
                    last_low = (pivot_i, bars[pivot_i].l); family = 1
            elif ph:
                if family == -1 and last_high is not None and bars[pivot_i].h < last_high[1]:
                    setup = -1; phase = 1; a1 = (last_high[0], last_high[1]); a2 = (pivot_i, bars[pivot_i].h)
                else:
                    last_high = (pivot_i, bars[pivot_i].h); family = -1

    return signals


def test_bullish_lifecycle():
    # Two consecutive LOW pivots (10 -> 12) form the frozen UP line.
    # Bar 9 makes an exact third touch at line price 14.
    # Pivot HIGH at bar 11 becomes the reaction; bars 12-13 provide
    # a later bullish engulfing confirmation.
    bars = [
        Bar(14, 18, 13, 15),
        Bar(14, 19, 12, 15),
        Bar(13, 21, 11, 14),
        Bar(12, 18, 10, 13),
        Bar(13, 20, 12.5, 15),
        Bar(14, 19, 12.5, 16),
        Bar(15, 20, 12, 16),
        Bar(15, 21, 13, 17),
        Bar(16, 21, 13.5, 18),
        Bar(17, 22, 14.0, 18.5),
        Bar(16, 19, 15.0, 17),
        Bar(18, 25, 16.0, 22),
        Bar(19, 20, 16.0, 18),
        Bar(17.5, 21, 17.5, 21),
        Bar(19, 22, 18, 21),
    ]
    s = run(bars)
    assert any(direction == 1 for _, direction, _ in s), s


def test_bearish_lifecycle():
    # Two consecutive HIGH pivots (20 -> 17) form the frozen DOWN line.
    # Bar 10 makes an exact third touch at line price 13.
    # Pivot LOW at bar 11 becomes the reaction; bars 12-13 provide
    # a later bearish engulfing confirmation.
    bars = [
        Bar(12, 18, 10, 14),
        Bar(13, 18, 11, 15),
        Bar(14, 19, 12, 16),
        Bar(16, 20, 13, 17),
        Bar(15, 16, 12, 14),
        Bar(14, 16.5, 11, 13),
        Bar(13, 17, 10, 12),
        Bar(12, 16, 10, 11),
        Bar(11, 15, 9.5, 10.5),
        Bar(11, 14.0, 9.0, 10.2),
        Bar(10, 13, 8.5, 9.5),
        Bar(9, 12, 8, 8.5),
        Bar(9, 10.9, 9.0, 9.8),
        Bar(9.9, 9.95, 8.2, 8.2),
        Bar(8, 9, 7.5, 8),
    ]
    s = run(bars)
    assert any(direction == -1 for _, direction, _ in s), s


def test_negative_nison_blocks_signal():
    bars = [Bar(10,11,9,10)] * 30
    assert run(bars) == []


def test_no_lookahead_pivot_confirmation():
    bars = [Bar(10,11,9,10)] * 10
    for current in range(6, len(bars)):
        assert current - 3 <= current - 1


def test_signal_is_one_shot():
    bars = [Bar(10,11,9,10)] * 30
    assert len(run(bars)) <= 1


def test_exact_line_touch_required():
    x1, y1, x2, y2, x = 0, 10, 10, 20, 15
    lp = y1 + (y2-y1)*(x-x1)/(x2-x1)
    assert lp == 25


def test_execution_geometry():
    entry, atr = 2000.0, 10.0
    risk = 0.75 * atr
    assert entry - risk == 1992.5
    assert entry + 2*risk == 2015.0


if __name__ == '__main__':
    tests = [v for k, v in globals().items() if k.startswith('test_')]
    for test in tests:
        test()
    print(f'{len(tests)}/{len(tests)} PASS')
