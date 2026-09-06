from __future__ import annotations

import base64
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


def csv_rule_ids(path: Path) -> set[str]:
    import csv
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        field = next((f for f in fields if f.lower() in {"rule_id", "ruleid", "id"}), None)
        if field is None:
            return set()
        return {str(row.get(field, "")).strip() for row in reader if str(row.get(field, "")).strip()}


def select_murphy_csv(directory: Path, minimum: int = 34) -> Path:
    candidates = sorted(directory.rglob("*.csv"))
    scored = sorted(((len(csv_rule_ids(path)), path) for path in candidates), reverse=True)
    if not scored or scored[0][0] < minimum:
        summary = ", ".join(f"{count}:{path.name}" for count, path in scored[:10]) or "none"
        raise SystemExit(f"No complete Murphy evidence CSV found; need at least {minimum} rule IDs. Candidates: {summary}")
    return scored[0][1]


download("/New 8/NISON_2016_2024_FULL_EVIDENCE.csv", ROOT / "nison" / "NISON_2016_2024_FULL_EVIDENCE.csv")
download("/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip", Path("/tmp/murphy.zip"))
download("/New 8/GBPUSD_H1_2016_2025_MASTER.zip", ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip")
download("/New 8/GBPUSD_MARKET_STATE 6.csv", ROOT / "GBPUSD_MARKET_STATE.csv")

with zipfile.ZipFile("/tmp/murphy.zip") as archive:
    archive.extractall(ROOT / "murphy")
dropbox_csv = select_murphy_csv(ROOT / "murphy")
shutil.copy2(dropbox_csv, ROOT / "murphy" / "MURPHY_DROPBOX_FULL_EVIDENCE.csv")
print(f"Selected complete Dropbox Murphy evidence: {dropbox_csv}")

# The committed embedded artifact must be independent and complete. Never substitute
# Dropbox data for the GitHub-side source, because that would make reconciliation meaningless.
encoded = Path("BACKTEST/DEV_BACKTEST_R1_MURPHY_SOURCE.zip.b64.txt").read_text(encoding="utf-8")
encoded = "".join(encoded.split())
if len(encoded) % 4 == 1:
    raise SystemExit("Embedded GitHub Murphy artifact is truncated: invalid base64 length")
embedded_bytes = base64.b64decode(encoded, validate=True)
embedded_zip = Path("/tmp/murphy_embedded.zip")
embedded_zip.write_bytes(embedded_bytes)
with zipfile.ZipFile(embedded_zip) as archive:
    archive.extractall(Path("/tmp/murphy_embedded"))
github_csv = select_murphy_csv(Path("/tmp/murphy_embedded"))
shutil.copy2(github_csv, ROOT / "murphy" / "MURPHY_GITHUB_FULL_EVIDENCE.csv")
print(f"Selected complete embedded GitHub Murphy evidence: {github_csv}")

with zipfile.ZipFile(ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip") as archive:
    archive.extractall(ROOT / "source" / "unpacked")
source_csv = sorted((ROOT / "source" / "unpacked").rglob("*.csv"))[0]
Path("/tmp/source_csv_path").write_text(str(source_csv), encoding="utf-8")
print(f"Prepared source: {source_csv}")
