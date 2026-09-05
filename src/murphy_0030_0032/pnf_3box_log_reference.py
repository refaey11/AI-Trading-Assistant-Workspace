"""Compatibility wrapper for the Murphy 3-box percentage-based reference tests."""

from .pnf_3box_reference import PNFBar, PNFColumn, PNF3BoxReference


class PNF3BoxLogReference(PNF3BoxReference):
    """3-box reference engine using a percentage-derived fixed box size."""

    def __init__(self, box_pct: float = 0.01):
        if box_pct <= 0:
            raise ValueError("box_pct must be positive")
        self.box_pct = float(box_pct)
        super().__init__(box_size=1.0, reversal_boxes=3)

    def build(self, bars: list[PNFBar]) -> list[PNFColumn]:
        if bars:
            self.box_size = float(bars[0].close) * self.box_pct
        return super().build(bars)


__all__ = ["PNFBar", "PNFColumn", "PNF3BoxLogReference"]
