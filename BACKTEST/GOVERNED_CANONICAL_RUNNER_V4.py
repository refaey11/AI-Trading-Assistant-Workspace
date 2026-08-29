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

    The authoritative MTF source uses H4_trend / H1_trend. We map those names
    into the V3 field names without creating new timeframes or scores.
    """
    out = base.brain_row(row.copy())

    aliases = {
        "H4_trend": "h4_trend",
        "H1_trend": "h1_trend",
        "H4_trend_regime": "H4_trend_regime",
        "H1_trend_regime": "H1_trend_regime",
    }
    for source, target in aliases.items():
        if source in row.index and pd.notna(row[source]):
            # base.brain_row handles the canonical regime keys; only add the
            # lower-case aliases used by V3's local compatibility logic.
            out[target] = row[source]

    # Ensure authoritative H4/H1 trends are normalized into the existing
    # numeric regime fields when the source provides the textual trend labels.
    trend_map = {"BULL_TREND": 1.0, "BEAR_TREND": -1.0, "TRANSITION": 0.0, "UNKNOWN": 0.0}
    for tf in ("H1", "H4"):
        key = f"{tf}_trend"
        if key in row.index and pd.notna(row[key]):
            raw = str(row[key]).upper()
            out[f"{tf}_trend_regime"] = trend_map.get(raw, out.get(f"{tf}_trend_regime", 0.0))

    return out


# V3 uses brain_row() directly, so replace only that helper. There is no
# build_row() dependency in the actual V3 revision used by CircleCI.
base.read_csv = read_csv
_original_brain_row = base.brain_row
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
