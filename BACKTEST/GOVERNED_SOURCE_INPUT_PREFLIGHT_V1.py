from __future__ import annotations

"""Read-only, fail-closed source input preflight for the 2016-2024 development window.

This module validates source-file integrity and input shape only. It does not
join evidence, infer producer semantics, generate features, run a replay, or
calculate trading performance. H1 2025 rows are counted as excluded OOS rows.
"""

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

START_YEAR = 2016
END_YEAR = 2024
OOS_YEAR = 2025
DEV_YEARS = list(range(START_YEAR, END_YEAR + 1))

MTF_NUMERIC_FIELDS = (
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
)

SOURCE_CONTRACTS = {
    "h1": {
        "required": {"timestamp", "open", "high", "low", "close"},
        "unique_timestamp": True,
        "allow_oos_2025": True,
        "require_full_year_coverage": True,
        "numeric_fields": ("open", "high", "low", "close"),
    },
    "market_state": {
        "required": {"timestamp"},
        "unique_timestamp": True,
        "allow_oos_2025": False,
        "require_full_year_coverage": True,
        "numeric_fields": (),
    },
    "mtf": {
        "required": {"timestamp", *MTF_NUMERIC_FIELDS},
        "unique_timestamp": True,
        "allow_oos_2025": False,
        "require_full_year_coverage": True,
        "numeric_fields": MTF_NUMERIC_FIELDS,
    },
    "murphy": {
        "required": {"timestamp", "status", "direction", "source_rule_id"},
        "unique_timestamp": False,
        "allow_oos_2025": False,
        "require_full_year_coverage": False,
        "numeric_fields": (),
    },
    "nison": {
        "required": {"timestamp", "status", "direction", "rule_id"},
        "unique_timestamp": False,
        "allow_oos_2025": False,
        "require_full_year_coverage": False,
        "numeric_fields": (),
    },
    "historical_context": {
        "required": {"timestamp", "context_signature"},
        "unique_timestamp": False,
        "allow_oos_2025": False,
        "require_full_year_coverage": False,
        "numeric_fields": (),
    },
    "historical_outcome": {
        "required": {"timestamp", "context_signature"},
        "unique_timestamp": False,
        "allow_oos_2025": False,
        "require_full_year_coverage": False,
        "numeric_fields": (),
    },
}


def parse_timestamp(value: str) -> datetime:
    raw = (value or "").strip()
    if not raw:
        raise ValueError("empty timestamp")
    candidate = raw[:-1] + "+00:00" if raw.endswith(("Z", "z")) else raw
    try:
        return datetime.fromisoformat(candidate)
    except ValueError:
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y.%m.%d %H:%M:%S",
            "%Y.%m.%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M",
        ):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
    raise ValueError(f"unsupported timestamp format: {raw[:80]}")


def normalized_timestamp_key(value: datetime) -> str:
    if value.tzinfo is None:
        return "NAIVE:" + value.isoformat()
    return value.astimezone(timezone.utc).isoformat()


def utc_order_key(value: datetime) -> datetime:
    if value.tzinfo is None:
        # Used only to detect ordering. Naive timestamps are separately blocked;
        # this does not assert that their source timezone is UTC.
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_source(key: str, path: Path) -> dict[str, Any]:
    if key not in SOURCE_CONTRACTS:
        raise ValueError(f"unknown source key: {key}")
    contract = SOURCE_CONTRACTS[key]
    report: dict[str, Any] = {
        "source_key": key,
        "path": str(path),
        "status": "BLOCKED",
        "required_columns": sorted(contract["required"]),
        "numeric_fields_checked": list(contract["numeric_fields"]),
        "rows_total": 0,
        "rows_in_development_window": 0,
        "rows_excluded_oos_2025": 0,
        "rows_outside_allowed_window": 0,
        "invalid_timestamps": 0,
        "timezone_naive_timestamps": 0,
        "duplicate_timestamps": 0,
        "out_of_order_rows": 0,
        "invalid_numeric_values": 0,
        "ohlc_violations": 0,
        "year_counts": {},
        "outside_allowed_year_counts": {},
        "invalid_numeric_by_field": {},
        "first_bad_numeric_values": [],
        "first_bad_timestamps": [],
        "first_out_of_order_rows": [],
        "first_outside_allowed_rows": [],
        "development_years_present": [],
        "development_years_missing": DEV_YEARS.copy(),
        "min_timestamp": None,
        "max_timestamp": None,
        "columns": [],
        "errors": [],
        "warnings": [],
    }

    if not path.is_file():
        report["errors"].append("SOURCE_FILE_MISSING")
        return report
    if path.stat().st_size == 0:
        report["errors"].append("SOURCE_FILE_EMPTY")
        return report

    report["size_bytes"] = path.stat().st_size
    report["sha256"] = sha256_file(path)

    seen_timestamps: set[str] = set()
    years: Counter[int] = Counter()
    outside_years: Counter[int] = Counter()
    invalid_numeric_by_field: Counter[str] = Counter()
    min_timestamp: datetime | None = None
    previous_timestamp: datetime | None = None
    max_timestamp: datetime | None = None
    min_order_key: datetime | None = None
    max_order_key: datetime | None = None
    previous_order_key: datetime | None = None
    first_bad_timestamps: list[str] = []
    first_bad_numeric: list[str] = []

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = reader.fieldnames or []
            report["columns"] = columns
            if len(columns) != len(set(columns)):
                report["errors"].append("DUPLICATE_COLUMN_NAMES")
            missing = sorted(contract["required"] - set(columns))
            if missing:
                report["errors"].append("MISSING_REQUIRED_COLUMNS:" + ",".join(missing))
                return report

            for row_number, row in enumerate(reader, start=2):
                report["rows_total"] += 1
                try:
                    ts = parse_timestamp(row.get("timestamp", ""))
                except (TypeError, ValueError) as exc:
                    report["invalid_timestamps"] += 1
                    if len(first_bad_timestamps) < 10:
                        first_bad_timestamps.append(f"row={row_number}:{exc}")
                    continue

                if ts.tzinfo is None:
                    report["timezone_naive_timestamps"] += 1
                order_key = utc_order_key(ts)
                if min_order_key is None or order_key < min_order_key:
                    min_timestamp, min_order_key = ts, order_key
                if max_order_key is None or order_key > max_order_key:
                    max_timestamp, max_order_key = ts, order_key
                if previous_order_key is not None and order_key < previous_order_key:
                    report["out_of_order_rows"] += 1
                    if len(report["first_out_of_order_rows"]) < 10:
                        report["first_out_of_order_rows"].append({
                            "row": row_number,
                            "timestamp": ts.isoformat(),
                            "previous_timestamp": previous_timestamp.isoformat() if previous_timestamp else None,
                        })
                previous_order_key = order_key
                previous_timestamp = ts

                if contract["unique_timestamp"]:
                    key_value = normalized_timestamp_key(ts)
                    if key_value in seen_timestamps:
                        report["duplicate_timestamps"] += 1
                    else:
                        seen_timestamps.add(key_value)

                years[ts.year] += 1
                if START_YEAR <= ts.year <= END_YEAR:
                    report["rows_in_development_window"] += 1
                elif key == "h1" and ts.year == OOS_YEAR:
                    report["rows_excluded_oos_2025"] += 1
                else:
                    report["rows_outside_allowed_window"] += 1
                    outside_years[ts.year] += 1
                    if len(report["first_outside_allowed_rows"]) < 10:
                        report["first_outside_allowed_rows"].append({
                            "row": row_number,
                            "timestamp": ts.isoformat(),
                        })

                numeric_values: dict[str, float] = {}
                for field in contract["numeric_fields"]:
                    raw_value = (row.get(field) or "").strip()
                    try:
                        value = float(raw_value)
                        if not math.isfinite(value):
                            raise ValueError("non-finite")
                        numeric_values[field] = value
                    except (TypeError, ValueError):
                        report["invalid_numeric_values"] += 1
                        invalid_numeric_by_field[field] += 1
                        if len(first_bad_numeric) < 20:
                            first_bad_numeric.append(f"row={row_number}:{field}={raw_value[:80]}")

                if key == "h1" and len(numeric_values) == 4:
                    op, hi, lo, cl = (numeric_values[x] for x in ("open", "high", "low", "close"))
                    if hi < max(op, cl) or lo > min(op, cl) or hi < lo:
                        report["ohlc_violations"] += 1
    except (UnicodeDecodeError, csv.Error, OSError) as exc:
        report["errors"].append(f"CSV_READ_ERROR:{type(exc).__name__}:{exc}")
        return report

    report["year_counts"] = {str(y): years[y] for y in sorted(years)}
    report["outside_allowed_year_counts"] = {
        str(y): outside_years[y] for y in sorted(outside_years)
    }
    report["invalid_numeric_by_field"] = {
        field: invalid_numeric_by_field[field]
        for field in sorted(invalid_numeric_by_field)
    }
    report["first_bad_numeric_values"] = first_bad_numeric
    report["first_bad_timestamps"] = first_bad_timestamps
    report["development_years_present"] = [y for y in DEV_YEARS if years[y] > 0]
    report["development_years_missing"] = [y for y in DEV_YEARS if years[y] == 0]
    report["min_timestamp"] = min_timestamp.isoformat() if min_timestamp else None
    report["max_timestamp"] = max_timestamp.isoformat() if max_timestamp else None

    if report["rows_total"] == 0:
        report["errors"].append("NO_DATA_ROWS")
    if report["invalid_timestamps"]:
        report["errors"].append("INVALID_TIMESTAMPS_PRESENT")
    if report["timezone_naive_timestamps"]:
        report["errors"].append("TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMPS")
    if report["duplicate_timestamps"]:
        report["errors"].append("DUPLICATE_TIMESTAMPS_PRESENT")
    if report["invalid_numeric_values"]:
        report["errors"].append("INVALID_OR_NONFINITE_NUMERIC_VALUES")
    if report["ohlc_violations"]:
        report["errors"].append("OHLC_INVARIANT_VIOLATIONS")
    if report["rows_outside_allowed_window"]:
        report["errors"].append("ROWS_OUTSIDE_ALLOWED_DEVELOPMENT_WINDOW")
    if report["rows_in_development_window"] == 0:
        report["errors"].append("NO_DEVELOPMENT_ROWS")
    if contract["require_full_year_coverage"] and report["development_years_missing"]:
        report["errors"].append(
            "MISSING_DEVELOPMENT_YEARS:" +
            ",".join(str(y) for y in report["development_years_missing"])
        )
    if report["out_of_order_rows"]:
        report["warnings"].append("SOURCE_ROWS_NOT_CHRONOLOGICALLY_ORDERED")
    if key == "h1" and report["rows_excluded_oos_2025"]:
        report["warnings"].append("2025_SOURCE_ROWS_PRESENT_BUT_EXCLUDED_FROM_DEVELOPMENT")
    if key == "h1" and years and max(years) > OOS_YEAR:
        report["errors"].append("H1_SOURCE_CONTAINS_ROWS_AFTER_2025")

    report["status"] = "PASS" if not report["errors"] else "BLOCKED"
    return report


def run_preflight(inputs: dict[str, Path], output: Path, source_manifest: Path | None = None) -> dict[str, Any]:
    expected = set(SOURCE_CONTRACTS)
    supplied = set(inputs)
    missing = sorted(expected - supplied)
    extra = sorted(supplied - expected)

    report: dict[str, Any] = {
        "gate": "GOVERNED_SOURCE_INPUT_PREFLIGHT_V1",
        "scope": "INPUT_SHAPE_AND_WINDOW_ONLY",
        "development_window": {"start_year": START_YEAR, "end_year": END_YEAR},
        "oos_2025": {
            "status": "LOCKED",
            "h1_source_rows_excluded": True,
            "used_for_development": False,
            "used_for_tuning": False,
            "used_for_calibration": False,
        },
        "checks_not_performed": {
            "source_timezone_contract": "NOT_VERIFIED_BEYOND_DETECTING_NAIVE_TIMESTAMPS",
            "producer_formula_lineage": "NOT_VERIFIED",
            "market_state_asof_join": "NOT_VERIFIED",
            "mtf_asof_join_and_close_alignment": "NOT_VERIFIED",
            "murphy_rule_semantic_eligibility": "NOT_VERIFIED_BY_THIS_GATE",
            "nison_confirmation_only_semantics": "NOT_VERIFIED_BY_THIS_GATE",
            "memory_future_isolation": "NOT_VERIFIED",
            "tiz_process_boundary": "NOT_VERIFIED",
            "risk_execution_contract": "NOT_VERIFIED",
            "costs_and_slippage": "NOT_VERIFIED",
            "full_backtest": "NOT_RUN",
            "profitability": "NOT_EVALUATED",
        },
        "promotion_allowed": False,
        "missing_input_keys": missing,
        "unexpected_input_keys": extra,
        "sources": {},
        "errors": [],
    }

    if source_manifest is not None:
        if source_manifest.is_file():
            report["source_manifest_path"] = str(source_manifest)
            report["source_manifest_sha256"] = sha256_file(source_manifest)
        else:
            report["errors"].append("PINNED_SOURCE_MANIFEST_MISSING")

    if missing:
        report["errors"].append("MISSING_INPUTS:" + ",".join(missing))
    if extra:
        report["errors"].append("UNEXPECTED_INPUTS:" + ",".join(extra))

    for key in sorted(expected & supplied):
        report["sources"][key] = inspect_source(key, inputs[key])
        if report["sources"][key]["status"] != "PASS":
            report["errors"].append(f"SOURCE_BLOCKED:{key}")

    all_pass = not report["errors"] and all(
        item["status"] == "PASS" for item in report["sources"].values()
    )
    report["status"] = "PASS_INPUT_PREFLIGHT_ONLY" if all_pass else "BLOCKED"

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for key in SOURCE_CONTRACTS:
        parser.add_argument(f"--{key.replace('_', '-')}", required=True, type=Path)
    parser.add_argument("--source-manifest", type=Path)
    parser.add_argument("--output", type=Path, default=Path("artifacts/gate_a_preflight/source_input_preflight.json"))
    args = parser.parse_args()

    inputs = {key: getattr(args, key) for key in SOURCE_CONTRACTS}
    report = run_preflight(inputs, args.output, args.source_manifest)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS_INPUT_PREFLIGHT_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
