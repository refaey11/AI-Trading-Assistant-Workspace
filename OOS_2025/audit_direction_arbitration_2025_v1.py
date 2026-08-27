from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain


def _read(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp", kind="stable").reset_index(drop=True)


def _brain_bias_counts(context: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in context.to_dict("records"):
        assessment = decision_brain.assess(row)
        rows.append(
            {
                "timestamp": row["timestamp"],
                "brain_bias": str(assessment.directional_bias).upper(),
                "brain_confidence": float(assessment.confidence),
                "brain_market_state": str(assessment.market_state),
            }
        )
    return pd.DataFrame(rows)


def _candidate_map(murphy: pd.DataFrame) -> pd.DataFrame:
    out = murphy[["timestamp", "status", "direction", "source_rule_id"]].copy()
    out["candidate_status"] = out["status"].astype(str).str.upper()
    out["candidate_direction"] = out["direction"].astype(str).str.upper()
    return out[["timestamp", "candidate_status", "candidate_direction", "source_rule_id"]]


def _normalize_direction(value: str) -> str:
    value = str(value).upper()
    if value in {"BULL", "BULLISH", "BUY"}:
        return "BULLISH"
    if value in {"BEAR", "BEARISH", "SELL"}:
        return "BEARISH"
    return value


def audit(context_path: Path, murphy_path: Path, risk_path: Path, output_json: Path, output_csv: Path) -> dict:
    context = _read(context_path, {"timestamp"})
    murphy = _read(murphy_path, {"timestamp", "status", "direction", "source_rule_id"})
    risk = _read(risk_path, {"timestamp", "risk_status"})

    context = context[context["timestamp"].dt.year.eq(2025)].copy()
    murphy = murphy[murphy["timestamp"].dt.year.eq(2025)].copy()
    risk = risk[risk["timestamp"].dt.year.eq(2025)].copy()

    brain = _brain_bias_counts(context)
    candidate = _candidate_map(murphy)
    merged = brain.merge(candidate, on="timestamp", how="inner", validate="one_to_one")
    merged = merged.merge(risk[["timestamp", "risk_status"]], on="timestamp", how="left", validate="one_to_one")
    merged["brain_direction"] = merged["brain_bias"].map(_normalize_direction)
    merged["candidate_direction_norm"] = merged["candidate_direction"].map(_normalize_direction)
    merged["direction_relation"] = "NOT_APPLICABLE"
    comparable = merged["brain_direction"].isin(["BULLISH", "BEARISH"]) & merged["candidate_direction_norm"].isin(["BULLISH", "BEARISH"])
    merged.loc[comparable & (merged["brain_direction"] == merged["candidate_direction_norm"]), "direction_relation"] = "MATCH"
    merged.loc[comparable & (merged["brain_direction"] != merged["candidate_direction_norm"]), "direction_relation"] = "OPPOSITE"
    merged.loc[merged["brain_bias"].isin(["NEUTRAL", "CONFLICTED"]), "direction_relation"] = "BRAIN_NON_DIRECTIONAL"

    candidate_pass = merged[merged["candidate_status"].eq("PASS")].copy()
    risk_pass = candidate_pass[candidate_pass["risk_status"].astype(str).str.upper().eq("PASS")].copy()

    confusion = (
        candidate_pass.groupby(["candidate_direction_norm", "brain_bias"], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values(["candidate_direction_norm", "brain_bias"])
    )
    confusion.to_csv(output_csv, index=False)

    relation_counts = Counter(candidate_pass["direction_relation"].astype(str))
    risk_relation_counts = Counter(risk_pass["direction_relation"].astype(str))

    result = {
        "status": "PASS",
        "evaluation_year": 2025,
        "context_rows": int(len(context)),
        "candidate_rows": int(len(murphy)),
        "risk_rows": int(len(risk)),
        "candidate_pass_rows": int(len(candidate_pass)),
        "risk_pass_candidate_rows": int(len(risk_pass)),
        "brain_bias_counts_all_context": {k: int(v) for k, v in Counter(brain["brain_bias"]).items()},
        "candidate_direction_counts": {k: int(v) for k, v in Counter(candidate_pass["candidate_direction_norm"]).items()},
        "candidate_pass_direction_relation_counts": {k: int(v) for k, v in relation_counts.items()},
        "risk_pass_candidate_direction_relation_counts": {k: int(v) for k, v in risk_relation_counts.items()},
        "candidate_pass_brain_confusion": confusion.to_dict("records"),
        "risk_pass_confusion": (
            risk_pass.groupby(["candidate_direction_norm", "brain_bias"], dropna=False)
            .size()
            .reset_index(name="count")
            .sort_values(["candidate_direction_norm", "brain_bias"])
            .to_dict("records")
        ),
        "notes": [
            "Audit-only diagnostic. No rule thresholds, semantics, or P&L logic are changed.",
            "BRAIN_NON_DIRECTIONAL separates neutral/conflicted Brain assessments from true opposite directional conflicts.",
            "This report is intended to explain zero executable trades without tuning 2025.",
        ],
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", required=True, type=Path)
    parser.add_argument("--murphy", required=True, type=Path)
    parser.add_argument("--risk", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    args = parser.parse_args()
    audit(args.context, args.murphy, args.risk, args.output_json, args.output_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
