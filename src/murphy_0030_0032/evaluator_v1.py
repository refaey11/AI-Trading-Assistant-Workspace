"""Murphy 0030-0032 evidence evaluator.

This evaluator consumes the existing deterministic logarithmic 3-box P&F
operationalization and emits rule evidence only. It does not create trades.

Source boundary:
- Murphy 0030 = bullish P&F support reference from the base of the lowest O column.
- Murphy 0031 = long stop reference below the previous O column in an uptrend.
- Murphy 0032 = short stop reference above the previous X column in a downtrend.

Bootstrap and percentage box size are explicit project operational policies,
not verbatim Murphy/Tower formulas.
"""
from dataclasses import dataclass
from typing import Literal, Optional

from .pnf_3box_log_reference import PNF3BoxLogReference, PNFBar, PNFColumn


Status = Literal["AVAILABLE", "NOT_EVALUABLE"]


@dataclass(frozen=True)
class RuleEvidence:
    rule_id: str
    status: Status
    direction: str
    evidence_type: str
    availability_timestamp: Optional[str]
    reference_column_index: Optional[int] = None
    reference_price: Optional[float] = None
    placement_relation: Optional[str] = None


def evaluate_0030(columns: list[PNFColumn], availability_timestamp: str) -> RuleEvidence:
    o_columns = [(i, c) for i, c in enumerate(columns) if c.kind == "O"]
    if not o_columns:
        return RuleEvidence(
            rule_id="MURPHY_0030",
            status="NOT_EVALUABLE",
            direction="BULLISH",
            evidence_type="PNF_BULLISH_SUPPORT_REFERENCE",
            availability_timestamp=None,
        )

    index, origin = min(o_columns, key=lambda item: item[1].bottom)
    return RuleEvidence(
        rule_id="MURPHY_0030",
        status="AVAILABLE",
        direction="BULLISH",
        evidence_type="PNF_BULLISH_SUPPORT_REFERENCE",
        availability_timestamp=availability_timestamp,
        reference_column_index=index,
        reference_price=origin.bottom,
    )


def evaluate_0031(columns: list[PNFColumn], availability_timestamp: str) -> RuleEvidence:
    if len(columns) < 2 or columns[-1].kind != "X" or columns[-2].kind != "O":
        return RuleEvidence(
            rule_id="MURPHY_0031",
            status="NOT_EVALUABLE",
            direction="BULLISH",
            evidence_type="PNF_LONG_STOP_REFERENCE",
            availability_timestamp=None,
        )

    previous_index = len(columns) - 2
    previous_o = columns[previous_index]
    return RuleEvidence(
        rule_id="MURPHY_0031",
        status="AVAILABLE",
        direction="BULLISH",
        evidence_type="PNF_LONG_STOP_REFERENCE",
        availability_timestamp=availability_timestamp,
        reference_column_index=previous_index,
        reference_price=previous_o.bottom,
        placement_relation="BELOW_PREVIOUS_O_COLUMN",
    )


def evaluate_0032(columns: list[PNFColumn], availability_timestamp: str) -> RuleEvidence:
    if len(columns) < 2 or columns[-1].kind != "O" or columns[-2].kind != "X":
        return RuleEvidence(
            rule_id="MURPHY_0032",
            status="NOT_EVALUABLE",
            direction="BEARISH",
            evidence_type="PNF_SHORT_STOP_REFERENCE",
            availability_timestamp=None,
        )

    previous_index = len(columns) - 2
    previous_x = columns[previous_index]
    return RuleEvidence(
        rule_id="MURPHY_0032",
        status="AVAILABLE",
        direction="BEARISH",
        evidence_type="PNF_SHORT_STOP_REFERENCE",
        availability_timestamp=availability_timestamp,
        reference_column_index=previous_index,
        reference_price=previous_x.top,
        placement_relation="ABOVE_PREVIOUS_X_COLUMN",
    )


def evaluate_series(bars: list[PNFBar], box_pct: float) -> list[dict]:
    """Evaluate 0030-0032 after each completed D1 bar.

    Each row is generated from the P&F state available immediately after that
    bar. No future suffix is consulted when producing an earlier row.
    """
    engine = PNF3BoxLogReference(box_pct=box_pct, reversal_boxes=3)
    snapshots = []

    # The engine's public build() is deterministic but does not expose
    # snapshots. Rebuild prefixes so every emitted row is explicitly tied to
    # the information available at that completed bar.
    for i in range(len(bars)):
        prefix = bars[: i + 1]
        try:
            columns = engine.build(prefix)
        except Exception as exc:
            snapshots.append({
                "timestamp": bars[i].timestamp,
                "status": "NOT_EVALUABLE",
                "error": type(exc).__name__,
                "rules": [],
            })
            continue

        rules = [
            evaluate_0030(columns, bars[i].timestamp),
            evaluate_0031(columns, bars[i].timestamp),
            evaluate_0032(columns, bars[i].timestamp),
        ]
        snapshots.append({
            "timestamp": bars[i].timestamp,
            "status": "AVAILABLE",
            "rules": rules,
        })

    return snapshots
