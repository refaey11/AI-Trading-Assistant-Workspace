from __future__ import annotations

from typing import Any, Iterable, Mapping
import pandas as pd

MURPHY_RULES = [
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007",
    "MURPHY_0018", "MURPHY_0019", "MURPHY_0021", "MURPHY_0022", "MURPHY_0023",
    "MURPHY_0025", "MURPHY_0026", "MURPHY_0028", "MURPHY_0029", "MURPHY_0030",
    "MURPHY_0031", "MURPHY_0032", "MURPHY_0033", "MURPHY_0034", "MURPHY_0035",
    "MURPHY_0036", "MURPHY_0037", "MURPHY_0038", "MURPHY_0039", "MURPHY_0040",
    "MURPHY_0041", "MURPHY_0042", "MURPHY_0043", "MURPHY_0044", "MURPHY_0045",
    "MURPHY_0047", "MURPHY_0048", "MURPHY_0049", "MURPHY_0050", "MURPHY_0051",
]
NISON_RULES = [f"NISON_{i:04d}" for i in range(1, 45)]
ALLOWLIST = tuple(MURPHY_RULES + NISON_RULES)


def build_rule_event_stream(
    timestamps: Iterable[Any],
    *,
    murphy_rows: Iterable[Mapping[str, Any]] = (),
    nison_rows: Iterable[Mapping[str, Any]] = (),
) -> pd.DataFrame:
    """Build a 78-rule OOS evidence stream without inventing missing evidence.

    One row is emitted for every allowlisted rule at every supplied timestamp.
    Existing runtime outputs are copied through. Anything unavailable remains
    NOT_EVALUABLE with an explicit missing-evidence reason.

    This is a coverage/event-stream boundary, not a strategy or profitability
    evaluator. It never creates direction, SL/TP, TIZ psychology, or Risk data.
    """
    ts = sorted(pd.to_datetime(list(timestamps), utc=True).unique())
    records: dict[tuple[pd.Timestamp, str], dict[str, Any]] = {}

    def ingest(rows: Iterable[Mapping[str, Any]], source: str) -> None:
        for raw in rows:
            stamp = pd.Timestamp(raw["timestamp"], tz="UTC")
            rule_id = str(raw["rule_id"])
            if rule_id not in ALLOWLIST:
                raise ValueError(f"rule_id outside frozen allowlist: {rule_id}")
            key = (stamp, rule_id)
            record = records.setdefault(key, {
                "timestamp": stamp,
                "rule_id": rule_id,
                "source": source,
                "status": "NOT_EVALUABLE",
                "available": False,
                "direction": None,
                "reason": "MISSING_AUTHORITATIVE_INPUT",
                "provenance": None,
            })
            record.update({
                "source": source,
                "status": str(raw.get("status", record["status"])),
                "available": bool(raw.get("available", record["available"])),
                "direction": raw.get("direction", record["direction"]),
                "reason": raw.get("reason", record["reason"]),
                "provenance": raw.get("provenance", record["provenance"]),
            })

    ingest(murphy_rows, "Murphy runtime")
    ingest(nison_rows, "Nison runtime")

    out: list[dict[str, Any]] = []
    for stamp in ts:
        for rule_id in ALLOWLIST:
            row = records.get((stamp, rule_id))
            if row is None:
                row = {
                    "timestamp": stamp,
                    "rule_id": rule_id,
                    "source": "verified runtime boundary",
                    "status": "NOT_EVALUABLE",
                    "available": False,
                    "direction": None,
                    "reason": "NO_2025_OUTPUT",
                    "provenance": None,
                }
            out.append(row)

    return pd.DataFrame(out, columns=[
        "timestamp", "rule_id", "source", "status", "available",
        "direction", "reason", "provenance",
    ])


def summarize_coverage(stream: pd.DataFrame) -> dict[str, Any]:
    expected_rules = set(ALLOWLIST)
    observed_rules = set(stream["rule_id"].astype(str))
    timestamps = stream["timestamp"].nunique()
    full_expected = timestamps * len(expected_rules)
    available_rows = int(stream["available"].fillna(False).astype(bool).sum())
    return {
        "runtime_allowlist_count": len(expected_rules),
        "observed_rule_count": len(observed_rules & expected_rules),
        "timestamps": int(timestamps),
        "expected_rule_rows": int(full_expected),
        "actual_rows": int(len(stream)),
        "available_rows": available_rows,
        "availability_rate": (available_rows / full_expected) if full_expected else 0.0,
        "missing_rule_ids": sorted(expected_rules - observed_rules),
        "generated_from_existing_outputs_only": True,
        "2025_tuning": False,
    }
