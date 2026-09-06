from __future__ import annotations

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


download("/New 8/NISON_2016_2024_FULL_EVIDENCE.csv", ROOT / "nison" / "NISON_2016_2024_FULL_EVIDENCE.csv")
download("/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip", Path("/tmp/murphy.zip"))
download("/New 8/GBPUSD_H1_2016_2025_MASTER.zip", ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip")
download("/New 8/GBPUSD_MARKET_STATE 6.csv", ROOT / "GBPUSD_MARKET_STATE.csv")

with zipfile.ZipFile("/tmp/murphy.zip") as archive:
    archive.extractall(ROOT / "murphy")

murphy_csvs = sorted((ROOT / "murphy").rglob("*.csv"))
if not murphy_csvs:
    raise SystemExit("No Murphy CSV found in Dropbox archive")
shutil.copy2(murphy_csvs[0], ROOT / "murphy" / "MURPHY_DROPBOX_FULL_EVIDENCE.csv")

with zipfile.ZipFile(ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip") as archive:
    archive.extractall(ROOT / "source" / "unpacked")

source_csvs = sorted((ROOT / "source" / "unpacked").rglob("GBPUSD_H1_2016_2025_MASTER.csv"))
if not source_csvs:
    raise SystemExit("No GBPUSD H1 CSV found in source archive")
Path("/tmp/source_csv_path").write_text(str(source_csvs[0]), encoding="utf-8")
print(f"Prepared source: {source_csvs[0]}")
