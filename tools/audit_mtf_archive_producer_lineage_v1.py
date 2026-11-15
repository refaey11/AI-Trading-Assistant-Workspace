from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

TEXT_SUFFIXES = {".py", ".ipynb", ".md", ".json", ".yaml", ".yml", ".toml", ".ini", ".txt", ".sh", ".ps1", ".bat"}
NAME_TERMS = ("resampl", "timeframe", "market_structure", "mtf", "trend_regime", "trend_score", "ohlcv", "manifest", "readme", "schema", "converter")
CONTENT_TERMS = ("resample", "resampling", "mtf_trend_score", "trend_regime", "ohlcv", "closed bar", "available_at", "m1", "m5")
MAX_TEXT_BYTES = 2 * 1024 * 1024


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inspect_archive(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    all_members: list[dict[str, Any]] = []
    matches: list[dict[str, Any]] = []
    csv_schemas: list[dict[str, Any]] = []
    text_documents: list[dict[str, Any]] = []
    candidate_count = 0
    with zipfile.ZipFile(path) as zf:
        infos = [info for info in zf.infolist() if not info.is_dir()]
        for info in infos:
            name = info.filename
            lower = name.lower()
            suffix = Path(name).suffix.lower()
            name_hits = [term for term in NAME_TERMS if term in lower]
            all_members.append({
                "path": name,
                "size": info.file_size,
                "compressed_size": info.compress_size,
                "suffix": suffix,
                "name_hits": name_hits,
            })
            if suffix == ".csv":
                try:
                    with zf.open(info, "r") as raw:
                        sample = raw.read(256 * 1024).decode("utf-8-sig", errors="replace")
                    lines = sample.splitlines()
                    header = next(csv.reader(lines), [])
                    preview_rows = list(csv.DictReader(lines[:6]))[:5]
                    schema = {
                        "path": name,
                        "size": info.file_size,
                        "header": header[:250],
                        "preview_rows": preview_rows,
                        "header_hits": [term for term in CONTENT_TERMS if any(term in str(col).lower() for col in header)],
                    }
                    if Path(name).name == "GBPUSD_M1_MASTER_2016_2026.csv":
                        with zf.open(info, "r") as raw:
                            reader = csv.DictReader((line.decode("utf-8", errors="replace") for line in raw))
                            years = Counter()
                            periods = Counter()
                            volume_available = Counter()
                            row_count = 0
                            first_ts = None
                            last_ts = None
                            for row in reader:
                                ts = str(row.get("timestamp", "")).strip()
                                year = ts[:4] if len(ts) >= 4 else ""
                                if year in {str(y) for y in range(2016, 2025)}:
                                    row_count += 1
                                    years[year] += 1
                                    periods[str(row.get("source_period", ""))] += 1
                                    volume_available[str(row.get("volume_available", ""))] += 1
                                    if first_ts is None:
                                        first_ts = ts
                                    last_ts = ts
                            schema["development_window_2016_2024"] = {
                                "rows": row_count,
                                "rows_by_year": dict(sorted(years.items())),
                                "source_period_counts": dict(periods),
                                "volume_available_counts": dict(volume_available),
                                "first_timestamp": first_ts,
                                "last_timestamp": last_ts,
                                "note": "Counts restricted to 2016-2024; no 2025+ rows used in this audit summary.",
                            }
                    csv_schemas.append(schema)
                except Exception as exc:
                    csv_schemas.append({"path": name, "size": info.file_size, "error": type(exc).__name__})
            if suffix not in TEXT_SUFFIXES or info.file_size > MAX_TEXT_BYTES:
                continue
            candidate_count += 1
            try:
                text = zf.read(info).decode("utf-8-sig")
            except (UnicodeDecodeError, RuntimeError, zipfile.BadZipFile):
                continue
            text_documents.append({"path": name, "size": info.file_size, "content": text[:20000]})
            line_hits = []
            for line_no, line in enumerate(text.splitlines(), start=1):
                low = line.lower()
                terms = [term for term in CONTENT_TERMS if re.search(r"(?<![a-z0-9_])" + re.escape(term) + r"(?![a-z0-9_])", low)]
                if terms:
                    line_hits.append({"line": line_no, "terms": terms, "text": line[:500]})
                    if len(line_hits) >= 80:
                        break
            if name_hits or line_hits:
                matches.append({
                    "path": name,
                    "size": info.file_size,
                    "suffix": suffix,
                    "name_hits": name_hits,
                    "content_matches": line_hits,
                })
    return {
        "archive": path.name,
        "archive_size": path.stat().st_size,
        "archive_sha256": _sha256(path),
        "member_count": len(all_members),
        "text_files_scanned": candidate_count,
        "all_members": all_members[:1000],
        "text_documents": text_documents[:100],
        "csv_schemas": csv_schemas[:500],
        "source_candidates": matches[:500],
        "candidate_truncated": len(matches) > 500 or len(all_members) > 1000 or len(csv_schemas) > 500,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", action="append", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    reports = [inspect_archive(p) for p in args.archive]
    result = {
        "audit": "MTF_ARCHIVE_PRODUCER_LINEAGE_READ_ONLY_V1",
        "status": "COMPLETED_READ_ONLY",
        "scope": "Archive inventory, small text-document extraction, CSV schema/preview inspection, and 2016-2024 M1 master counts only; no runtime or market data changes.",
        "archives": reports,
        "interpretation": [
            "A matching filename or keyword is a lead, not proof that the file generated the released dataset.",
            "Producer lineage requires identifying code, inputs, parameters, and a reproducible output match.",
            "This audit does not infer trend-regime encodings or mtf_trend_score formulas.",
            "2025+ rows are excluded from the M1 summary and are not used for tuning or calibration.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
