from __future__ import annotations

import base64
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

EXPECTED_MURPHY_IDS = {
    f"MURPHY_{n:04d}"
    for n in (3, 4, 6, 7, 18, 19, 21, 22, 23, 25, 26, 28, 29, 30, 31, 32,
              33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48,
              49, 50, 51)
}


def download(dropbox_path: str, output: Path) -> None:
    request = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        data=b"",
        method="POST",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Dropbox-API-Arg": json.dumps({"path": dropbox_path}),
        },
    )
    with urllib.request.urlopen(request, timeout=900) as response, output.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def rule_field(fields: list[str]) -> str | None:
    normalized = {f.strip().lower(): f for f in fields}
    for name in ("rule_id", "ruleid", "id", "evidence_id"):
        if name in normalized:
            return normalized[name]
    return None


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]], set[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        field = rule_field(fields)
        if field is None:
            return fields, [], set()
        rows = []
        ids = set()
        for row in reader:
            value = str(row.get(field, "")).strip()
            if value:
                row["rule_id"] = value
                ids.add(value)
                rows.append(row)
        return fields, rows, ids


def merge_murphy_csvs(directory: Path, output: Path) -> tuple[Path, set[str]]:
    candidates = sorted(
        p for p in directory.rglob("*.csv")
        if p.resolve() != output.resolve()
    )
    merged: dict[str, dict[str, str]] = {}
    fieldnames: list[str] = ["rule_id"]
    for path in candidates:
        fields, rows, _ = read_csv(path)
        if not rows:
            continue
        for field in fields:
            if field not in fieldnames and field != "rule_id":
                fieldnames.append(field)
        for row in rows:
            rid = row["rule_id"]
            merged.setdefault(rid, row)
    ids = set(merged)
    if not EXPECTED_MURPHY_IDS.issubset(ids):
        missing = sorted(EXPECTED_MURPHY_IDS - ids)
        raise SystemExit(
            f"Murphy evidence incomplete: found {len(ids)}/{len(EXPECTED_MURPHY_IDS)} rule IDs; "
            f"missing: {', '.join(missing)}"
        )
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged[rid] for rid in sorted(merged))
    return output, ids


download("/New 8/NISON_2016_2024_FULL_EVIDENCE.csv", ROOT / "nison" / "NISON_2016_2024_FULL_EVIDENCE.csv")
download("/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip", Path("/tmp/murphy.zip"))
download("/New 8/GBPUSD_H1_2016_2025_MASTER.zip", ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip")
download("/New 8/GBPUSD_MARKET_STATE 6.csv", ROOT / "GBPUSD_MARKET_STATE.csv")

with zipfile.ZipFile("/tmp/murphy.zip") as archive:
    archive.extractall(ROOT / "murphy")
merge_murphy_csvs(ROOT / "murphy", ROOT / "murphy" / "MURPHY_DROPBOX_FULL_EVIDENCE.csv")
print("Prepared complete Dropbox Murphy evidence")

encoded = Path("BACKTEST/DEV_BACKTEST_R1_MURPHY_SOURCE.zip.b64.txt").read_text(encoding="utf-8")
encoded = "".join(encoded.split())
if len(encoded) % 4 == 1:
    raise SystemExit("Embedded GitHub Murphy artifact is truncated: invalid base64 length")
embedded_zip = Path("/tmp/murphy_embedded.zip")
embedded_zip.write_bytes(base64.b64decode(encoded, validate=True))
with zipfile.ZipFile(embedded_zip) as archive:
    archive.extractall(Path("/tmp/murphy_embedded"))
merge_murphy_csvs(Path("/tmp/murphy_embedded"), ROOT / "murphy" / "MURPHY_GITHUB_FULL_EVIDENCE.csv")
print("Prepared complete embedded GitHub Murphy evidence")

with zipfile.ZipFile(ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip") as archive:
    archive.extractall(ROOT / "source" / "unpacked")
source_csv = sorted((ROOT / "source" / "unpacked").rglob("*.csv"))[0]
Path("/tmp/source_csv_path").write_text(str(source_csv), encoding="utf-8")
print(f"Prepared source: {source_csv}")
