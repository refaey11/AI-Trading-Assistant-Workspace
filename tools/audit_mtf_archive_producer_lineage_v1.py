from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
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
    members: list[dict[str, Any]] = []
    matches: list[dict[str, Any]] = []
    candidate_count = 0
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename
            lower = name.lower()
            suffix = Path(name).suffix.lower()
            name_hits = [term for term in NAME_TERMS if term in lower]
            item = {
                "path": name,
                "size": info.file_size,
                "compressed_size": info.compress_size,
                "crc32": f"{info.CRC:08x}",
                "name_hits": name_hits,
            }
            if name_hits:
                members.append(item)
            if suffix not in TEXT_SUFFIXES or info.file_size > MAX_TEXT_BYTES:
                continue
            candidate_count += 1
            try:
                raw = zf.read(info)
                text = raw.decode("utf-8-sig")
            except (UnicodeDecodeError, RuntimeError, zipfile.BadZipFile):
                continue
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
        "member_count": len(zipfile.ZipFile(path).infolist()),
        "text_files_scanned": candidate_count,
        "name_candidates": members[:500],
        "source_candidates": matches[:500],
        "candidate_truncated": len(matches) > 500 or len(members) > 500,
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
        "scope": "Archive inventory and source-text keyword scan only; no runtime or market data changes.",
        "archives": reports,
        "interpretation": [
            "A matching filename or keyword is a lead, not proof that the file generated the released dataset.",
            "Producer lineage requires identifying code, inputs, parameters, and a reproducible output match.",
            "This audit does not infer trend-regime encodings or mtf_trend_score formulas.",
            "2025 is not used for tuning, calibration, or validation.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
