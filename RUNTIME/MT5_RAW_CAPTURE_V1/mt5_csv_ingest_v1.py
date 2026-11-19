"""Strict CSV adapter for MT5_Raw_Capture_Only_V1 output."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import TextIO

from mt5_raw_capture_contract_v1 import (
    CaptureValidationError,
    canonical_payload_hash,
    validate_batch,
    validate_raw_bar,
)

EXPECTED_COLUMNS = (
    "symbol", "timeframe", "bar_time_mt5_utc", "terminal_time_server",
    "terminal_time_current_server", "host_gmt_estimate_utc",
    "host_local_time_observed", "broker_server_id", "source_id",
    "capture_version", "is_closed", "open", "high", "low", "close",
    "tick_volume", "real_volume", "spread_points", "volume_type",
    "observed_server_minus_host_gmt_seconds",
)
FLOAT_COLUMNS = {"open", "high", "low", "close"}
INT_COLUMNS = {
    "tick_volume", "real_volume", "spread_points",
    "observed_server_minus_host_gmt_seconds",
}


def _parse_row(raw: dict[str, str], line_number: int) -> dict:
    row = dict(raw)
    if row.get("is_closed") not in {"true", "false"}:
        raise CaptureValidationError(f"CSV_LINE_{line_number}:IS_CLOSED_INVALID")
    row["is_closed"] = row["is_closed"] == "true"

    try:
        for field in FLOAT_COLUMNS:
            row[field] = float(row[field])
        for field in INT_COLUMNS:
            # Reject decimal/exponential representations for integer source fields.
            value = row[field]
            if not value or value.strip() != value or not value.lstrip("-").isdigit():
                raise ValueError(field)
            row[field] = int(value)
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        raise CaptureValidationError(f"CSV_LINE_{line_number}:NUMERIC_PARSE_FAILED") from exc

    if row["tick_volume"] < 0 or row["real_volume"] < 0 or row["spread_points"] < 0:
        raise CaptureValidationError(f"CSV_LINE_{line_number}:NEGATIVE_VOLUME_OR_SPREAD")
    return row


def read_and_validate_csv(stream: TextIO) -> list[dict]:
    reader = csv.DictReader(stream)
    if reader.fieldnames is None:
        raise CaptureValidationError("CSV_HEADER_MISSING")
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise CaptureValidationError("CSV_DUPLICATE_HEADER")
    if tuple(reader.fieldnames) != EXPECTED_COLUMNS:
        raise CaptureValidationError("CSV_HEADER_MISMATCH")

    records = []
    for line_number, raw in enumerate(reader, start=2):
        if None in raw or any(value is None for value in raw.values()):
            raise CaptureValidationError(f"CSV_LINE_{line_number}:COLUMN_COUNT_MISMATCH")
        row = _parse_row(raw, line_number)
        validate_raw_bar(row)
        row["payload_hash"] = canonical_payload_hash(row)
        records.append(row)

    # Enforce deterministic duplicate behavior across the whole input file.
    validate_batch(records)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and normalize MT5 raw capture CSV.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_jsonl", type=Path)
    args = parser.parse_args()

    with args.input_csv.open("r", encoding="utf-8-sig", newline="") as source:
        records = read_and_validate_csv(source)

    with args.output_jsonl.open("w", encoding="utf-8", newline="\n") as target:
        for record in records:
            target.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")

    print(f"Validated {len(records)} MT5 raw bars -> {args.output_jsonl}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
