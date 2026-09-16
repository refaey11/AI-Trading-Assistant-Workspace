from __future__ import annotations

import csv
import json
import os
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


def download(dropbox_path: str, output: Path) -> None:
    request = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        data=b"",
        method="POST",
        headers={"Authorization": f"Bearer {TOKEN}", "Dropbox-API-Arg": json.dumps({"path": dropbox_path})},
    )
    with urllib.request.urlopen(request, timeout=900) as response, output.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def extract_records(path: Path) -> list[dict[str, str]]:
    try:
        raw = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return []
    records: list[dict[str, str]] = []
    if path.suffix.lower() == ".csv":
        try:
            reader = csv.DictReader(raw.splitlines())
            for row in reader:
                text = " | ".join(f"{k}: {v}" for k, v in row.items() if v not in (None, ""))
                ids = {x.upper() for x in __import__("re").findall(r"\bMURPHY_\d{4}\b", text, __import__("re").IGNORECASE)}
                for rid in ids:
                    records.append({"rule_id": rid, "source_file": str(path), "evidence_text": text})
        except (csv.Error, UnicodeError):
            pass
    return records


def merge_murphy_evidence(directory: Path, output: Path) -> tuple[Path, set[str]]:
    merged: dict[str, dict[str, str]] = {}
    diagnostics: list[dict[str, object]] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.resolve() == output.resolve() or path.suffix.lower() not in {".csv", ".json", ".jsonl", ".txt", ".md", ".sql", ".yaml", ".yml"}:
            continue
        records = extract_records(path)
        diagnostics.append({"file": str(path), "records": len(records), "ids": sorted({r["rule_id"] for r in records})})
        for record in records:
            merged.setdefault(record["rule_id"], record)
    ids = set(merged)
    (directory / "murphy_extraction_diagnostics.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
    missing = sorted(EXPECTED_MURPHY_IDS - ids)
    if missing:
        raise SystemExit(f"Murphy evidence incomplete after recursive extraction: found {len(ids)}/{len(EXPECTED_MURPHY_IDS)}; missing: {', '.join(missing)}")
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
