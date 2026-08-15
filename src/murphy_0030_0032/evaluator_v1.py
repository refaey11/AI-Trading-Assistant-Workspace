"""Murphy 0030-0032 evidence evaluator.

Evidence only: this module never creates entries or trades.
0030 is structural support-line origin evidence; 0031/0032 are risk-only
stop references. Box/bootstrap mechanics are project operationalizations.
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
    role: str
    availability_timestamp: Optional[str]
    reference_column_index: Optional[int] = None
    reference_price: Optional[float] = None
    placement_relation: Optional[str] = None
    entry_trigger: Optional[str] = None


def _missing(rule_id: str, direction: str, evidence_type: str, role: str) -> RuleEvidence:
    return RuleEvidence(
        rule_id=rule_id,
        status="NOT_EVALUABLE",
        direction=direction,
        evidence_type=evidence_type,
        role=role,
        availability_timestamp=None,
    )


def evaluate_0030(columns: list[PNFColumn], availability_timestamp: str) -> RuleEvidence:
    """Return the lowest-O support-line ORIGIN only.

    The source rule describes a 45-degree bullish support trendline from this
    origin. This evaluator intentionally does not manufacture the trendline
    projection or an entry trigger because that operator is not source-locked.
    """
    o_columns = [(i, c) for i, c in enumerate(columns) if c.kind == "O"]
    if not o_columns:
        return _missing(
            "MURPHY_0030", "BULLISH", "PNF_BULLISH_SUPPORT_ORIGIN", "STRUCTURAL_REFERENCE"
        )

    index, origin = min(o_columns, key=lambda item: item[1].bottom)
    return RuleEvidence(
        rule_id="MURPHY_0030",
        status="AVAILABLE",
        direction="BULLISH",
        evidence_type="PNF_BULLISH_SUPPORT_ORIGIN",
        role="STRUCTURAL_REFERENCE",
        availability_timestamp=availability_timestamp,
        reference_column_index=index,
        reference_price=origin.bottom,
        entry_trigger=None,
    )


def evaluate_0031(columns: list[PNFColumn], availability_timestamp: str) -> RuleEvidence:
    if len(columns) < 2 or columns[-1].kind != "X" or columns[-2].kind != "O":
        return _missing(
            "MURPHY_0031", "BULLISH", "PNF_LONG_STOP_REFERENCE", "RISK_REFERENCE"
        )

    previous_index = len(columns) - 2
    previous_o = columns[previous_index]
    return RuleEvidence(
        rule_id="MURPHY_0031",
        status="AVAILABLE",
        direction="BULLISH",
        evidence_type="PNF_LONG_STOP_REFERENCE",
        role="RISK_REFERENCE",
        availability_timestamp=availability_timestamp,
        reference_column_index=previous_index,
        reference_price=previous_o.bottom,
        placement_relation="BELOW_PREVIOUS_O_COLUMN",
        entry_trigger=None,
    )


def evaluate_0032(columns: list[PNFColumn], availability_timestamp: str) -> RuleEvidence:
    if len(columns) < 2 or columns[-1].kind != "O" or columns[-2].kind != "X":
        return _missing(
            "MURPHY_0032", "BEARISH", "PNF_SHORT_STOP_REFERENCE", "RISK_REFERENCE"
        )

    previous_index = len(columns) - 2
    previous_x = columns[previous_index]
    return RuleEvidence(
        rule_id="MURPHY_0032",
        status="AVAILABLE",
        direction="BEARISH",
        evidence_type="PNF_SHORT_STOP_REFERENCE",
        role="RISK_REFERENCE",
        availability_timestamp=availability_timestamp,
        reference_column_index=previous_index,
        reference_price=previous_x.top,
        placement_relation="ABOVE_PREVIOUS_X_COLUMN",
        entry_trigger=None,
    )


def evaluate_series(bars: list[PNFBar], box_pct: float) -> list[dict]:
    """Evaluate 0030-0032 from completed-bar prefixes only."""
    engine = PNF3BoxLogReference(box_pct=box_pct, reversal_boxes=3)
    snapshots = []
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

        snapshots.append({
            "timestamp": bars[i].timestamp,
            "status": "AVAILABLE",
            "rules": [
                evaluate_0030(columns, bars[i].timestamp),
                evaluate_0031(columns, bars[i].timestamp),
                evaluate_0032(columns, bars[i].timestamp),
            ],
        })
    return snapshots
