"""Source-faithful 3-box Point & Figure construction core for Murphy 0030-0032.

Source boundary: John J. Murphy, Technical Analysis of the Financial Markets,
Chapter 11, 3-box reversal construction.

Important: box-size selection and initial-chart bootstrap are explicit project
parameters. They are NOT claimed to be verbatim Murphy numeric prescriptions.
"""
from dataclasses import dataclass
from math import floor, ceil
from typing import Literal, Optional


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


class PNF3BoxReference:
    """Deterministic 3-box P&F engine using D1 High/Low construction.

    Murphy construction boundary:
    - X column: inspect High first; if another X box can be filled, fill it and
      ignore Low for that day. Only when High cannot continue do we inspect Low
      for a 3-box reversal.
    - O column: inspect Low first; if another O box can be filled, fill it and
      ignore High for that day. Only when Low cannot continue do we inspect High
      for a 3-box reversal.
    - A reversal creates a new column three boxes in the opposite direction.
    """

    def __init__(self, box_size: float, reversal_boxes: int = 3):
        if box_size <= 0:
            raise ValueError("box_size must be positive")
        if reversal_boxes != 3:
            raise ValueError("Murphy 0030-0032 core is fixed to 3-box reversal")
        self.box_size = float(box_size)
        self.reversal_boxes = 3
        self.columns: list[PNFColumn] = []

    def _floor_box(self, price: float) -> float:
        return floor(price / self.box_size) * self.box_size

    def _ceil_box(self, price: float) -> float:
        return ceil(price / self.box_size) * self.box_size

    def _seed(self, bar: PNFBar) -> PNFColumn:
        # Project bootstrap only. Murphy describes the construction after a
        # column exists; this seed is deliberately isolated so it can later be
        # replaced by an approved project bootstrap without touching the core.
        if bar.close >= bar.open:
            level = self._floor_box(bar.high)
            return PNFColumn("X", [level], bar.timestamp, bar.timestamp)
        level = self._ceil_box(bar.low)
        return PNFColumn("O", [level], bar.timestamp, bar.timestamp)

    def build(self, bars: list[PNFBar]) -> list[PNFColumn]:
        columns: list[PNFColumn] = []
        for bar in bars:
            if bar.high < bar.low:
                raise ValueError(f"invalid OHLC at {bar.timestamp}: high < low")

            if not columns:
                columns.append(self._seed(bar))
                continue

            current = columns[-1]
            if current.kind == "X":
                next_x = current.top + self.box_size
                if bar.high >= next_x:
                    n = int(floor((bar.high - next_x) / self.box_size)) + 1
                    current.boxes.extend(next_x + i * self.box_size for i in range(n))
                    current.last_timestamp = bar.timestamp
                    continue

                reversal_level = current.top - self.reversal_boxes * self.box_size
                if bar.low <= reversal_level:
                    first = current.top - self.box_size
                    boxes = [first - i * self.box_size for i in range(self.reversal_boxes)]
                    columns.append(PNFColumn("O", boxes, bar.timestamp, bar.timestamp))

            else:
                next_o = current.bottom - self.box_size
                if bar.low <= next_o:
                    n = int(floor((next_o - bar.low) / self.box_size)) + 1
                    current.boxes.extend(next_o - i * self.box_size for i in range(n))
                    current.last_timestamp = bar.timestamp
                    continue

                reversal_level = current.bottom + self.reversal_boxes * self.box_size
                if bar.high >= reversal_level:
                    first = current.bottom + self.box_size
                    boxes = [first + i * self.box_size for i in range(self.reversal_boxes)]
                    columns.append(PNFColumn("X", boxes, bar.timestamp, bar.timestamp))

        self.columns = columns
        return columns


def bullish_support_reference(columns: list[PNFColumn]) -> Optional[dict]:
    """Return the 45-degree bullish support origin.

    Source semantics: bullish support line starts from the base of the lowest O
    column. In a P&F grid, a 45-degree line advances one box upward per column.
    This function returns the structural reference; it does not manufacture a
    trade signal.
    """
    o_columns = [(i, c) for i, c in enumerate(columns) if c.kind == "O"]
    if not o_columns:
        return None
    index, origin = min(o_columns, key=lambda item: item[1].bottom)
    return {
        "origin_column_index": index,
        "origin_price": origin.bottom,
        "box_step_per_column": 1,
        "direction": "UP",
        "status": "AVAILABLE",
    }


def stop_reference(columns: list[PNFColumn], direction: Literal["BULLISH", "BEARISH"]) -> Optional[dict]:
    """Return Murphy's P&F stop reference without inventing an offset.

    Bullish: below previous O column.
    Bearish: above previous X column.
    The exact execution offset below/above the reference is intentionally not
    invented here.
    """
    wanted = "O" if direction == "BULLISH" else "X"
    for index in range(len(columns) - 1, -1, -1):
        column = columns[index]
        if column.kind == wanted:
            return {
                "reference_column_index": index,
                "reference_column": wanted,
                "reference_price": column.bottom if wanted == "O" else column.top,
                "placement_relation": "BELOW" if wanted == "O" else "ABOVE",
                "status": "AVAILABLE",
            }
    return None
