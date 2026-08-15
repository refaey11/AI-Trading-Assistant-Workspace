"""Logarithmic 3-box P&F construction for Murphy 0030-0032.

This module is a source-compatible project operationalization of Murphy
Chapter 11's logarithmic/percentage P&F construction. It does not claim to
reproduce Kenneth Tower's unpublished volatility-to-box conversion formula.
"""
from dataclasses import dataclass
from math import exp, floor, log, ceil
from typing import Literal


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
    """Deterministic logarithmic 3-box P&F engine using D1 High/Low data."""

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

    def build(self, bars: list[PNFBar]) -> list[PNFColumn]:
        columns: list[PNFColumn] = []
        for bar in bars:
            if bar.high < bar.low:
                raise ValueError(f"invalid OHLC at {bar.timestamp}: high < low")
            if not columns:
                if bar.close >= bar.open:
                    columns.append(PNFColumn("X", [self._floor_box(bar.high)], bar.timestamp, bar.timestamp))
                else:
                    columns.append(PNFColumn("O", [self._ceil_box(bar.low)], bar.timestamp, bar.timestamp))
                continue

            current = columns[-1]
            if current.kind == "X":
                next_box = self._up(current.top)
                if bar.high >= next_box:
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
                if bar.low <= next_box:
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
    # Local helper keeps the module's numerical dependency explicit.
    return log(1.0 + x)
