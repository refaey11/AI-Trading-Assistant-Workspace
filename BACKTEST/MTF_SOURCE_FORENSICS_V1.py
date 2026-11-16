from __future__ import annotations

"""Read-only forensic profile of the recovered GBPUSD MTF archive.

This tool inspects only 2016-2024 annual data files. It does not recode,
impute, scale, normalize, or modify source rows. 2025/2026 files are ignored.
"""

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

FILE_PATTERN = "GBPUSD_M5_MTF_ALIGNMENT_{year}.csv"
YEARS = tuple(range(2016, 2025))
BRAIN_FIELDS = (
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
)
AGGREGATE_FIELDS = (
    "mtf_bullish_count",
    "mtf_bearish_count",
    "mtf_neutral_count",
    "mtf_context",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_blank(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def _timestamp_mode(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return "invalid"
    return "aware" if parsed.tzinfo is not None and parsed.utcoffset() is not None else "naive"


def _find_one(root: Path, name: str) -> Path | None:
    matches = list(root.rglob(name))
    return matches[0] if len(matches) == 1 else None


def inspect_year(path: Path, year: int) -> dict[str, Any]:
    field_counts = {name: {"blank": 0, "nonblank": 0, "values": Counter()} for name in (*BRAIN_FIELDS, *AGGREGATE_FIELDS)}
    timestamp_counts = Counter()
    missing_samples: list[dict[str, Any]] = []
    first_rows: list[dict[str, Any]] = []
    row_count = 0
    first_timestamp = None
    last_timestamp = None
    header: list[str] | None = None

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = list(reader.fieldnames or [])
        for row_number, row in enumerate(reader, start=2):
            row_count += 1
            timestamp = (row.get("timestamp") or "").strip()
            if first_timestamp is None:
                first_timestamp = timestamp
            last_timestamp = timestamp
            timestamp_counts[_timestamp_mode(timestamp)] += 1

            for name, stats in field_counts.items():
                value = row.get(name)
                if _is_blank(value):
                    stats["blank"] += 1
                else:
                    stats["nonblank"] += 1
                    token = str(value).strip()
                    stats["values"][token] += 1

            missing = [name for name in BRAIN_FIELDS if _is_blank(row.get(name))]
            if missing and len(missing_samples) < 5:
                missing_samples.append({
                    "row_number": row_number,
                    "timestamp": timestamp,
                    "missing_fields": missing,
                    "observed_brain_fields": {name: row.get(name) for name in BRAIN_FIELDS},
                })
            if len(first_rows) < 3:
                first_rows.append({
                    "row_number": row_number,
                    "timestamp": timestamp,
                    "brain_fields": {name: row.get(name) for name in BRAIN_FIELDS},
                })

    fields_report = {}
    for name, stats in field_counts.items():
        fields_report[name] = {
            "blank": stats["blank"],
            "nonblank": stats["nonblank"],
            "distinct_nonblank_values": len(stats["values"]),
            "top_values": [{"value": key, "count": count} for key, count in stats["values"].most_common(30)],
        }

    return {
        "year": year,
        "file": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "row_count": row_count,
        "column_count": len(header or []),
        "header": header,
        "header_sha256": hashlib.sha256(",".join(header or []).encode()).hexdigest(),
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "timestamp_modes": dict(timestamp_counts),
        "brain_and_aggregate_field_profile": fields_report,
        "first_rows_brain_fields": first_rows,
        "first_rows_with_missing_brain_fields": missing_samples,
    }


def run_forensics(source_root: Path, output_path: Path) -> dict[str, Any]:
    files = []
    missing_years = []
    for year in YEARS:
        path = source_root / FILE_PATTERN.format(year=year)
        if not path.is_file():
            matches = list(source_root.rglob(path.name))
            if len(matches) != 1:
                missing_years.append(year)
                continue
            path = matches[0]
        files.append(inspect_year(path, year))

    readme_path = _find_one(source_root, "README.json")
    manifest_path = _find_one(source_root, "FINAL_MANIFEST.csv")
    readme: Any = None
    readme_error = None
    if readme_path:
        try:
            readme = json.loads(readme_path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            readme_error = type(exc).__name__
    manifest_rows = []
    if manifest_path:
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                year_text = row.get("year") or row.get("Year") or ""
                try:
                    year = int(year_text)
                except ValueError:
                    continue
                if year in YEARS:
                    manifest_rows.append(row)

    headers = {item["header_sha256"] for item in files}
    report = {
        "status": "PASS_FORENSICS_ONLY" if not missing_years and len(headers) <= 1 else "BLOCKED_FORENSICS",
        "scope": "READ_ONLY_SOURCE_FORENSICS",
        "development_years_inspected": list(YEARS),
        "oos_policy": {"2025": "LOCKED_NOT_READ", "2026": "NOT_READ"},
        "missing_development_years": missing_years,
        "annual_file_count": len(files),
        "common_header_across_development_years": len(headers) == 1,
        "expected_brain_fields": list(BRAIN_FIELDS),
        "source_readme": readme,
        "source_readme_parse_error": readme_error,
        "source_manifest_2016_2024_rows": manifest_rows,
        "producer_code_files_found": [
            str(p.relative_to(source_root))
            for p in source_root.rglob("*")
            if p.is_file() and p.suffix.lower() in {".py", ".ipynb", ".sql"}
        ],
        "annual_files": files,
        "transformations_applied": {
            "timestamp_conversion": False,
            "categorical_recoding": False,
            "imputation": False,
            "scaling": False,
            "source_mutation": False,
        },
        "interpretation": (
            "This report profiles serialized source values only. It does not establish "
            "producer formulas, timezone semantics, or permission to adapt missing values."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = run_forensics(args.source_root, args.output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS_FORENSICS_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
