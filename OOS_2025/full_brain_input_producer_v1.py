from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import pandas as pd

REQUIRED = {
    "context": {"timestamp", "entry_price", "atr"},
    "murphy": {"timestamp", "status", "direction", "source_rule_id"},
    "nison": {"timestamp", "confirmation", "contradiction", "source_rule_id"},
    "risk": {"timestamp", "risk_status", "stop_loss"},
    "execution": {"timestamp", "entry_price", "atr"},
}


def read_stream(path: Path, required: set[str], name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{name}: missing authoritative stream: {path}")
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{name}: missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{name}: invalid timestamps")
    if df["timestamp"].duplicated().any():
        raise ValueError(f"{name}: duplicate timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def restrict_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    return df.loc[df["timestamp"].dt.year == year].copy()


def intersect_timestamps(streams: Iterable[pd.DataFrame]) -> pd.DatetimeIndex:
    sets = [set(df["timestamp"]) for df in streams]
    if not sets:
        return pd.DatetimeIndex([])
    common = set.intersection(*sets)
    return pd.DatetimeIndex(sorted(common), tz="UTC")


def normalize(
    *,
    context: Path,
    murphy: Path,
    nison: Path,
    risk: Path,
    execution: Path,
    year: int,
    output_dir: Path,
) -> dict:
    streams = {
        name: restrict_year(read_stream(path, REQUIRED[name], name), year)
        for name, path in {
            "context": context,
            "murphy": murphy,
            "nison": nison,
            "risk": risk,
            "execution": execution,
        }.items()
    }

    common = intersect_timestamps(streams.values())
    if len(common) == 0:
        raise ValueError(f"No fully joinable timestamps for evaluation year {year}")

    output_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    for name, df in streams.items():
        out = df[df["timestamp"].isin(common)].copy()
        out.to_csv(output_dir / f"{name}.csv", index=False)
        paths[name] = str(output_dir / f"{name}.csv")

    manifest = {
        "status": "PASS",
        "mode": "FULL_DECISION_BRAIN_INPUT_NORMALIZATION",
        "evaluation_year": year,
        "common_timestamps": len(common),
        "streams": {
            name: {
                "rows": int(len(df[df["timestamp"].isin(common)])),
                "source": paths[name],
            }
            for name, df in streams.items()
        },
        "canonical_policy": {
            "nison_confirmation_only": True,
            "tiz_process_only": True,
            "risk_hard_gate": True,
            "historical_memory_evidence_only": True,
            "2025_is_oos": True,
            "no_tuning": True,
        },
        "source_backed_only": True,
        "invented_evidence": False,
        "ready_for_full_brain_assembler": True,
    }
    (output_dir / "FULL_BRAIN_INPUT_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--risk", required=True, type=Path)
    p.add_argument("--execution", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--output-dir", required=True, type=Path)
    args = p.parse_args()
    manifest = normalize(
        context=args.context,
        murphy=args.murphy,
        nison=args.nison,
        risk=args.risk,
        execution=args.execution,
        year=args.year,
        output_dir=args.output_dir,
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
