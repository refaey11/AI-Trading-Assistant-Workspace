"""Reference Point & Figure core for Murphy 0030-0032.

SOURCE BOUNDARY
---------------
The construction logic is based on John Murphy, Technical Analysis of the
Financial Markets, Chapter 11: 3-box reversal P&F construction. Murphy's
chapter describes using daily High/Low data, checking the continuation side
of the current column first, and only then checking the opposite price for a
3-box reversal.

PROJECT BOUNDARY
----------------
This module is a deterministic reference implementation, not a claim that
Murphy supplied a complete GBPUSD percentage-box formula. Percentage box
size and the logarithmic grid anchor are explicit inputs and must be governed
before production freeze.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

Direction = Literal["X", "O"]


@dataclass(frozen=True)
class PNFConfig:
    box_pct: float
    reversal_boxes: int = 3
    anchor_price: float = 1.0

    def __post_init__(self) -> None:
        if self.box_pct <= 0:
            raise ValueError("box_pct must be > 0")
        if self.reversal_boxes < 1:
            raise ValueError("reversal_boxes must be >= 1")
        if self.anchor_price <= 0:
            raise ValueError("anchor_price must be > 0")

    @property
    def step(self) -> float:
        return 1.0 + self.box_pct


@dataclass
class Column:
    direction: Direction
    boxes: list[int]
    start_timestamp: str
    end_timestamp: str


class PNFReferenceEngine:
    """Deterministic 3-box P&F constructor from completed OHLC bars.

    The engine requires an explicit seed column. It never invents an initial
    direction. For an X column it checks High for continuation first; only if
    High cannot extend X does it check Low for reversal. For an O column the
    order is mirrored: Low continuation first, then High reversal.
    """

    def __init__(self, config: PNFConfig):
        self.config = config
        self.columns: list[Column] = []

    def box_index(self, price: float) -> int:
        if price <= 0:
            raise ValueError("price must be > 0")
        return math.floor(math.log(price / self.config.anchor_price) /
                          math.log(self.config.step) + 1e-12)

    def price_for_box(self, index: int) -> float:
        return self.config.anchor_price * (self.config.step ** index)

    def seed(self, direction: Direction, price: float, timestamp: str) -> None:
        if direction not in ("X", "O"):
            raise ValueError("direction must be X or O")
        if self.columns:
            raise RuntimeError("engine already seeded")
        idx = self.box_index(price)
        self.columns.append(Column(direction, [idx], timestamp, timestamp))

    @property
    def current(self) -> Column:
        if not self.columns:
            raise RuntimeError("engine is not seeded")
        return self.columns[-1]

    def _new_column(self, direction: Direction, boxes: list[int], timestamp: str) -> None:
        self.columns.append(Column(direction, boxes, timestamp, timestamp))

    def process_bar(self, timestamp: str, high: float, low: float) -> str:
        if high < low:
            raise ValueError("high must be >= low")
        cur = self.current
        cur.end_timestamp = timestamp

        if cur.direction == "X":
            top = max(cur.boxes)
            high_idx = self.box_index(high)

            # Murphy construction priority: continue X first.
            if high_idx > top:
                cur.boxes.extend(range(top + 1, high_idx + 1))
                return "CONTINUE_X"

            # Only when X cannot continue do we test Low for reversal.
            reversal_floor = top - (self.config.reversal_boxes - 1)
            low_idx = self.box_index(low)
            if low_idx <= reversal_floor:
                boxes = list(range(low_idx, top))
                self._new_column("O", boxes, timestamp)
                return "REVERSAL_O"
            return "HOLD_X"

        bottom = min(cur.boxes)
        low_idx = self.box_index(low)

        # Mirror construction priority for an O column.
        if low_idx < bottom:
            cur.boxes.extend(range(low_idx, bottom))
            return "CONTINUE_O"

        reversal_ceiling = bottom + (self.config.reversal_boxes - 1)
        high_idx = self.box_index(high)
        if high_idx >= reversal_ceiling:
            boxes = list(range(bottom + 1, high_idx + 1))
            self._new_column("X", boxes, timestamp)
            return "REVERSAL_X"
        return "HOLD_O"
