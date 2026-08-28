from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path


FILES = {
    "h1.zip": "/New 8/GBPUSD_H1_2016_2025_MASTER.zip",
    "nison.csv": "/New 8/NISON_2016_2024_FULL_EVIDENCE.csv",
    "murphy.zip": "/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip",
    "market_state.csv": "/New 8/GBPUSD_MARKET_STATE 6.csv",
    "mtf.zip": "/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1.zip",
    "historical_context.zip": "/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_HISTORICAL_CONTEXT_MEMORY_V1.zip",
    "historical_outcome.zip": "/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1.zip",
    "similarity.zip": "/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_SIMILARITY_MEMORY_V2.zip",
    "retrieval.zip": "/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_CONTEXT_AWARE_RETRIEVAL_V2.zip",
}


def download(token: str, remote_path: str, output: Path) -> None:
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        data=b"",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": remote_path}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=900) as response:
            with output.open("wb") as handle:
                while True:
                    chunk = response.read(4 * 1024 * 1024)
                    if not chunk:
                        break
                    handle.write(chunk)
    except Exception as exc:
        raise SystemExit(f"DROPBOX_DOWNLOAD_FAILED path={remote_path} error={exc}") from exc


def main() -> int:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN", "")
    if not token:
        raise SystemExit("DROPBOX_ACCESS_TOKEN is not configured in CircleCI project/context")

    raw = Path("artifacts/raw")
    unpacked = Path("artifacts/unpacked")
    raw.mkdir(parents=True, exist_ok=True)
    unpacked.mkdir(parents=True, exist_ok=True)

    for name, remote_path in FILES.items():
        print(f"DOWNLOAD {remote_path}")
        download(token, remote_path, raw / name)

    for bundle in ("h1", "murphy", "mtf", "historical_context", "historical_outcome", "similarity", "retrieval"):
        target = unpacked / bundle
        target.mkdir(parents=True, exist_ok=True)
        import zipfile
        try:
            with zipfile.ZipFile(raw / f"{bundle}.zip") as archive:
                archive.extractall(target)
        except Exception as exc:
            raise SystemExit(f"ZIP_EXTRACT_FAILED bundle={bundle} error={exc}") from exc

    paths = {
        "H1": next((p for p in (unpacked / "h1").rglob("GBPUSD_H1_2016_2025_MASTER.csv")), None),
        "MURPHY": next((p for p in (unpacked / "murphy").rglob("MURPHY_2016_2024_FULL_EVIDENCE.csv")), None),
        "MTF": next((p for p in (unpacked / "mtf").rglob("GBPUSD_MTF_H4_H1.csv")), None),
        "HC": next((p for p in (unpacked / "historical_context").rglob("HISTORICAL_CONTEXT_MEMORY.csv")), None),
        "HO": next((p for p in (unpacked / "historical_outcome").rglob("HISTORICAL_OUTCOMES.csv")), None),
    }
    for key, value in paths.items():
        if value is None:
            raise SystemExit(f"MISSING {key} CSV")
        print(f"FOUND {key}={value}")

    with Path(os.environ.get("BASH_ENV", "/tmp/bash_env")).open("a", encoding="utf-8") as env:
        for key, value in paths.items():
            env.write(f"export {key}='{value}'\n")
        env.write("export SIM_DIR='artifacts/unpacked/similarity'\n")
        env.write("export RET_DIR='artifacts/unpacked/retrieval'\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
