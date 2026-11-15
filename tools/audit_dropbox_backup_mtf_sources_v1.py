from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TEXT_SUFFIXES = {".py", ".ipynb", ".m", ".js", ".ts", ".tsx", ".jsx", ".sh", ".ps1", ".bat", ".json", ".md", ".yml", ".yaml", ".txt", ".toml", ".sql", ".xml"}
CODE_SUFFIXES = {".py", ".ipynb", ".m", ".js", ".ts", ".tsx", ".jsx", ".sh", ".ps1", ".bat", ".sql"}
TERMS = (
    "resample", "resampling", "m1_to_m5", "m1_to_mtf", "timeframe_converter",
    "mtf_trend_score", "trend_regime", "market_structure", "pivot_high", "pivot_low",
    "break_structure", "bos", "choch", "ohlcv", "bar_complete", "m1_count",
)
MAX_TEXT_BYTES = 5 * 1024 * 1024


def audit(root: Path) -> dict:
    files = []
    code_files = []
    candidates = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(root))
        size = path.stat().st_size
        suffix = path.suffix.lower()
        files.append({"path": rel, "size": size, "suffix": suffix})
        if suffix not in TEXT_SUFFIXES or size > MAX_TEXT_BYTES:
            continue
        try:
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        except Exception:
            continue
        if suffix in CODE_SUFFIXES:
            code_files.append({"path": rel, "size": size})
        hits = []
        for line_no, line in enumerate(content.splitlines(), 1):
            matched = [term for term in TERMS if re.search(r"(?<![A-Za-z0-9_])" + re.escape(term) + r"(?![A-Za-z0-9_])", line, re.I)]
            if matched:
                hits.append({"line": line_no, "terms": matched, "text": line[:600]})
                if len(hits) >= 100:
                    break
        name_hit = any(term in rel.lower() for term in ("mtf", "market_structure", "resampl", "timeframe", "ohlcv", "trend_regime"))
        if hits or name_hit:
            candidates.append({"path": rel, "size": size, "suffix": suffix, "hits": hits})
    return {
        "audit": "DROPBOX_BACKUP_MTF_PRODUCER_SOURCE_SCAN_V1",
        "status": "COMPLETED_READ_ONLY",
        "file_count": len(files),
        "code_file_count": len(code_files),
        "code_files": code_files[:2000],
        "candidate_count": len(candidates),
        "candidates": candidates[:1500],
        "interpretation": [
            "Code and document matches are recovery leads, not proof of output lineage.",
            "No market data values were used for tuning or calibration.",
            "2025 remains excluded from tuning/calibration.",
            "No source files or project runtime modules were modified."
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = audit(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "file_count": result["file_count"],
        "code_file_count": result["code_file_count"],
        "code_files": result["code_files"],
        "candidate_count": result["candidate_count"],
        "candidate_paths": [x["path"] for x in result["candidates"]],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
