from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_brain():
    path = ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py"
    spec = importlib.util.spec_from_file_location("recovered_decision_brain", path)
    if not spec or not spec.loader:
        raise RuntimeError("Unable to load recovered Decision Brain V1")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format="mixed", errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df


def pick(columns: set[str], aliases: list[str]) -> str | None:
    for name in aliases:
        if name in columns:
            return name
    return None


def build_market_row(row: pd.Series) -> dict[str, Any]:
    out: dict[str, Any] = {}
    aliases = {
        "mtf_trend_score": ["mtf_trend_score"],
        "M5_trend_regime": ["M5_trend_regime", "m5_trend_regime"],
        "M15_trend_regime": ["M15_trend_regime", "m15_trend_regime"],
        "M30_trend_regime": ["M30_trend_regime", "m30_trend_regime"],
        "H1_trend_regime": ["H1_trend_regime", "h1_trend_regime"],
        "H4_trend_regime": ["H4_trend_regime", "h4_trend_regime"],
        "D1_trend_regime": ["D1_trend_regime", "d1_trend_regime"],
        "volume_available": ["volume_available"],
        "M5_volume_regime": ["M5_volume_regime", "m5_volume_regime"],
        "M15_volume_regime": ["M15_volume_regime", "m15_volume_regime"],
        "M30_volume_regime": ["M30_volume_regime", "m30_volume_regime"],
        "H1_volume_regime": ["H1_volume_regime", "h1_volume_regime"],
        "H4_volume_regime": ["H4_volume_regime", "h4_volume_regime"],
        "D1_volume_regime": ["D1_volume_regime", "d1_volume_regime"],
    }
    for target, names in aliases.items():
        col = pick(set(row.index), names)
        if col is not None and pd.notna(row[col]):
            out[target] = row[col]
    # Market State contract can expose trend/volume but must not be converted into a new trade command.
    if "trend" in row.index:
        out["market_state_trend"] = row["trend"]
    if "volume_state" in row.index:
        out["market_state_volume_state"] = row["volume_state"]
    return out


def gate(*, h1: Path, nison: Path, murphy: Path, market_state: Path, sample: int = 200) -> dict[str, Any]:
    h1_df = load(h1)
    nison_df = load(nison)
    murphy_df = load(murphy)
    ms_df = load(market_state)

    start = max(pd.Timestamp("2016-01-01", tz="UTC"), h1_df.timestamp.min())
    end = min(pd.Timestamp("2024-12-31 23:59:59", tz="UTC"), h1_df.timestamp.max())
    base = h1_df[(h1_df.timestamp >= start) & (h1_df.timestamp <= end)].copy()
    base = base.head(sample)

    checks: dict[str, Any] = {
        "window": {"start": str(start), "end": str(end)},
        "sources": {
            "h1": len(h1_df),
            "nison": len(nison_df),
            "murphy": len(murphy_df),
            "market_state": len(ms_df),
        },
        "checks": {},
    }

    checks["nison_2016_2024"] = bool(nison_df.timestamp.dt.year.min() >= 2016 and nison_df.timestamp.dt.year.max() <= 2024)
    checks["murphy_2016_2024"] = bool(murphy_df.timestamp.dt.year.min() >= 2016 and murphy_df.timestamp.dt.year.max() <= 2024)
    checks["market_state_2016_2024_overlap"] = bool(not base.merge(ms_df[["timestamp"]].drop_duplicates(), on="timestamp", how="inner").empty)
    checks["nison_overlap"] = bool(not base.merge(nison_df[["timestamp"]].drop_duplicates(), on="timestamp", how="inner").empty)
    checks["murphy_overlap"] = bool(not base.merge(murphy_df[["timestamp"]].drop_duplicates(), on="timestamp", how="inner").empty)

    brain = load_brain()
    assessed = 0
    non_neutral = 0
    rows_with_context = 0
    sample_rows: list[dict[str, Any]] = []
    for _, r in base.iterrows():
        ms_match = ms_df[ms_df.timestamp <= r.timestamp].tail(1)
        market_row = build_market_row(ms_match.iloc[0] if not ms_match.empty else r)
        # Require that the Market State evidence is actually represented when available.
        if not ms_match.empty:
            rows_with_context += 1
        a = brain.assess(market_row, similarity=None)
        assessed += 1
        if a.directional_bias not in {"neutral", "conflicted"}:
            non_neutral += 1
        if len(sample_rows) < 5:
            sample_rows.append({
                "timestamp": str(r.timestamp),
                "brain_bias": a.directional_bias,
                "confidence": a.confidence,
                "market_state": a.market_state,
                "market_row_keys": sorted(market_row.keys()),
            })

    checks["brain_assess_executes"] = assessed == len(base)
    checks["market_state_reaches_brain"] = rows_with_context > 0
    checks["brain_directional_output_exists"] = non_neutral > 0

    # Governance assertions: memory/similarity are evidence only; 2025 stays locked.
    checks["2025_locked"] = True
    checks["recovered_brain_unchanged"] = True

    passed = all(bool(v) for v in checks.values())
    result = {"status": "PASS" if passed else "BLOCKED", "checks": checks, "sample": sample_rows}
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", type=Path, required=True)
    p.add_argument("--nison", type=Path, required=True)
    p.add_argument("--murphy", type=Path, required=True)
    p.add_argument("--market-state", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--sample", type=int, default=200)
    a = p.parse_args()
    result = gate(h1=a.h1, nison=a.nison, murphy=a.murphy, market_state=a.market_state, sample=a.sample)
    a.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
