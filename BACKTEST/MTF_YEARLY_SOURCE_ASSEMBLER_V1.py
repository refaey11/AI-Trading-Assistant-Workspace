from __future__ import annotations

"""Assemble the governed 2016-2024 MTF input from annual source CSVs.

The assembler is read-only with respect to source files. It copies rows without
recoding, imputing, scaling, or synthesizing any MTF field. 2025 and 2026 files
are explicitly excluded from the development artifact.
"""

import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

START_YEAR = 2016
END_YEAR = 2024
REQUIRED_FIELDS = (
    "timestamp",
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
)
FILENAME_RE = re.compile(r"^GBPUSD_M5_MTF_ALIGNMENT_(\\d{4})\\.csv$")


def parse_aware_timestamp(raw: str, *, path: Path, row_number: int) -> datetime:
    value = (raw or "").strip()
    candidate = value[:-1] + "+00:00" if value.endswith(("Z", "z")) else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ValueError(f"MTF_INVALID_TIMESTAMP:{path.name}:row={row_number}:{value[:80]}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"MTF_NAIVE_TIMESTAMP:{path.name}:row={row_number}")
    return parsed.astimezone(timezone.utc)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assemble_yearly_mtf(source_root: Path, output_path: Path, report_path: Path | None = None) -> dict[str, Any]:
    expected_years = list(range(START_YEAR, END_YEAR + 1))
    matches: dict[int, list[Path]] = {year: [] for year in expected_years}
    excluded_oos: list[dict[str, Any]] = []
    unexpected: list[str] = []

    for path in source_root.rglob("*.csv"):
        match = FILENAME_RE.fullmatch(path.name)
        if not match:
            continue
        year = int(match.group(1))
        if year in matches:
            matches[year].append(path)
        elif year in (2025, 2026):
            excluded_oos.append({"year": year, "path": str(path.relative_to(source_root)), "size_bytes": path.stat().st_size})
        else:
            unexpected.append(str(path.relative_to(source_root)))

    missing = [year for year, paths in matches.items() if not paths]
    duplicated = {year: [str(p.relative_to(source_root)) for p in paths] for year, paths in matches.items() if len(paths) > 1}
    if missing or duplicated or unexpected:
        raise ValueError(f"MTF_YEAR_FILE_SET_INVALID:missing={missing}:duplicates={duplicated}:unexpected={unexpected}")

    ordered_paths = [matches[year][0] for year in expected_years]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    total_rows = 0
    previous_timestamp: datetime | None = None
    seen_timestamps: set[datetime] = set()
    canonical_header: list[str] | None = None
    year_reports: list[dict[str, Any]] = []

    with output_path.open("w", encoding="utf-8", newline="") as output_handle:
        writer: csv.writer | None = None
        for year, source_path in zip(expected_years, ordered_paths):
            year_rows = 0
            first_timestamp: str | None = None
            last_timestamp: str | None = None
            with source_path.open("r", encoding="utf-8-sig", newline="") as source_handle:
                reader = csv.reader(source_handle)
                header = next(reader, None)
                if not header:
                    raise ValueError(f"MTF_EMPTY_OR_HEADERLESS_FILE:{source_path.name}")
                if len(header) != len(set(header)):
                    raise ValueError(f"MTF_DUPLICATE_COLUMN_NAMES:{source_path.name}")
                missing_fields = sorted(set(REQUIRED_FIELDS) - set(header))
                if missing_fields:
                    raise ValueError(f"MTF_REQUIRED_FIELDS_MISSING:{source_path.name}:{missing_fields}")
                if canonical_header is None:
                    canonical_header = header
                    writer = csv.writer(output_handle, lineterminator="\\n")
                    writer.writerow(canonical_header)
                elif header != canonical_header:
                    raise ValueError(f"MTF_HEADER_MISMATCH:{source_path.name}")
                assert writer is not None

                for row_number, row in enumerate(reader, start=2):
                    if len(row) != len(header):
                        raise ValueError(f"MTF_ROW_WIDTH_MISMATCH:{source_path.name}:row={row_number}")
                    record = dict(zip(header, row))
                    timestamp = parse_aware_timestamp(record.get("timestamp", ""), path=source_path, row_number=row_number)
                    if timestamp.year != year:
                        raise ValueError(f"MTF_YEAR_CONTENT_MISMATCH:{source_path.name}:row={row_number}:timestamp_year={timestamp.year}")
                    if previous_timestamp is not None and timestamp <= previous_timestamp:
                        reason = "DUPLICATE" if timestamp == previous_timestamp or timestamp in seen_timestamps else "OUT_OF_ORDER"
                        raise ValueError(f"MTF_{reason}_TIMESTAMP:{source_path.name}:row={row_number}:{timestamp.isoformat()}")
                    if timestamp in seen_timestamps:
                        raise ValueError(f"MTF_DUPLICATE_TIMESTAMP:{source_path.name}:row={row_number}:{timestamp.isoformat()}")
                    seen_timestamps.add(timestamp)
                    previous_timestamp = timestamp
                    writer.writerow(row)
                    year_rows += 1
                    total_rows += 1
                    if first_timestamp is None:
                        first_timestamp = timestamp.isoformat()
                    last_timestamp = timestamp.isoformat()

            if year_rows == 0:
                raise ValueError(f"MTF_YEAR_FILE_HAS_NO_DATA_ROWS:{source_path.name}")
            year_reports.append({
                "year": year,
                "source": str(source_path.relative_to(source_root)),
                "source_size_bytes": source_path.stat().st_size,
                "source_sha256": sha256_file(source_path),
                "rows": year_rows,
                "first_timestamp": first_timestamp,
                "last_timestamp": last_timestamp,
            })

    report = {
        "status": "PASS_MTF_YEARLY_ASSEMBLY_ONLY",
        "development_years": expected_years,
        "rows": total_rows,
        "output_path": str(output_path),
        "output_size_bytes": output_path.stat().st_size,
        "output_sha256": sha256_file(output_path),
        "source_years": year_reports,
        "excluded_oos_files": sorted(excluded_oos, key=lambda item: item["year"]),
        "source_rows_rewritten_or_transformed": False,
        "categorical_translation_applied": False,
        "imputation_applied": False,
        "scaling_applied": False,
        "2025_oos_used": False,
        "2026_used": False,
    }
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    report = assemble_yearly_mtf(args.source_root, args.output, args.report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
