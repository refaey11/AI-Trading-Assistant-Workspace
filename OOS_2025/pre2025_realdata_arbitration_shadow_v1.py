from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys
import zipfile

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain

DIRECTIONAL = {"BULLISH", "BEARISH"}
LOCKED_OOS_YEAR = 2025
PAIR = "GBPUSD"


def read_csv(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp", kind="stable").drop_duplicates("timestamp", keep="last").reset_index(drop=True)


def read_zip_csv(path: Path, member: str, required: set[str]) -> pd.DataFrame:
    with zipfile.ZipFile(path) as zf:
        with zf.open(member) as fh:
            data = pd.read_csv(fh)
    missing = sorted(required - set(data.columns))
    if missing:
        raise ValueError(f"{member}: missing columns {missing}")
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True, errors="coerce")
    if data["timestamp"].isna().any():
        raise ValueError(f"{member}: invalid timestamps")
    return data.sort_values("timestamp", kind="stable").drop_duplicates("timestamp", keep="last").reset_index(drop=True)


def normalize_direction(value) -> str:
    text = str(value or "").upper()
    if text in {"BULL", "BULLISH", "UP", "UPTREND"}:
        return "BULLISH"
    if text in {"BEAR", "BEARISH", "DOWN", "DOWNTREND"}:
        return "BEARISH"
    return "NONE"


def build_murphy_0021(h1: pd.DataFrame, m1: pd.DataFrame) -> pd.DataFrame:
    from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021
    h1 = h1.copy()
    m1 = m1.copy()
    h1["previous_close"] = h1["close"].shift(1)
    m1["h1_timestamp"] = m1["timestamp"].dt.floor("h")
    volume = (m1.groupby("h1_timestamp", as_index=False).agg(volume=("volume", "sum"), m1_count=("volume", "size")).sort_values("h1_timestamp"))
    volume["previous_volume"] = volume["volume"].shift(1)
    volume["volume_direction"] = None
    volume.loc[volume["volume"] > volume["previous_volume"], "volume_direction"] = "UP"
    volume.loc[volume["volume"] < volume["previous_volume"], "volume_direction"] = "DOWN"
    merged = h1.merge(volume[["h1_timestamp", "volume_direction", "m1_count"]], left_on="timestamp", right_on="h1_timestamp", how="left")
    rows = []
    for row in merged.itertuples(index=False):
        r = evaluate_0021({"close": row.close, "previous_close": row.previous_close, "volume_direction": row.volume_direction})
        rows.append({
            "timestamp": row.timestamp,
            "status": r["status"],
            "direction": normalize_direction(r.get("directional_confirmation")),
            "source_rule_id": r["rule_id"],
            "reason": r.get("reason"),
        })
    return pd.DataFrame(rows)


def audit(*, market_state: Path, mtf_archive: Path, h1: Path, m1: Path, year: int, output: Path) -> dict:
    if year >= LOCKED_OOS_YEAR:
        raise ValueError("2025_OOS_LOCKED: shadow audit must be pre-2025")

    state = read_csv(market_state, {"timestamp", "close", "atr20"})
    state = state[state["timestamp"].dt.year.eq(year)].copy()
    mtf = read_zip_csv(mtf_archive, f"{PAIR}_MTF_H4_H1.csv", {"timestamp"})
    mtf = mtf[mtf["timestamp"].dt.year.eq(year)].copy()
    h1_df = read_csv(h1, {"timestamp", "open", "high", "low", "close"})
    h1_df = h1_df[h1_df["timestamp"].dt.year.eq(year)].copy()
    m1_df = read_csv(m1, {"timestamp", "open", "high", "low", "close", "volume"})
    m1_df = m1_df[m1_df["timestamp"].dt.year.eq(year)].copy()

    murphy = build_murphy_0021(
        read_csv(h1, {"timestamp", "open", "high", "low", "close"}),
        read_csv(m1, {"timestamp", "open", "high", "low", "close", "volume"}),
    )
    murphy = murphy[murphy["timestamp"].dt.year.eq(year)].copy()

    mtf_lookup = mtf.set_index("timestamp")
    murphy_lookup = murphy.set_index("timestamp")
    records = []
    counts = Counter()

    for ts, row in state.set_index("timestamp").iterrows():
        brain = decision_brain.assess(row.to_dict(), similarity=None)
        brain_direction = normalize_direction(getattr(brain, "directional_bias", None))
        brain_confidence = float(getattr(brain, "confidence", 0.0) or 0.0)
        m = murphy_lookup.loc[ts] if ts in murphy_lookup.index else None
        if isinstance(m, pd.DataFrame):
            m = m.iloc[-1]
        murphy_direction = normalize_direction(m.get("direction") if m is not None else None)
        murphy_status = str(m.get("status") if m is not None else "NOT_EVALUABLE")

        if brain_direction not in DIRECTIONAL and murphy_direction not in DIRECTIONAL:
            classification = "NO_DIRECTION"
        elif brain_direction in DIRECTIONAL and murphy_direction not in DIRECTIONAL:
            classification = "BRAIN_ONLY"
        elif murphy_direction in DIRECTIONAL and brain_direction not in DIRECTIONAL:
            classification = "MURPHY_ONLY"
        elif brain_direction == murphy_direction:
            classification = "AGREE"
        else:
            classification = "CONFLICT"

        mtf_row = mtf_lookup.loc[ts] if ts in mtf_lookup.index else None
        mtf_state = normalize_direction(mtf_row.get("MTF_state") if mtf_row is not None else None)
        counts[classification] += 1
        records.append({
            "timestamp": ts,
            "brain_direction": brain_direction,
            "brain_confidence": brain_confidence,
            "murphy_0021_status": murphy_status,
            "murphy_0021_direction": murphy_direction,
            "mtf_state": mtf_state,
            "arbitration_classification": classification,
        })

    out = pd.DataFrame(records)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    total = len(out)
    summary = {
        "status": "PASS_SHADOW_ONLY",
        "mode": "REAL_DATA_PRE2025_SHADOW",
        "evaluation_year": year,
        "pair": PAIR,
        "events": total,
        "arbitration_counts": dict(counts),
        "coverage": {
            "brain_directional_pct": round(100.0 * sum(1 for x in out["brain_direction"] if x in DIRECTIONAL) / total, 4) if total else 0.0,
            "murphy_0021_directional_pct": round(100.0 * sum(1 for x in out["murphy_0021_direction"] if x in DIRECTIONAL) / total, 4) if total else 0.0,
            "agreement_pct": round(100.0 * counts.get("AGREE", 0) / total, 4) if total else 0.0,
            "conflict_pct": round(100.0 * counts.get("CONFLICT", 0) / total, 4) if total else 0.0,
        },
        "murphy_scope": {
            "directional_anchor": "MURPHY_0021",
            "full_34_rule_runtime_reconstructed": False,
            "reason": "No authoritative pre-2025 full 34-rule runtime event stream is currently wired into this shadow runner; this audit deliberately does not synthesize missing rule evidence.",
        },
        "mtf_consumption": {
            "available_in_event_source": True,
            "consumed_by_brain": False,
            "used_for_classification_only": True,
        },
        "memory_consumption": {
            "passed_to_brain": False,
            "direction_generated": False,
        },
        "oos_2025_locked": True,
        "oos_tuning": False,
        "new_rule_semantics": False,
        "replacement_pnl": False,
        "purpose": "Measure the real-data Brain-vs-Murphy directional topology before any governed arbitration policy change.",
    }
    (output.with_suffix(".json")).write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--mtf", required=True, type=Path)
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--m1", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    summary = audit(market_state=a.market_state, mtf_archive=a.mtf, h1=a.h1, m1=a.m1, year=a.year, output=a.output)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
