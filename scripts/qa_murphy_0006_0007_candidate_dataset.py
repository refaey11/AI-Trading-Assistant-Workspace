"""Deterministic QA checks for the corrected Murphy 0006/0007 candidate dataset.

This is an evidence QA gate only. It does not score, tune, or promote
candidate evidence to confirmation/PASS.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import hashlib
import pandas as pd

EXPECTED_COLUMNS = [
    "rule_id", "line_id", "line_type", "direction",
    "anchor_1_timestamp", "anchor_1_price", "anchor_2_timestamp", "anchor_2_price",
    "line_availability_timestamp", "candidate_timestamp", "candidate_pivot_type",
    "candidate_pivot_price", "line_price_at_candidate", "signed_distance",
    "absolute_distance", "daily_high", "daily_low", "daily_range_intersects_line",
    "reaction_candidate_timestamp", "reaction_candidate_type",
    "reaction_directionally_consistent", "no_break_observation", "evidence_status",
]


def validate(path: Path) -> dict:
    raw = path.read_bytes()
    df = pd.read_csv(path)
    assert list(df.columns) == EXPECTED_COLUMNS
    assert len(df) == 347
    assert df.groupby("rule_id").size().to_dict() == {"MURPHY_0006": 166, "MURPHY_0007": 181}
    assert set(df.evidence_status) == {"CANDIDATE_ONLY"}
    assert set(df.no_break_observation) <= {"OBSERVATION_ONLY", "RAW_ONLY"}

    cand = pd.to_datetime(df.candidate_timestamp)
    line_avail = pd.to_datetime(df.line_availability_timestamp)
    reaction = pd.to_datetime(df.reaction_candidate_timestamp)
    assert cand.min() >= pd.Timestamp("2016-01-01")
    assert cand.max() <= pd.Timestamp("2024-12-31")
    assert reaction.dropna().min() >= pd.Timestamp("2016-01-01")
    assert reaction.dropna().max() <= pd.Timestamp("2024-12-31")
    assert (cand >= line_avail).all()
    assert ((reaction.isna()) | (reaction >= cand)).all()

    m6 = df[df.rule_id == "MURPHY_0006"]
    m7 = df[df.rule_id == "MURPHY_0007"]
    assert (m6.line_type == "LOW").all() and (m6.direction == "UP").all()
    assert (m7.line_type == "HIGH").all() and (m7.direction == "DOWN").all()
    assert df.duplicated(["rule_id", "line_id", "candidate_timestamp"]).sum() == 0
    assert (df.absolute_distance == 0).sum() == 0

    return {
        "rows": len(df),
        "rule_counts": df.groupby("rule_id").size().to_dict(),
        "reaction_candidate_rows": int(reaction.notna().sum()),
        "directionally_consistent_reactions": int((df.reaction_directionally_consistent == True).sum()),
        "daily_range_intersections": int((df.daily_range_intersects_line == True).sum()),
        "exact_zero_distance": int((df.absolute_distance == 0).sum()),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "status": "PASS_CANDIDATE_QA_ONLY",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", type=Path)
    args = ap.parse_args()
    result = validate(args.csv)
    print(result)


if __name__ == "__main__":
    main()
