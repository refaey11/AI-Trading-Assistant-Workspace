from dataclasses import dataclass
from typing import Optional


@dataclass
class Pivot:
    kind: str
    time: int
    price: float


class Lifecycle:
    """Small deterministic oracle mirroring the Pine V2 lifecycle invariants."""

    def __init__(self):
        self.a1: Optional[Pivot] = None
        self.a2: Optional[Pivot] = None
        self.line_available_time: Optional[int] = None
        self.third_time: Optional[int] = None
        self.third_candidate = False
        self.murphy_pass = False
        self.nison_armed = False
        self.murphy_pass_time: Optional[int] = None
        self.engulf_time: Optional[int] = None
        self.engulf_level: Optional[float] = None
        self.nison_pass = False

    def add_anchor(self, p: Pivot):
        if self.a1 is None:
            self.a1 = p
        elif self.a2 is None:
            if p.time > self.a1.time and p.price > self.a1.price:
                self.a2 = p
                self.line_available_time = p.time + 3
            else:
                self.a1 = p

    def projected_line(self, t: int):
        assert self.a1 and self.a2
        return self.a1.price + (self.a2.price - self.a1.price) * (
            (t - self.a1.time) / (self.a2.time - self.a1.time)
        )

    def consider_low_touch(self, p: Pivot):
        # Critical invariant: third touch must be strictly after A2.
        if self.a2 and p.time > self.a2.time and p.time >= self.line_available_time:
            lp = self.projected_line(p.time)
            if p.price <= lp:
                self.third_candidate = True
                self.third_time = p.time

    def reaction_high(self, p: Pivot):
        if self.third_candidate and p.time > self.third_time:
            self.murphy_pass = True
            self.third_candidate = False

    def arm_nison_after_murphy(self, now: int):
        if self.murphy_pass and not self.nison_armed:
            self.nison_armed = True
            self.murphy_pass_time = now
            self.nison_pass = False
            self.engulf_time = None
            self.engulf_level = None

    def nison_pattern(self, now: int, high: float):
        if self.nison_armed and self.murphy_pass_time is not None and now > self.murphy_pass_time:
            self.engulf_time = now
            self.engulf_level = high

    def nison_break(self, now: int, close: float):
        if (
            self.nison_armed
            and self.engulf_time is not None
            and now > self.engulf_time
            and self.engulf_level is not None
            and close > self.engulf_level
        ):
            self.nison_pass = True


def test_a2_is_not_third_touch():
    x = Lifecycle()
    x.add_anchor(Pivot("LOW", 10, 100))
    x.add_anchor(Pivot("LOW", 20, 105))
    # A2 itself must never become the third-touch event.
    x.consider_low_touch(Pivot("LOW", 20, 105))
    assert x.third_candidate is False


def test_third_touch_requires_time_after_a2():
    x = Lifecycle()
    x.add_anchor(Pivot("LOW", 10, 100))
    x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 30, 108))
    assert x.third_candidate is True
    assert x.third_time == 30


def test_reaction_completes_murphy():
    x = Lifecycle()
    x.add_anchor(Pivot("LOW", 10, 100))
    x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 30, 108))
    x.reaction_high(Pivot("HIGH", 40, 115))
    assert x.murphy_pass is True
    assert x.third_candidate is False


def test_stale_nison_cannot_leak_before_murphy_pass():
    x = Lifecycle()
    x.nison_pattern(now=5, high=110)
    x.nison_break(now=6, close=111)
    assert x.nison_pass is False
    x.add_anchor(Pivot("LOW", 10, 100))
    x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 30, 108))
    x.reaction_high(Pivot("HIGH", 40, 115))
    x.arm_nison_after_murphy(now=40)
    assert x.nison_pass is False
    assert x.engulf_time is None


def test_current_nison_can_pass_after_murphy():
    x = Lifecycle()
    x.add_anchor(Pivot("LOW", 10, 100))
    x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 30, 108))
    x.reaction_high(Pivot("HIGH", 40, 115))
    x.arm_nison_after_murphy(now=40)
    x.nison_pattern(now=41, high=115)
    x.nison_break(now=42, close=116)
    assert x.nison_pass is True


if __name__ == "__main__":
    tests = [
        test_a2_is_not_third_touch,
        test_third_touch_requires_time_after_a2,
        test_reaction_completes_murphy,
        test_stale_nison_cannot_leak_before_murphy_pass,
        test_current_nison_can_pass_after_murphy,
    ]
    for test in tests:
        test()
    print(f"SOURCE-ALIGNED V2 LIFECYCLE TEST: {len(tests)}/{len(tests)} PASS")
