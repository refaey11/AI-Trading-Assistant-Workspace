from __future__ import annotations

"""Thin governed compatibility runner.

Preserves multi-row Murphy/Nison evidence, maps authoritative MTF names into
Decision Brain V1's existing field names, and keeps the existing V3 semantics.
No new directional logic, thresholds, or synthetic evidence are introduced.
2025 remains excluded from development consumption.
"""

import argparse
from pathlib import Path

import pandas as pd
from BACKTEST import GOVERNED_CANONICAL_RUNNER_V3 as base

_original_read_csv = base.read_csv
_original_brain_row = base.brain_row


def read_csv(path: Path, required: set[str], chunksize: int | None = None):
    # Rule-level evidence is many-to-one at a timestamp. Preserve every rule
    # row so the existing aggregate_rule_frame() can perform the fan-in.
    is_rule_evidence = bool({"rule_id", "source_rule_id"} & set(required))
    if not is_rule_evidence:
        return _original_read_csv(path, required, chunksize)

    effective_chunksize = chunksize or 200_000
    parts: list[pd.DataFrame] = []
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
    return pd.concat(parts, ignore_index=True).sort_values(
        ["timestamp", *sorted(required - {"timestamp"})]
    ).reset_index(drop=True)


def brain_row(row: pd.Series) -> dict:
    """Compatibility mapping for V3's existing brain_row() contract.

    The authoritative MTF source uses H4_trend / H1_trend. We preserve the
    existing six-timeframe schema and only normalize field names/labels.
    """
    out = _original_brain_row(row.copy())

    trend_map = {
        "BULL_TREND": 1.0,
        "BEAR_TREND": -1.0,
        "TRANSITION": 0.0,
        "UNKNOWN": 0.0,
    }
    for tf in ("M5", "M15", "M30", "H1", "H4", "D1"):
        source = f"{tf}_trend"
        if source in row.index and pd.notna(row[source]):
            raw = str(row[source]).strip().upper()
            out[f"{tf}_trend_regime"] = trend_map.get(raw, out.get(f"{tf}_trend_regime", 0.0))
        source_regime = f"{tf}_trend_regime"
        if source_regime in row.index and pd.notna(row[source_regime]):
            raw = str(row[source_regime]).strip().upper()
            out[f"{tf}_trend_regime"] = trend_map.get(raw, out.get(f"{tf}_trend_regime", 0.0))

    # Accept the authoritative MTF aggregate score if already present; do not
    # derive a new score here.
    for key in ("mtf_trend_score", "mtf_score"):
        if key in row.index and pd.notna(row[key]):
            out["mtf_trend_score"] = float(row[key])
            break

    return out


# V3 calls brain_row() directly. Replace only that helper after saving the
# original reference. All other V3 semantics remain untouched.
base.read_csv = read_csv
base.brain_row = brain_row


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
