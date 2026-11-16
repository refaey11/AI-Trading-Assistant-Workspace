from __future__ import annotations

"""Search a ZIP archive for MTF producer source without reading market data files."""

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any

TEXT_SUFFIXES = {".py", ".ipynb", ".sql", ".md", ".json", ".yml", ".yaml", ".txt", ".r", ".js", ".ts"}
CODE_SUFFIXES = {".py", ".ipynb", ".sql", ".r", ".js", ".ts"}
SOURCE_TERMS = (
    "mtf_trend_score", "m5_trend_regime", "trend_regime",
    "merge_asof", "resample(", "resample_", "closed_bar",
    "candle_close", "timeframe_alignment", "higher_tf",
)
SEARCH_TERMS = (
    "mtf", "multi-timeframe", "multi_timeframe", "timeframe",
    "alignment", "trend_regime", "mtf_trend_score",
    "merge_asof", "resample", "ffill", "shift",
)
MAX_TEXT_BYTES = 2 * 1024 * 1024


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_excerpt(line: str) -> str:
    if re.search(r"(token|password|secret|api[_-]?key)\s*[:=]", line, re.I):
        return "[REDACTED_SENSITIVE_ASSIGNMENT]"
    return line.strip()[:180]


def search_archive(archive_path: Path, output_path: Path) -> dict[str, Any]:
    entries = []
    candidates = []
    unread_text_candidates = []
    with zipfile.ZipFile(archive_path) as archive:
        infos = [info for info in archive.infolist() if not info.is_dir()]
        for info in infos:
            path = info.filename
            lower = path.lower()
            suffix = Path(path).suffix.lower()
            if any(term in lower for term in ("mtf", "timeframe", "alignment")):
                entries.append({"path": path, "size_bytes": info.file_size, "suffix": suffix})
            if suffix not in TEXT_SUFFIXES:
                continue
            if suffix not in CODE_SUFFIXES and not any(term in lower for term in ("mtf", "timeframe", "alignment")):
                continue
            if info.file_size > MAX_TEXT_BYTES:
                unread_text_candidates.append({"path": path, "size_bytes": info.file_size, "reason": "TEXT_FILE_OVER_SIZE_LIMIT"})
                continue
            try:
                raw = archive.read(info)
                text = raw.decode("utf-8-sig", errors="replace")
            except Exception as exc:
                unread_text_candidates.append({"path": path, "size_bytes": info.file_size, "reason": type(exc).__name__})
                continue
            lowered = text.lower()
            matched = [term for term in SEARCH_TERMS if term in lowered]
            if not matched:
                continue
            lines = text.splitlines()
            excerpts = []
            for line_number, line in enumerate(lines, start=1):
                low_line = line.lower()
                if any(term in low_line for term in SOURCE_TERMS):
                    excerpts.append({"line": line_number, "text": _safe_excerpt(line)})
                    if len(excerpts) >= 40:
                        break
            source_hits = [term for term in SOURCE_TERMS if term in lowered]
            candidates.append({
                "path": path,
                "suffix": suffix,
                "size_bytes": info.file_size,
                "sha256": sha256_bytes(raw),
                "matched_search_terms": matched,
                "matched_source_terms": source_hits,
                "producer_candidate": suffix in CODE_SUFFIXES and len(source_hits) >= 2,
                "matching_line_excerpts": excerpts,
            })

    candidates.sort(key=lambda item: (item["producer_candidate"], len(item["matched_source_terms"]), len(item["matched_search_terms"])), reverse=True)
    report = {
        "status": "PASS_ARCHIVE_SEARCH_ONLY",
        "scope": "SOURCE_CODE_AND_DOCUMENT_SEARCH_ONLY",
        "archive": archive_path.name,
        "archive_size_bytes": archive_path.stat().st_size,
        "archive_sha256": sha256_file(archive_path),
        "zip_entry_count": len(infos),
        "mtf_timeframe_alignment_named_entries": entries,
        "producer_candidates": [item for item in candidates if item["producer_candidate"]],
        "other_relevant_text_files": [item for item in candidates if not item["producer_candidate"]],
        "unread_text_candidates": unread_text_candidates,
        "data_policy": {
            "csv_parquet_hdf5_feather_xlsx_data_files_read": False,
            "market_rows_read": False,
            "2025_data_read_or_used": False,
            "source_archive_modified": False,
        },
        "interpretation": (
            "A candidate is only a source-search lead. Producer authority still requires "
            "formula, schema, timestamp, missing-value, and lineage compatibility review."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = search_archive(args.archive, args.output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
