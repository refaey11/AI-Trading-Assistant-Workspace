from __future__ import annotations

"""Thin governed runner over the existing V3 runtime.

Only corrects Nison ingestion so the 44-rule event stream is preserved without
collapsing multiple rules sharing a timestamp. Existing Decision Brain V1,
Handoff, Risk and TIZ boundaries remain authoritative and unchanged.
"""
import argparse
from pathlib import Path
import pandas as pd
from BACKTEST import GOVERNED_CANONICAL_RUNNER_V3 as base

_original_read_csv = base.read_csv


def read_csv(path: Path, required: set[str], chunksize: int | None = None):
    name = str(path).upper()
    if "NISON" not in name:
        return _original_read_csv(path, required, chunksize)
    parts=[]
    for part in pd.read_csv(path, usecols=list(required), chunksize=200_000, low_memory=False):
        missing=sorted(required-set(part.columns))
        if missing: raise ValueError(f"{path}: missing {missing}")
        part["timestamp"]=pd.to_datetime(part["timestamp"], utc=True, errors="coerce", format="mixed")
        if part["timestamp"].isna().any(): raise ValueError(f"{path}: invalid timestamp")
        if (part.timestamp.dt.year==2025).any(): raise ValueError("2025 Nison data reached development runner")
        part=part[(part.timestamp.dt.year>=2016)&(part.timestamp.dt.year<=2024)]
        if not part.empty: parts.append(part)
    if not parts: return pd.DataFrame(columns=sorted(required))
    return pd.concat(parts, ignore_index=True).sort_values(["timestamp","rule_id"]).reset_index(drop=True)

base.read_csv = read_csv


def main():
    p=argparse.ArgumentParser()
    for name in ("h1","market","mtf","murphy","nison","historical-context","historical-outcome","similarity","retrieval","output-dir"):
        p.add_argument("--"+name, required=True, type=Path)
    return base.run(p.parse_args())

if __name__ == "__main__":
    main()
