"""Compatibility wrapper for the Murphy 3-box percentage-based reference tests."""

from copy import deepcopy

from .pnf_3box_reference import PNFBar, PNFColumn, PNF3BoxReference


class PNF3BoxLogReference(PNF3BoxReference):
    """3-box reference engine using a percentage-derived fixed box size.

    This log-facing adapter returns the first completed snapshot of each
    column, so later bars cannot retroactively alter an already published
    prefix record.
    """

    def __init__(self, box_pct: float = 0.01):
        if box_pct <= 0:
            raise ValueError("box_pct must be positive")
        self.box_pct = float(box_pct)
        super().__init__(box_size=1.0, reversal_boxes=3)

    def build(self, bars: list[PNFBar]) -> list[PNFColumn]:
        if bars:
            self.box_size = float(bars[0].close) * self.box_pct
        columns: list[PNFColumn] = []
        published: list[PNFColumn] = []
        for bar in bars:
            before = len(columns)
            self._process_bar(columns, bar)
            if len(columns) > before:
                published.append(deepcopy(columns[-1]))
        self.columns = columns
        return published


__all__ = ["PNFBar", "PNFColumn", "PNF3BoxLogReference"]
