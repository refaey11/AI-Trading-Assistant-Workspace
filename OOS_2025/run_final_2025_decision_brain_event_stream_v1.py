from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from OOS_2025.full_78_rule_decision_event_stream_v2 import build_rule_event_stream, summarize_coverage
from OOS_2025.nison_2025_evidence_aggregate_v1 import aggregate_nison_evidence

NISON_RULES = [f"NISON_{i:04d}" for i in range(1, 45)]
MURPHY_RULES = [
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007",
    "MURPHY_0018", "MURPHY_0019", "MURPHY_0021", "MURPHY_0022", "MURPHY_0023",
    "MURPHY_0025", "MURPHY_0026", "MURPHY_0028", "MURPHY_0029", "MURPHY_0030",
    "MURPHY_0031", "MURPHY_0032", "MURPHY_0033", "MURPHY_0034", "MURPHY_0035",
    "MURPHY_0036", "MURPHY_0037", "MURPHY_0038", "MURPHY_0039", "MURPHY_0040",
    "MURPHY_0041", "MURPHY_0042", "MURPHY_0043", "MURPHY_0044", "MURPHY_0045",
    "MURPHY_0047", "MURPHY_0048", "MURPHY_0049", "MURPHY_0050", "MURPHY_0051",
]


def _read(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def _nison_with_provenance(raw: pd.DataFrame, year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = raw.copy()
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True)
    raw = raw[raw["timestamp"].dt.year.eq(year)].copy()
    aggregate = aggregate_nison_evidence(raw)

    source_rows: list[dict[str, Any]] = []
    for ts, group in raw.groupby("timestamp", sort=True):
        passes = [
            str(x) for x in group.loc[
                group["status"].eq("PASS") & group["direction"].astype(str).isin({"BULLISH", "BEARISH"}),
                "rule_id",
            ]
        ]
        fails = [
            str(x) for x in group.loc[
                group["status"].eq("FAIL") & group["direction"].astype(str).isin({"BULLISH", "BEARISH"}),
                "rule_id",
            ]
        ]
        source_rows.append({
            "timestamp": ts,
            "source_rule_id": passes[0] if passes else (fails[0] if fails else "NISON_NONE"),
        })
    src = pd.DataFrame(source_rows)
    aggregate["timestamp"] = pd.to_datetime(aggregate["timestamp"], utc=True)
    aggregate = aggregate.merge(src, on="timestamp", how="left", validate="one_to_one")
    return raw, aggregate


def _murphy_candidate_stream(frames: list[pd.DataFrame], year: int) -> pd.DataFrame:
    candidates: list[pd.DataFrame] = []
    priority = {"MURPHY_0022": 0, "MURPHY_0023": 1, "MURPHY_0021": 2}
    for df in frames:
        work = df.copy()
        work["timestamp"] = pd.to_datetime(work["timestamp"], utc=True)
        work = work[work["timestamp"].dt.year.eq(year)].copy()
        work["source_rule_id"] = work["rule_id"].astype(str)
        work["direction"] = work["directional_confirmation"].astype(str)
        work["_priority"] = work["source_rule_id"].map(priority).fillna(99)
        candidates.append(work[["timestamp", "rule_id", "status", "direction", "source_rule_id", "_priority"]])
    all_rows = pd.concat(candidates, ignore_index=True)
    all_rows["_pass_rank"] = all_rows["status"].eq("PASS").astype(int)
    all_rows = all_rows.sort_values(["timestamp", "_pass_rank", "_priority"], ascending=[True, False, True])
    chosen = all_rows.drop_duplicates("timestamp", keep="first").copy()
    chosen = chosen.drop(columns=["_pass_rank", "_priority"])
    return chosen


def _load_optional(path: Path | None, required: set[str]) -> pd.DataFrame | None:
    if path is None or not path.exists():
        return None
    return _read(path, required)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--nison", required=True, type=Path)
    p.add_argument("--murphy-0021", required=True, type=Path)
    p.add_argument("--murphy-0022-0023", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--output-dir", required=True, type=Path)
    args = p.parse_args()

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    h1 = _read(args.h1, {"timestamp", "open", "high", "low", "close"})
    h1_year = h1[h1["timestamp"].dt.year.eq(args.year)].copy()

    nison_raw, nison_agg = _nison_with_provenance(
        _read(args.nison, {"timestamp", "rule_id", "status", "direction"}), args.year
    )

    m21 = _read(args.murphy_0021, {"timestamp", "rule_id", "status", "directional_confirmation"})
    m22 = _read(args.murphy_0022_0023, {"timestamp", "rule_id", "status", "directional_confirmation"})
    murphy_candidate = _murphy_candidate_stream([m21, m22], args.year)

    # Emit the complete governed 78-rule evidence boundary. Missing Murphy rules
    # remain NOT_EVALUABLE; no new semantics are invented.
    event_stream = build_rule_event_stream(
        h1_year["timestamp"].tolist(),
        murphy_rows=pd.concat([
            m21.assign(direction=m21["directional_confirmation"], available=m21["status"].isin(["PASS", "FAIL"])),
            m22.assign(direction=m22["directional_confirmation"], available=m22["status"].isin(["PASS", "FAIL"])),
        ], ignore_index=True).to_dict("records"),
        nison_rows=nison_raw.to_dict("records"),
    )
    event_stream_df = event_stream
    event_stream_df.to_csv(out / "FULL_78_RULE_2025_EVENT_STREAM.csv", index=False)
    coverage = summarize_coverage(event_stream_df)

    # Normalize the three existing source-backed Murphy candidates to the contract
    # consumed by the recovered full Decision Brain producer.
    murphy_candidate[["timestamp", "status", "direction", "source_rule_id"]].to_csv(
        out / "MURPHY_2025_CANDIDATE_STREAM.csv", index=False
    )

    nison_agg.to_csv(out / "NISON_2025_AGGREGATED.csv", index=False)

    # Save a compact manifest. Construction of risk/context/Decision Brain events
    # is intentionally delegated to the existing governed adapters in CI.
    manifest = {
        "status": "PASS",
        "evaluation_year": args.year,
        "full_78_rule_event_rows": int(len(event_stream_df)),
        "full_78_rule_coverage": coverage,
        "nison_raw_rows": int(len(nison_raw)),
        "nison_timestamp_rows": int(len(nison_agg)),
        "nison_confirmation_available_timestamps": int(nison_agg["confirmation_available"].sum()),
        "nison_contradiction_timestamps": int(nison_agg["contradiction"].sum()),
        "murphy_candidate_rows": int(len(murphy_candidate)),
        "murphy_candidate_pass_rows": int(murphy_candidate["status"].eq("PASS").sum()),
        "source_backed_only": True,
        "direction_policy": "Murphy only; Nison confirmation/context only",
        "historical_memory_used_for_direction": False,
        "tiz_generates_direction": False,
        "risk_overridden": False,
        "oos_tuning": False,
        "note": "This runner assembles the governed 78-rule evidence boundary and source-backed Decision Brain candidate stream. It does not invent missing Murphy evidence and does not promote a profitability number by itself.",
    }
    (out / "FINAL_2025_EVENT_STREAM_MANIFEST.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
