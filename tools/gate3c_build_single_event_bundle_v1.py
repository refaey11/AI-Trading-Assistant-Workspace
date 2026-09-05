#!/usr/bin/env python3
"""Build the Gate 3C input bundle for one timestamped event.

The Murphy fan-in is deliberately checked at this boundary.  A partial fan-in
must never be represented as a successful Gate 3C event.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


MURPHY_IDS = (
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007",
    "MURPHY_0018", "MURPHY_0019", "MURPHY_0021", "MURPHY_0022",
    "MURPHY_0023", "MURPHY_0025", "MURPHY_0026", "MURPHY_0028",
    "MURPHY_0029", "MURPHY_0030", "MURPHY_0031", "MURPHY_0032",
    "MURPHY_0033", "MURPHY_0034", "MURPHY_0035", "MURPHY_0036",
    "MURPHY_0037", "MURPHY_0038", "MURPHY_0039", "MURPHY_0040",
    "MURPHY_0041", "MURPHY_0042", "MURPHY_0043", "MURPHY_0044",
    "MURPHY_0045", "MURPHY_0047", "MURPHY_0048", "MURPHY_0049",
    "MURPHY_0050", "MURPHY_0051",
)


def murphy_coverage(rule_ids: Iterable[object]) -> dict[str, Any]:
    """Return the complete, fail-closed coverage result for the Murphy fan-in."""
    expected = set(MURPHY_IDS)
    observed = {str(rule_id) for rule_id in rule_ids if rule_id is not None}
    missing_rule_ids = sorted(expected - observed)
    unknown_rule_ids = sorted(observed - expected)
    complete = observed == expected
    return {
        "rule_ids": sorted(observed & expected),
        "rule_count": len(observed & expected),
        "missing_rule_ids": missing_rule_ids,
        "unknown_rule_ids": unknown_rule_ids,
        "complete": complete,
    }


def _utc_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _read_murphy_rows(root: Path, target: datetime) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(root.rglob("*.csv")):
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                continue
            id_column = "source_rule_id" if "source_rule_id" in reader.fieldnames else "rule_id"
            if id_column not in reader.fieldnames or "timestamp" not in reader.fieldnames:
                continue
            for row in reader:
                timestamp = row.get("timestamp")
                if timestamp and _utc_timestamp(timestamp) == target:
                    rows.append({**row, "source_rule_id": str(row[id_column]), "source_path": str(path)})
    return rows


def build_bundle(timestamp: str, murphy_root: Path) -> dict[str, Any]:
    """Build the portion of the canonical event owned by the Murphy fan-in."""
    target = _utc_timestamp(timestamp)
    rows = _read_murphy_rows(murphy_root, target)
    coverage = murphy_coverage(row["source_rule_id"] for row in rows)
    murphy = {"rows": rows, **coverage}
    provenance = {
        "murphy_root": str(murphy_root),
        "murphy_row_count": len(rows),
        "missing_rule_ids": coverage["missing_rule_ids"],
        "unknown_rule_ids": coverage["unknown_rule_ids"],
        "complete": coverage["complete"],
    }
    if (
        coverage["missing_rule_ids"]
        or coverage["unknown_rule_ids"]
        or not coverage["complete"]
    ):
        raise RuntimeError("BLOCKED_MURPHY_34_INCOMPLETE")
    return {
        "timestamp": target.isoformat().replace("+00:00", "Z"),
        "murphy": murphy,
        "provenance": provenance,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--murphy-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    # These are accepted by the existing Gate 3C invocation.  They remain
    # opaque here because the canonical event assembly is owned by callers.
    for name in ("h1", "market-state", "nison", "mtf-root", "historical-context-root",
                 "historical-outcome-root", "similarity-root", "retrieval-root"):
        parser.add_argument(f"--{name}")
    args = parser.parse_args()
    bundle = build_bundle(args.timestamp, args.murphy_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
