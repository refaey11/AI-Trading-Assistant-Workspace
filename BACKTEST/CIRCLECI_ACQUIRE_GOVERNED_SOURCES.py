from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
import zipfile

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

REQUIRED_BRAIN_MTF_FIELDS = {
    "timestamp",
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
}
REGIME_FIELDS = tuple(sorted(REQUIRED_BRAIN_MTF_FIELDS - {"timestamp", "mtf_trend_score"}))
V1_REGIME_MAP = {
    "BULL_TREND": 1.0,
    "BEAR_TREND": -1.0,
    "TRANSITION": 0.0,
    "UNKNOWN": 0.0,
    "BULLISH": 1.0,
    "BEARISH": -1.0,
    "NEUTRAL": 0.0,
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
        with urllib.request.urlopen(req, timeout=900) as response, output.open("wb") as handle:
            while True:
                chunk = response.read(4 * 1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
    except Exception as exc:
        raise SystemExit(f"DROPBOX_DOWNLOAD_FAILED path={remote_path} error={exc}") from exc


def _normalize_regime(df: pd.DataFrame, field: str, path: Path) -> None:
    source = df[field].astype("string").str.strip()
    numeric = pd.to_numeric(df[field], errors="coerce")
    mapped = source.str.upper().map(V1_REGIME_MAP)
    missing = source.isna() | source.eq("")
    unknown = numeric.isna() & mapped.isna() & ~missing
    if unknown.any():
        examples = sorted(source[unknown].dropna().unique().tolist())[:10]
        raise SystemExit(f"MTF_SOURCE_UNKNOWN_REGIME_TOKEN path={path} field={field} examples={examples}")
    df[f"{field}_source"] = source
    numeric = numeric.copy()
    numeric.loc[numeric.isna()] = mapped.loc[numeric.isna()]
    df[field] = numeric.astype(float)


def build_mtf_development_csv(unpacked_root: Path, output: Path) -> None:
    candidates: list[Path] = []
    for year in range(2016, 2025):
        matches = sorted(unpacked_root.rglob(f"GBPUSD_M5_MTF_ALIGNMENT_{year}.csv"))
        if not matches:
            raise SystemExit(f"MISSING_MTF_ANNUAL_SOURCE year={year}")
        candidates.append(matches[0])

    frames: list[pd.DataFrame] = []
    skipped_rows = 0
    for path in candidates:
        df = pd.read_csv(path, low_memory=False)
        missing = sorted(REQUIRED_BRAIN_MTF_FIELDS - set(df.columns))
        if missing:
            raise SystemExit(f"MTF_SOURCE_MISSING_REQUIRED_FIELDS path={path} missing={missing}")
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        if df["timestamp"].isna().any():
            raise SystemExit(f"MTF_SOURCE_INVALID_TIMESTAMP path={path}")
        score = pd.to_numeric(df["mtf_trend_score"], errors="coerce")
        if score.isna().any():
            raise SystemExit(f"MTF_SOURCE_NON_NUMERIC_FIELD path={path} field=mtf_trend_score")
        df["mtf_trend_score"] = score.astype(float)
        for field in REGIME_FIELDS:
            _normalize_regime(df, field, path)
        valid = df[list(REGIME_FIELDS)].notna().all(axis=1)
        skipped = int((~valid).sum())
        if skipped:
            skipped_rows += skipped
            print(f"MTF_SOURCE_INCOMPLETE_ROWS path={path} skipped={skipped}")
            df = df.loc[valid].copy()
        if df.empty:
            raise SystemExit(f"MTF_SOURCE_EMPTY_VALID_ROWS path={path}")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True).sort_values("timestamp")
    combined = combined[(combined["timestamp"].dt.year >= 2016) & (combined["timestamp"].dt.year <= 2024)]
    if combined["timestamp"].duplicated().any():
        raise SystemExit("MTF_SOURCE_DUPLICATE_TIMESTAMP")
    if combined.empty:
        raise SystemExit("MTF_SOURCE_EMPTY_2016_2024")
    output.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output, index=False)
    print(
        f"MTF_BRAIN_SOURCE_READY rows={len(combined)} skipped_incomplete_rows={skipped_rows} "
        f"from={combined.timestamp.min().isoformat()} to={combined.timestamp.max().isoformat()}"
    )


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
        try:
            with zipfile.ZipFile(raw / f"{bundle}.zip") as archive:
                archive.extractall(target)
        except Exception as exc:
            raise SystemExit(f"ZIP_EXTRACT_FAILED bundle={bundle} error={exc}") from exc

    paths = {
        "H1": next((p for p in (unpacked / "h1").rglob("GBPUSD_H1_2016_2025_MASTER.csv")), None),
        "MARKET_STATE": raw / "market_state.csv",
        "MURPHY": next((p for p in (unpacked / "murphy").rglob("MURPHY_2016_2024_FULL_EVIDENCE.csv")), None),
        "HC": next((p for p in (unpacked / "historical_context").rglob("HISTORICAL_CONTEXT_MEMORY.csv")), None),
        "HO": next((p for p in (unpacked / "historical_outcome").rglob("HISTORICAL_OUTCOMES.csv")), None),
    }
    for key, value in paths.items():
        if value is None or not Path(value).exists():
            raise SystemExit(f"MISSING {key} CSV: {value}")
        print(f"FOUND {key}={value}")

    mtf_output = Path("artifacts/unpacked/mtf/GBPUSD_MTF_ALIGNMENT_2016_2024.csv")
    build_mtf_development_csv(unpacked / "mtf", mtf_output)
    paths["MTF"] = mtf_output

    with Path(os.environ.get("BASH_ENV", "/tmp/bash_env")).open("a", encoding="utf-8") as env:
        for key, value in paths.items():
            env.write(f"export {key}='{value}'\n")
        env.write("export SIM_DIR='artifacts/unpacked/similarity'\n")
        env.write("export RET_DIR='artifacts/unpacked/retrieval'\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
