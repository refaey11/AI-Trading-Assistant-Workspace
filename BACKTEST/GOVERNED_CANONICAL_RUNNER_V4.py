from __future__ import annotations

"""Thin governed runner over the existing V3 runtime.

Compatibility repair only:
- preserves multiple Murphy/Nison rule rows sharing a timestamp;
- prevents rule-level evidence from being collapsed before aggregation;
- maps authoritative MTF field names without changing their meaning;
- preserves the existing Decision Brain V1, Handoff, Risk and TIZ boundaries;
- keeps 2025 excluded from development consumption.
"""

import argparse
from pathlib import Path

import pandas as pd
from BACKTEST import GOVERNED_CANONICAL_RUNNER_V3 as base

_original_read_csv = base.read_csv
_original_build_row = base.build_row


def read_csv(path: Path, required: set[str], chunksize: int | None = None):
    # Rule-level evidence is many-to-one at a timestamp. The old V3 reader
    # dropped all but one rule row per timestamp, which destroyed the 78-rule
    # fan-in before aggregate_rule_frame() could combine it.
    is_rule_evidence = bool({"rule_id", "source_rule_id"} & set(required))
    if not is_rule_evidence:
        return _original_read_csv(path, required, chunksize)

    effective_chunksize = chunksize or 200_000
    parts = []
    for part in pd.read_csv(path, usecols=list(required), chunksize=effective_chunksize, low_memory=False):
        missing = sorted(required - set(part.columns))
        if missing:
            raise ValueError(f"{path}: missing {missing}")
        part["timestamp"] = pd.to_datetime(part["timestamp"], utc=True, errors="coerce", format="mixed")
        if part["timestamp"].isna().any():
            raise ValueError(f"{path}: invalid timestamp")
        years = part["timestamp"].dt.year
        if (years == 2025).any():
            raise ValueError(f"2025 rule evidence reached development runner: {path}")
        part = part[(years >= 2016) & (years <= 2024)]
        if not part.empty:
            parts.append(part)
    if not parts:
        return pd.DataFrame(columns=sorted(required))
    return pd.concat(parts, ignore_index=True).sort_values(["timestamp", *sorted((required - {"timestamp"}))]).reset_index(drop=True)


def build_row(market, mtf):
    """Normalize authoritative MTF field names into the V3 adapter names.

    This is a field-name compatibility mapping only. It does not infer a new
    score or synthesize any timeframe that the source contract does not have.
    """
    market2 = dict(market or {})
    mtf2 = dict(mtf or {})
    if "trend" not in market2 and "H1_trend" in market2:
        market2["trend"] = market2["H1_trend"]
    if "h4_trend" not in mtf2 and "H4_trend" in mtf2:
        mtf2["h4_trend"] = mtf2["H4_trend"]
    return _original_build_row(market2, mtf2)


base.read_csv = read_csv
base.build_row = build_row


def main():
    p = argparse.ArgumentParser()
    for name in (
        "h1", "market", "mtf", "murphy", "nison",
        "historical-context", "historical-outcome", "similarity",
        "retrieval", "output-dir"
    ):
        p.add_argument("--" + name, required=True, type=Path)
    return base.run(p.parse_args())

if __name__ == "__main__":
    main()
