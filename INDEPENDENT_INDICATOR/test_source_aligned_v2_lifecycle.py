from dataclasses import dataclass
from typing import Optional

@dataclass
class Pivot:
    kind: str
    time: int
    price: float

class Lifecycle:
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
        return self.a1.price + (self.a2.price - self.a1.price) * (
            (t - self.a1.time) / (self.a2.time - self.a1.time)
        )

    def consider_low_touch(self, p: Pivot):
        if self.a2 and p.time > self.a2.time and p.time >= self.line_available_time:
            if p.price <= self.projected_line(p.time):
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
            self.nison_armed and self.engulf_time is not None
            and now > self.engulf_time and close > self.engulf_level
        ):
            self.nison_pass = True

def test_a2_is_not_third_touch():
    x = Lifecycle()
    x.add_anchor(Pivot("LOW", 10, 100)); x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 20, 105))
    assert not x.third_candidate

def test_third_touch_requires_time_after_a2():
    x = Lifecycle()
    x.add_anchor(Pivot("LOW", 10, 100)); x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 30, 108))
    assert x.third_candidate and x.third_time == 30

def test_reaction_completes_murphy():
    x = Lifecycle()
    x.add_anchor(Pivot("LOW", 10, 100)); x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 30, 108)); x.reaction_high(Pivot("HIGH", 40, 115))
    assert x.murphy_pass and not x.third_candidate

def test_stale_nison_cannot_leak():
    x = Lifecycle()
    x.nison_pattern(5, 110); x.nison_break(6, 111)
    assert not x.nison_pass
    x.add_anchor(Pivot("LOW", 10, 100)); x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 30, 108)); x.reaction_high(Pivot("HIGH", 40, 115))
    x.arm_nison_after_murphy(40)
    assert not x.nison_pass and x.engulf_time is None

def test_current_nison_can_pass():
    x = Lifecycle()
    x.add_anchor(Pivot("LOW", 10, 100)); x.add_anchor(Pivot("LOW", 20, 105))
    x.consider_low_touch(Pivot("LOW", 30, 108)); x.reaction_high(Pivot("HIGH", 40, 115))
    x.arm_nison_after_murphy(40); x.nison_pattern(41, 115); x.nison_break(42, 116)
    assert x.nison_pass

if __name__ == "__main__":
    tests = [test_a2_is_not_third_touch, test_third_touch_requires_time_after_a2,
             test_reaction_completes_murphy, test_stale_nison_cannot_leak,
             test_current_nison_can_pass]
    for test in tests:
        test()
    print(f"SOURCE-ALIGNED V2 LIFECYCLE TEST: {len(tests)}/{len(tests)} PASS")
