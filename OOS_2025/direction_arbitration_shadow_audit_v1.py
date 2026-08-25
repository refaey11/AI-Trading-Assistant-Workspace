from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain

DIRECTIONAL = {"BULLISH", "BEARISH"}


def _read(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp", kind="stable").reset_index(drop=True)


def _murphy_direction(rows: pd.DataFrame) -> tuple[str, list[str]]:
    subset = rows.loc[
        rows["status"].astype(str).str.upper().eq("PASS")
        & rows.get("directional_confirmation", pd.Series(index=rows.index, dtype=str)).astype(str).str.upper().isin(DIRECTIONAL)
    ]
    directions = sorted(set(subset["directional_confirmation"].astype(str).str.upper()))
    if len(directions) == 1:
        return directions[0], directions
    if len(directions) > 1:
        return "CONFLICT", directions
    return "NONE", directions


def audit(context_path: Path, murphy_full_path: Path, output_path: Path, year: int) -> dict:
    context = _read(context_path, {"timestamp"})
    murphy = _read(murphy_full_path, {"timestamp", "source_rule_id", "status"})
    context = context[context["timestamp"].dt.year.eq(year)].copy()
    murphy = murphy[murphy["timestamp"].dt.year.eq(year)].copy()

    if context.empty:
        raise ValueError(f"No context rows for {year}")
    if murphy.empty:
        raise ValueError(f"No Murphy rows for {year}")

    records: list[dict] = []
    brain_counts = Counter()
    arbitration_counts = Counter()
    murphy_rule_direction_counts = Counter()

    for ts, row in context.set_index("timestamp").iterrows():
        m = murphy.loc[murphy["timestamp"].eq(ts)]
        assessment = decision_brain.assess(row.to_dict(), similarity=None)
        brain_direction = str(assessment.directional_bias or "neutral").upper()
        brain_confidence = float(assessment.confidence or 0.0)
        murphy_direction, directional_rules = _murphy_direction(m)

        if brain_direction not in {"BULLISH", "BEARISH"}:
            classification = "BRAIN_NO_DIRECTION"
        elif murphy_direction == "NONE":
            classification = "MURPHY_NO_DIRECTION"
        elif murphy_direction == "CONFLICT":
            classification = "MURPHY_INTERNAL_CONFLICT"
        elif murphy_direction == brain_direction:
            classification = "AGREE"
        else:
            classification = "CONFLICT"

        brain_counts[brain_direction] += 1
        arbitration_counts[classification] += 1
        for rule_id in directional_rules:
            murphy_rule_direction_counts[(rule_id, classification)] += 1

        records.append(
            {
                "timestamp": ts,
                "brain_direction": brain_direction,
                "brain_confidence": brain_confidence,
                "murphy_direction": murphy_direction,
                "murphy_directional_rule_ids": json.dumps(directional_rules),
                "arbitration_classification": classification,
            }
        )

    out = pd.DataFrame(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    total = len(out)
    summary = {
        "status": "PASS",
        "mode": "SHADOW_ONLY",
        "evaluation_year": year,
        "events": total,
        "brain_direction_counts": dict(brain_counts),
        "arbitration_counts": dict(arbitration_counts),
        "coverage": {
            "brain_directional_pct": round(100.0 * sum(v for k, v in brain_counts.items() if k in DIRECTIONAL) / total, 4),
            "murphy_directional_pct": round(100.0 * sum(v for k, v in arbitration_counts.items() if k not in {"BRAIN_NO_DIRECTION", "MURPHY_NO_DIRECTION"}) / total, 4),
            "agreement_pct": round(100.0 * arbitration_counts.get("AGREE", 0) / total, 4),
            "conflict_pct": round(100.0 * arbitration_counts.get("CONFLICT", 0) / total, 4),
        },
        "murphy_rule_direction_breakdown": {
            f"{rule}:{classification}": count
            for (rule, classification), count in sorted(murphy_rule_direction_counts.items())
        },
        "oos_tuning": False,
        "new_rule_semantics": False,
        "decision_semantics_changed": False,
        "purpose": "Measure whether the existing Brain-vs-Murphy veto boundary is systematically over-rejecting valid directional evidence without changing any trading semantics.",
    }
    manifest = output_path.with_suffix(".json")
    manifest.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--murphy-full-evidence", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    args = p.parse_args()
    audit(args.context, args.murphy_full_evidence, args.output, args.year)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
