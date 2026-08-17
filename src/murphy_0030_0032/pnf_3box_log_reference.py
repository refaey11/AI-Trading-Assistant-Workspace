"""Compatibility entrypoint for the Murphy 0030-0032 P&F reference engine.

The canonical implementation lives in ``pnf_3box_reference``.  This module
preserves the existing test/registry entrypoint name without duplicating or
changing construction semantics.
"""

from .pnf_3box_reference import PNF3BoxReference, PNFBar


class PNF3BoxLogReference(PNF3BoxReference):
    """Named compatibility entrypoint for the existing 3-box log-reference tests."""

    pass


__all__ = ["PNF3BoxLogReference", "PNFBar"]
