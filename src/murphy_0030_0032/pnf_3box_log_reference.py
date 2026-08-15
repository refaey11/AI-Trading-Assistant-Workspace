"""Logarithmic 3-box P&F construction for Murphy 0030-0032.

Murphy-compatible project operationalization for Chapter 11. The module
implements the High/Low method and 3-box reversal. The bootstrap is an
explicit project policy based on external P&F construction references; it is
not claimed as verbatim Murphy or Kenneth Tower methodology.
"""
from dataclasses import dataclass
from math import exp, floor, log, ceil
from typing import Literal


class PNFBootstrapAmbiguity(ValueError):
    """Both initial directions qualify on the same completed D1 bar."""


@dataclass(frozen=True)
class PNFBar:
    timestamp: str
    open: float
    high: float
    low: float
    close: float


@dataclass
class PNFColumn:
    kind: Literal["X", "O"]
    boxes: list[float]
    first_timestamp: str
    last_timestamp: str

    @property
    def top(self) -> float:
        return max(self.boxes)

    @property
    def bottom(self) -> float:
        return min(self.boxes)


class PNF3BoxLogReference:
    """Deterministic logarithmic 3-box P&F engine using completed D1 High/Low."""

    def __init__(self, box_pct: float, reversal_boxes: int = 3):
        if box_pct <= 0:
            raise ValueError("box_pct must be positive")
        if reversal_boxes != 3:
            raise ValueError("Murphy 0030-0032 core is fixed to 3-box reversal")
        self.box_pct = float(box_pct)
        self.step = log1p(self.box_pct)
        self.reversal_boxes = 3
        self.columns: list[PNFColumn] = []

    def _floor_box(self, price: float) -> float:
        return exp(floor(log(price) / self.step) * self.step)

    def _ceil_box(self, price: float) -> float:
        return exp(ceil(log(price) / self.step) * self.step)

    def _up(self, price: float, n: int = 1) -> float:
        return price * exp(self.step * n)

    def _down(self, price: float, n: int = 1) -> float:
        return price * exp(-self.step * n)

    def _bootstrap(self, bars: list[PNFBar]) -> tuple[int, PNFColumn]:
        """Find the first direction using a deterministic High/Low bootstrap.

        The first completed bar supplies the initial high/low reference.
        Later completed bars are scanned until either the first upward box above
        the initial high or the first downward box below the initial low is
        reached. If both qualify on the same bar, evaluation is ambiguous and
        must not silently choose a direction.
        """
        if not bars:
            raise ValueError("at least one completed D1 bar is required")

        first = bars[0]
        ref_high = self._floor_box(first.high)
        ref_low = self._ceil_box(first.low)

        for idx in range(1, len(bars)):
            bar = bars[idx]
            up_trigger = self._up(ref_high)
            down_trigger = self._down(ref_low)
            qualifies_x = bar.high >= up_trigger * (1 + 1e-12)
            qualifies_o = bar.low <= down_trigger * (1 - 1e-12)

            if qualifies_x and qualifies_o:
                raise PNFBootstrapAmbiguity(
                    f"bootstrap direction ambiguous at {bar.timestamp}: "
                    "both X and O first-box thresholds qualify"
                )

            if qualifies_x:
                boxes = []
                level = ref_high
                while level <= bar.high * (1 + 1e-12):
                    boxes.append(level)
                    level = self._up(level)
                return idx, PNFColumn("X", boxes, bar.timestamp, bar.timestamp)

            if qualifies_o:
                boxes = []
                level = ref_low
                while level >= bar.low * (1 - 1e-12):
                    boxes.append(level)
                    level = self._down(level)
                return idx, PNFColumn("O", boxes, bar.timestamp, bar.timestamp)

        raise ValueError("P&F bootstrap direction was not established by available data")

    def build(self, bars: list[PNFBar]) -> list[PNFColumn]:
        if any(bar.high < bar.low for bar in bars):
            bad = next(bar for bar in bars if bar.high < bar.low)
            raise ValueError(f"invalid OHLC at {bad.timestamp}: high < low")
        if not bars:
            self.columns = []
            return []

        start_idx, first_column = self._bootstrap(bars)
        columns: list[PNFColumn] = [first_column]

        for bar in bars[start_idx + 1 :]:
            current = columns[-1]
            if current.kind == "X":
                next_box = self._up(current.top)
                if bar.high >= next_box * (1 + 1e-12):
                    level = next_box
                    while level <= bar.high * (1 + 1e-12):
                        current.boxes.append(level)
                        level = self._up(level)
                    current.last_timestamp = bar.timestamp
                    continue

                reversal = self._down(current.top, self.reversal_boxes)
                if bar.low <= reversal * (1 + 1e-12):
                    first = self._down(current.top)
                    boxes = [self._down(first, i) for i in range(self.reversal_boxes)]
                    columns.append(PNFColumn("O", boxes, bar.timestamp, bar.timestamp))

            else:
                next_box = self._down(current.bottom)
                if bar.low <= next_box * (1 - 1e-12):
                    level = next_box
                    while level >= bar.low * (1 - 1e-12):
                        current.boxes.append(level)
                        level = self._down(level)
                    current.last_timestamp = bar.timestamp
                    continue

                reversal = self._up(current.bottom, self.reversal_boxes)
                if bar.high >= reversal * (1 - 1e-12):
                    first = self._up(current.bottom)
                    boxes = [self._up(first, i) for i in range(self.reversal_boxes)]
                    columns.append(PNFColumn("X", boxes, bar.timestamp, bar.timestamp))

        self.columns = columns
        return columns


def log1p(x: float) -> float:
    return log(1.0 + x)
