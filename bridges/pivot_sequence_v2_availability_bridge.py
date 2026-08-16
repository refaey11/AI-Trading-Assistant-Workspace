from __future__ import annotations

from typing import Any, Mapping


def validate_confirmed_pivot_availability(row: Mapping[str, Any]) -> dict[str, Any]:
    """Validate only the canonical PIVOT_SEQUENCE_V2 availability contract.

    This bridge does not select support, define a break, create direction, or
    classify a Murphy rule. It checks the source-backed two-bar confirmation
    chronology only.
    """
    source_row = int(row["source_row"])
    availability_row = int(row["availability_row"])
    confirmation_status = row["confirmation_status"]
    year = int(row.get("year", str(row.get("timestamp", "0000"))[:4]))

    if availability_row - source_row != 2:
        raise ValueError("PIVOT_SEQUENCE_V2 availability must be source_row + 2")
    if confirmation_status != "CONFIRMED_AFTER_2_BARS":
        raise ValueError("Unexpected pivot confirmation status")
    if year == 2025:
        raise ValueError("2025 is OOS and cannot enter this evidence contract")

    return {
        "module": "pivot_sequence_v2_availability",
        "available": True,
        "confirmation_status": confirmation_status,
        "source_row": source_row,
        "availability_row": availability_row,
        "lookahead_safe": availability_row > source_row,
        "decision_hint": "neutral",
    }
