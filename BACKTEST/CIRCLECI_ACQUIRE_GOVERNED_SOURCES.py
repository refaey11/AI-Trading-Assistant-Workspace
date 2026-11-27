from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

import pandas as pd

FILES = {
    "h1.zip": "/New 8/GBPUSD_H1_2016_2025_MASTER.zip",
    "nison.csv": "/New 8/NISON_2016_2024_FULL_EVIDENCE.csv",
    "murphy.zip": "/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip",
    "market_state.csv": "/New 8/GBPUSD_MARKET_STATE 6.csv",
    "mtf.zip": "/MTF_ALIGNMENT_GBPUSD_V1.zip",
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
        headers={"Authorization": f"Bearer {token}", "Dropbox-API-Arg": json.dumps({"path": remote_path})},
    )
    try:
        with urllib.request.urlopen(req, timeout=900) as response, output.open("wb") as handle:
            while True:
                chunk = response.read(4 * 1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
    except Exception as exc:
        raise SystemExit(f"DROPBOX_DOWNLOAD_FAILED path={remote_path} error={exc}") from exc


def build_canonical_mtf_source(mtf_root: Path, output: Path) -> Path:
    """Select and validate existing six-TF annual source files for 2016-2024 only.

    No MTF values are created, encoded, imputed, scaled, or interpreted here.
    """
    from BACKTEST.mtf_source_contract_gate_v1 import REQUIRED, inspect, parse_aware_timestamps

    frames: list[pd.DataFrame] = []
    for year in range(2016, 2025):
        matches = sorted(mtf_root.rglob(f"GBPUSD_M5_MTF_ALIGNMENT_{year}.csv"))
        if len(matches) != 1:
            raise SystemExit(f"MTF_FILE_COUNT_FAIL:{year}:{matches}")

        source_path = matches[0]
        try:
            inspect(source_path)
        except SystemExit as exc:
            raise SystemExit(f"MTF_SOURCE_INVALID:{year}:{exc}") from exc

        frame = pd.read_csv(source_path, low_memory=False)
        if frame.empty:
            raise SystemExit(f"MTF_EMPTY_SOURCE_FILE:{year}:{source_path}")
        frame["timestamp"] = parse_aware_timestamps(
            frame["timestamp"],
            label=f"MTF_SOURCE:{year}",
            error_prefix="BLOCKED_SOURCE",
        )
        for field in REQUIRED:
            frame[field] = pd.to_numeric(frame[field], errors="raise").astype(float)
        frames.append(frame)

    combined = pd.concat(frames, ignore_index=True).sort_values("timestamp").reset_index(drop=True)
    if combined["timestamp"].duplicated().any():
        raise SystemExit("MTF_GLOBAL_TIMESTAMP_DUPLICATE_FAIL")

    output.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output, index=False)
    return output


def main() -> int:
    token = os.environ.get("DROPBOX_ACCESS_TOKEN", "")
    if not token:
        raise SystemExit("DROPBOX_ACCESS_TOKEN is not configured in CircleCI project/context")

    Path("artifacts/integration_gate").mkdir(parents=True, exist_ok=True)
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

    canonical_mtf = build_canonical_mtf_source(
        unpacked / "mtf",
        Path("artifacts/integration_gate/mtf_alignment_2016_2024.csv"),
    )

    paths = {
        "H1": next((p for p in (unpacked / "h1").rglob("GBPUSD_H1_2016_2025_MASTER.csv")), None),
        "MARKET_STATE": raw / "market_state.csv",
        "MURPHY": next((p for p in (unpacked / "murphy").rglob("MURPHY_2016_2024_FULL_EVIDENCE.csv")), None),
        "MTF": canonical_mtf,
        "HC": next((p for p in (unpacked / "historical_context").rglob("HISTORICAL_CONTEXT_MEMORY.csv")), None),
        "HO": next((p for p in (unpacked / "historical_outcome").rglob("HISTORICAL_OUTCOMES.csv")), None),
    }
    for key, value in paths.items():
        if value is None or not Path(value).exists():
            raise SystemExit(f"MISSING {key} CSV: {value}")
        print(f"FOUND {key}={value}")

    with Path(os.environ.get("BASH_ENV", "/tmp/bash_env")).open("a", encoding="utf-8") as env:
        for key, value in paths.items():
            env.write(f"export {key}='{value}'\n")
        env.write("export SIM_DIR='artifacts/unpacked/similarity'\n")
        env.write("export RET_DIR='artifacts/unpacked/retrieval'\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
