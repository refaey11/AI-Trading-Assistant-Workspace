"""CSV adapter for MT5 Raw Capture V1.3; no timestamp conversion."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from typing import TextIO
from mt5_raw_capture_contract_v1_3 import CaptureV13Error, payload_hash, validate_raw_bar_v13

EXPECTED_COLUMNS = ("symbol", "timeframe", "bar_time_epoch_seconds_raw", "bar_time_source_clock",
 "bar_time_utc_status", "terminal_time_server_observed", "terminal_time_current_server_observed",
 "host_gmt_estimate_observed", "host_local_time_observed", "broker_server_id", "source_id",
 "capture_version", "is_closed", "open", "high", "low", "close", "tick_volume", "real_volume",
 "spread_points", "volume_type", "observed_server_minus_host_gmt_seconds")
FLOAT_COLUMNS = {"open", "high", "low", "close"}
INT_COLUMNS = {"bar_time_epoch_seconds_raw", "tick_volume", "real_volume", "spread_points",
 "observed_server_minus_host_gmt_seconds"}

def _parse_row(raw: dict[str, str], line: int) -> dict:
    row = dict(raw)
    if row.get("is_closed") not in {"true", "false"}: raise CaptureV13Error(f"CSV_LINE_{line}:IS_CLOSED_INVALID")
    row["is_closed"] = row["is_closed"] == "true"
    try:
        for key in FLOAT_COLUMNS: row[key] = float(row[key])
        for key in INT_COLUMNS:
            value = row[key]
            if not value or value.strip() != value or not value.lstrip("-").isdigit(): raise ValueError(key)
            row[key] = int(value)
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        raise CaptureV13Error(f"CSV_LINE_{line}:NUMERIC_PARSE_FAILED") from exc
    return row

def read_and_validate_csv_v13(stream: TextIO) -> list[dict]:
    reader = csv.DictReader(stream)
    if reader.fieldnames is None: raise CaptureV13Error("CSV_HEADER_MISSING")
    if len(reader.fieldnames) != len(set(reader.fieldnames)): raise CaptureV13Error("CSV_DUPLICATE_HEADER")
    if tuple(reader.fieldnames) != EXPECTED_COLUMNS: raise CaptureV13Error("CSV_HEADER_MISMATCH")
    output, seen = [], {}
    for line, raw in enumerate(reader, start=2):
        if None in raw or any(value is None for value in raw.values()):
            raise CaptureV13Error(f"CSV_LINE_{line}:COLUMN_COUNT_MISMATCH")
        row = _parse_row(raw, line)
        bar = validate_raw_bar_v13(row)
        key = (bar.symbol, bar.timeframe, bar.bar_time_epoch_seconds_raw)
        if key in seen and seen[key] != bar.payload_hash: raise CaptureV13Error("CONFLICTING_DUPLICATE_RAW_BAR")
        if key not in seen:
            seen[key] = bar.payload_hash
            row["payload_hash"] = payload_hash(row)
            output.append(row)
    return output

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MT5 raw-clock V1.3 CSV.")
    parser.add_argument("input_csv", type=Path); parser.add_argument("output_jsonl", type=Path)
    args = parser.parse_args()
    with args.input_csv.open("r", encoding="utf-8-sig", newline="") as source:
        records = read_and_validate_csv_v13(source)
    with args.output_jsonl.open("w", encoding="utf-8", newline="\n") as target:
        for record in records: target.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    print(f"Validated {len(records)} V1.3 raw MT5 bars -> {args.output_jsonl}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
