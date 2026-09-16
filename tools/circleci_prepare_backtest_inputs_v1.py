from __future__ import annotations

import csv
import json
import os
import re
import shutil
import urllib.request
import zipfile
from pathlib import Path

TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("DROPBOX_ACCESS_TOKEN is required")

ROOT = Path("artifacts")
(ROOT / "nison").mkdir(parents=True, exist_ok=True)
(ROOT / "murphy").mkdir(parents=True, exist_ok=True)
(ROOT / "source" / "unpacked").mkdir(parents=True, exist_ok=True)

EXPECTED_MURPHY_IDS = {f"MURPHY_{n:04d}" for n in (3, 4, 6, 7, 18, 19, 21, 22, 23, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51)}
SUPPORTED_TEXT_SUFFIXES = {".csv", ".json", ".jsonl", ".txt", ".md", ".sql", ".yaml", ".yml"}


def download(dropbox_path: str, output: Path) -> None:
    request = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        data=b"",
        method="POST",
        headers={"Authorization": f"Bearer {TOKEN}", "Dropbox-API-Arg": json.dumps({"path": dropbox_path})},
    )
    with urllib.request.urlopen(request, timeout=900) as response, output.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def _ids(text: str) -> set[str]:
    return {x.upper() for x in re.findall(r"\bMURPHY[_ -]?\d{4}\b", text, re.IGNORECASE)}


def _normalize_ids(ids: set[str]) -> set[str]:
    normalized: set[str] = set()
    for value in ids:
        match = re.search(r"(\d{4})$", value)
        if match:
            normalized.add(f"MURPHY_{match.group(1)}")
    return normalized


def extract_records(path: Path) -> list[dict[str, str]]:
    try:
        raw = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return []

    # Some authoritative nested evidence packs identify the Murphy rule only in
    # the filename/directory name. Include the path as governed provenance rather
    # than requiring the ID to be repeated inside the payload.
    path_ids = _normalize_ids(_ids(str(path)))
    records: list[dict[str, str]] = []
    if path.suffix.lower() == ".csv":
        try:
            reader = csv.DictReader(raw.splitlines())
            for row in reader:
                text = " | ".join(f"{k}: {v}" for k, v in row.items() if v not in (None, ""))
                row_ids = _normalize_ids(_ids(text)) | path_ids
                for rid in sorted(row_ids):
                    records.append({"rule_id": rid, "source_file": str(path), "evidence_text": text})
        except (csv.Error, UnicodeError):
            pass
        return records

    if path.suffix.lower() in SUPPORTED_TEXT_SUFFIXES:
        content_ids = _normalize_ids(_ids(raw))
        all_ids = content_ids | path_ids
        evidence_text = f"source_path: {path}\n\n{raw}"
        for rid in sorted(all_ids):
            records.append({"rule_id": rid, "source_file": str(path), "evidence_text": evidence_text})
    return records


def merge_murphy_evidence(directory: Path, output: Path) -> tuple[Path, set[str]]:
    merged: dict[str, dict[str, str]] = {}
    diagnostics: list[dict[str, object]] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.resolve() == output.resolve() or path.suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
            continue
        records = extract_records(path)
        diagnostics.append({"file": str(path), "records": len(records), "ids": sorted({r["rule_id"] for r in records})})
        for record in records:
            merged.setdefault(record["rule_id"], record)
    ids = set(merged)
    (directory / "murphy_extraction_diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
    missing = sorted(EXPECTED_MURPHY_IDS - ids)
    unknown = sorted(ids - EXPECTED_MURPHY_IDS)
    if missing or unknown:
        raise SystemExit(
            f"Murphy evidence incomplete after recursive text extraction: found {len(ids)}/{len(EXPECTED_MURPHY_IDS)}; "
            f"missing: {', '.join(missing) or 'none'}; unknown: {', '.join(unknown) or 'none'}"
        )
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["rule_id", "source_file", "evidence_text"])
        writer.writeheader()
        writer.writerows(merged[rid] for rid in sorted(merged))
    return output, ids


download("/New 8/NISON_2016_2024_FULL_EVIDENCE.csv", ROOT / "nison" / "NISON_2016_2024_FULL_EVIDENCE.csv")
download("/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip", Path("/tmp/murphy.zip"))
download("/New 8/GBPUSD_H1_2016_2025_MASTER.zip", ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip")
download("/New 8/GBPUSD_MARKET_STATE 6.csv", ROOT / "GBPUSD_MARKET_STATE.csv")

with zipfile.ZipFile("/tmp/murphy.zip") as archive:
    archive.extractall(ROOT / "murphy")
merge_murphy_evidence(ROOT / "murphy", ROOT / "murphy" / "MURPHY_DROPBOX_FULL_EVIDENCE.csv")
print("Prepared complete Dropbox Murphy evidence; embedded legacy GitHub base64 artifact is intentionally not consumed.")

with zipfile.ZipFile(ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip") as archive:
    archive.extractall(ROOT / "source" / "unpacked")
source_csvs = sorted((ROOT / "source" / "unpacked").rglob("*.csv"))
if not source_csvs:
    raise SystemExit("No source CSV found in GBPUSD master archive")
Path("/tmp/source_csv_path").write_text(str(source_csvs[0]), encoding="utf-8")
print(f"Prepared source: {source_csvs[0]}")
