from __future__ import annotations

import argparse
import json
from pathlib import Path
import zipfile

import pandas as pd

from DEVELOPMENT_2016_2024.xauusd_murphy_0006_0007_runtime_evidence_v1 import (
    build_xau_trendline_evidence,
)


SOURCE_CSV_NAME = "XAUUSD_M1_MASTER_2016_2026_08.csv"


def load_input(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            matches = [name for name in archive.namelist() if Path(name).name == SOURCE_CSV_NAME]
            if not matches:
                raise FileNotFoundError(f"{SOURCE_CSV_NAME} not found in {path}")
            with archive.open(matches[0]) as handle:
                return pd.read_csv(handle, usecols=["timestamp", "open", "high", "low", "close"])

    return pd.read_csv(path, usecols=["timestamp", "open", "high", "low", "close"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="XAUUSD M1 CSV or ZIP.")
    parser.add_argument("--output", type=Path, required=True, help="Sparse 0006/0007 evidence CSV.")
    args = parser.parse_args()

    bars = load_input(args.input)
    evidence = build_xau_trendline_evidence(bars)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    evidence.to_csv(args.output, index=False)

    manifest = {
        "status": "PASS_WITH_NOT_EVALUABLES",
        "mode": "XAUUSD_MURPHY_0006_0007_RUNTIME_EVIDENCE_V1",
        "development_window": "2016-2024",
        "rules": ["MURPHY_0006", "MURPHY_0007"],
        "rows": int(len(evidence)),
        "2025_used": False,
        "source_backed_geometry": True,
        "runtime_reused": True,
        "touch_threshold": None,
        "reaction_threshold": None,
        "atr_threshold": None,
        "output": str(args.output),
    }
    manifest_path = args.output.with_name("XAUUSD_MURPHY_0006_0007_EVIDENCE_MANIFEST.json")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
