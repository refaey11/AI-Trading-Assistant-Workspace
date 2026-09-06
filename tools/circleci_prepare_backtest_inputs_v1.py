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


def first_csv(directory: Path) -> Path:
    files = sorted(directory.rglob("*.csv"))
    if not files:
        raise SystemExit(f"No CSV found under {directory}")
    return files[0]


download("/New 8/NISON_2016_2024_FULL_EVIDENCE.csv", ROOT / "nison" / "NISON_2016_2024_FULL_EVIDENCE.csv")
download("/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip", Path("/tmp/murphy.zip"))
download("/New 8/GBPUSD_H1_2016_2025_MASTER.zip", ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip")
download("/New 8/GBPUSD_MARKET_STATE 6.csv", ROOT / "GBPUSD_MARKET_STATE.csv")

with zipfile.ZipFile("/tmp/murphy.zip") as archive:
    archive.extractall(ROOT / "murphy")
shutil.copy2(first_csv(ROOT / "murphy"), ROOT / "murphy" / "MURPHY_DROPBOX_FULL_EVIDENCE.csv")

embedded_zip = Path("/tmp/murphy_embedded.zip")
embedded_zip.write_bytes(base64.b64decode(Path("BACKTEST/DEV_BACKTEST_R1_MURPHY_SOURCE.zip.b64.txt").read_text(encoding="utf-8")))
with zipfile.ZipFile(embedded_zip) as archive:
    archive.extractall(Path("/tmp/murphy_embedded"))
shutil.copy2(first_csv(Path("/tmp/murphy_embedded")), ROOT / "murphy" / "MURPHY_GITHUB_FULL_EVIDENCE.csv")

with zipfile.ZipFile(ROOT / "source" / "GBPUSD_H1_2016_2025_MASTER.zip") as archive:
    archive.extractall(ROOT / "source" / "unpacked")
source_csv = first_csv(ROOT / "source" / "unpacked")
Path("/tmp/source_csv_path").write_text(str(source_csv), encoding="utf-8")
print(f"Prepared source: {source_csv}")
