from __future__ import annotations

"""Create immutable 2016-2024 projections from pinned source CSVs.

Original inputs are never modified. Rows outside the development window are
counted and excluded. Historical outcomes additionally require the full 48h
forward-label horizon to mature strictly before 2025-01-01 UTC.
"""

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

START_YEAR = 2016
END_YEAR = 2024
OOS_START = datetime(2025, 1, 1, tzinfo=timezone.utc)
OUTCOME_MAX_HORIZON_HOURS = 48

REQUIRED_COLUMNS = {
    "market_state": {"timestamp"},
    "historical_context": {"timestamp", "context_signature"},
    "historical_outcome": {
        "timestamp", "context_signature",
        "return_6h", "return_12h", "return_24h", "return_48h",
    },
}


def parse_aware_timestamp(raw: str, *, source: str, row_number: int) -> datetime:
    value = (raw or "").strip()
    if not value:
        raise ValueError(f"EMPTY_TIMESTAMP:{source}:row={row_number}")
    candidate = value[:-1] + "+00:00" if value.endswith(("Z", "z")) else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ValueError(f"INVALID_TIMESTAMP:{source}:row={row_number}:{value[:80]}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"TIMEZONE_PROVENANCE_UNRESOLVED:{source}:row={row_number}:{value[:80]}")
    return parsed


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_source(key: str, source_path: Path, output_path: Path) -> dict[str, Any]:
    if key not in REQUIRED_COLUMNS:
        raise ValueError(f"UNKNOWN_SOURCE_KEY:{key}")
    if not source_path.is_file() or source_path.stat().st_size == 0:
        raise ValueError(f"SOURCE_MISSING_OR_EMPTY:{key}:{source_path}")

    year_counts: Counter[int] = Counter()
    excluded_year_counts: Counter[int] = Counter()
    excluded_oos_maturity = 0
    rows_total = 0
    rows_kept = 0
    first_timestamp = None
    last_timestamp = None

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with source_path.open("r", encoding="utf-8-sig", newline="") as src, output_path.open(
        "w", encoding="utf-8", newline=""
    ) as dst:
        reader = csv.DictReader(src)
        columns = reader.fieldnames or []
        if not columns:
            raise ValueError(f"SOURCE_HEADER_MISSING:{key}")
        missing = sorted(REQUIRED_COLUMNS[key] - set(columns))
        if missing:
            raise ValueError(f"SOURCE_REQUIRED_COLUMNS_MISSING:{key}:{missing}")
        writer = csv.DictWriter(dst, fieldnames=columns, lineterminator="\n")
        writer.writeheader()

        for row_number, row in enumerate(reader, start=2):
            rows_total += 1
            ts = parse_aware_timestamp(row.get("timestamp", ""), source=key, row_number=row_number)
            year_counts[ts.year] += 1
            if not START_YEAR <= ts.year <= END_YEAR:
                excluded_year_counts[ts.year] += 1
                continue

            if key == "historical_outcome":
                maturity = ts.astimezone(timezone.utc) + timedelta(hours=OUTCOME_MAX_HORIZON_HOURS)
                if maturity >= OOS_START:
                    excluded_oos_maturity += 1
                    continue

            writer.writerow(row)
            rows_kept += 1
            first_timestamp = first_timestamp or ts.isoformat()
            last_timestamp = ts.isoformat()

    if rows_kept == 0:
        raise ValueError(f"NO_GOVERNED_DEVELOPMENT_ROWS:{key}")

    return {
        "source_key": key,
        "source_path": str(source_path),
        "source_sha256": sha256_file(source_path),
        "source_size_bytes": source_path.stat().st_size,
        "output_path": str(output_path),
        "output_sha256": sha256_file(output_path),
        "output_size_bytes": output_path.stat().st_size,
        "rows_total": rows_total,
        "rows_kept_2016_2024": rows_kept,
        "year_counts_source": {str(y): year_counts[y] for y in sorted(year_counts)},
        "excluded_outside_development_year_counts": {
            str(y): excluded_year_counts[y] for y in sorted(excluded_year_counts)
        },
        "excluded_outcome_rows_not_mature_before_2025": excluded_oos_maturity,
        "first_kept_timestamp": first_timestamp,
        "last_kept_timestamp": last_timestamp,
        "source_rows_modified": False,
        "source_timestamps_rewritten": False,
        "2025_or_later_rows_in_output": False,
        "outcome_horizon_guard_hours": OUTCOME_MAX_HORIZON_HOURS if key == "historical_outcome" else None,
        "2025_oos_used": False,
    }


def project_all(inputs: dict[str, Path], output_dir: Path, report_path: Path) -> dict[str, Any]:
    expected = set(REQUIRED_COLUMNS)
    if set(inputs) != expected:
        raise ValueError(f"PROJECTION_INPUT_KEYS_MISMATCH:expected={sorted(expected)}:got={sorted(inputs)}")
    reports = {}
    for key in ("market_state", "historical_context", "historical_outcome"):
        reports[key] = project_source(key, inputs[key], output_dir / f"{key}_2016_2024_GOVERNED.csv")
    report = {
        "status": "PASS_GOVERNED_SCOPE_PROJECTION_ONLY",
        "development_window": {"start_year": START_YEAR, "end_year": END_YEAR},
        "oos_policy": "2025_LOCKED_NOT_USED",
        "projections": reports,
        "source_files_modified": False,
        "full_backtest_authorized": False,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for key in REQUIRED_COLUMNS:
        parser.add_argument(f"--{key.replace('_', '-')}", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    report = project_all(
        {key: getattr(args, key) for key in REQUIRED_COLUMNS},
        args.output_dir,
        args.report,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
