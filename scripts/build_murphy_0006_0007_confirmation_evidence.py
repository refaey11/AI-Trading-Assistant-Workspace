"""Build candidate-only Murphy 0006/0007 confirmation evidence.

The input must already contain source-derived candidate observations. This
script performs normalization and schema validation only. It does not infer
touch, reaction, or no-break conditions and never emits PASS/FAIL.
"""

import argparse
import csv
from pathlib import Path

REQUIRED = {
    "rule_id",
    "line_id",
    "line_type",
    "direction",
    "anchor_1_timestamp",
    "anchor_1_price",
    "anchor_2_timestamp",
    "anchor_2_price",
    "line_availability_timestamp",
    "candidate_timestamp",
    "candidate_pivot_type",
    "candidate_pivot_price",
}

OUTPUT_FIELDS = [
    "rule_id", "line_id", "trendline_type", "direction", "anchor_count",
    "anchor_1_timestamp", "anchor_1_price", "anchor_2_timestamp",
    "anchor_2_price", "candidate_timestamp", "candidate_pivot_type",
    "candidate_pivot_price", "line_availability_timestamp",
    "third_touch_candidate", "reaction_candidate", "no_break_observation",
    "confirmation_available_timestamp", "status",
]

EXPECTED = {
    "MURPHY_0006": ("LOW", "UP"),
    "MURPHY_0007": ("HIGH", "DOWN"),
}


def transform(rows):
    out = []
    for row in rows:
        missing = REQUIRED - set(row)
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")
        rule = row["rule_id"]
        if rule not in EXPECTED:
            raise ValueError(f"unsupported rule_id: {rule}")
        line_type, direction = EXPECTED[rule]
        if (row["line_type"].upper(), row["direction"].upper()) != (line_type, direction):
            raise ValueError(f"rule/geometry mismatch for {rule}")
        out.append({
            "rule_id": rule,
            "line_id": row["line_id"],
            "trendline_type": line_type,
            "direction": direction,
            "anchor_count": 2,
            "anchor_1_timestamp": row["anchor_1_timestamp"],
            "anchor_1_price": row["anchor_1_price"],
            "anchor_2_timestamp": row["anchor_2_timestamp"],
            "anchor_2_price": row["anchor_2_price"],
            "candidate_timestamp": row["candidate_timestamp"],
            "candidate_pivot_type": row["candidate_pivot_type"],
            "candidate_pivot_price": row["candidate_pivot_price"],
            "line_availability_timestamp": row["line_availability_timestamp"],
            "third_touch_candidate": "CANDIDATE_ONLY",
            "reaction_candidate": "CANDIDATE_ONLY",
            "no_break_observation": "NOT_BOUND",
            "confirmation_available_timestamp": row["line_availability_timestamp"],
            "status": "CANDIDATE_ONLY",
        })
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    with args.input_csv.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = transform(rows)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(out)
    print(f"wrote {len(out)} candidate-only records to {args.output_csv}")


if __name__ == "__main__":
    main()
