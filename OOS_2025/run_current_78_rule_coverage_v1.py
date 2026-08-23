from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

NISON_RULES = [f"NISON_{i:04d}" for i in range(1, 45)]
MURPHY_RULES = [
    "MURPHY_0003","MURPHY_0004","MURPHY_0006","MURPHY_0007","MURPHY_0018","MURPHY_0019",
    "MURPHY_0021","MURPHY_0022","MURPHY_0023","MURPHY_0025","MURPHY_0026","MURPHY_0028",
    "MURPHY_0029","MURPHY_0030","MURPHY_0031","MURPHY_0032","MURPHY_0033","MURPHY_0034",
    "MURPHY_0035","MURPHY_0036","MURPHY_0037","MURPHY_0038","MURPHY_0039","MURPHY_0040",
    "MURPHY_0041","MURPHY_0042","MURPHY_0043","MURPHY_0044","MURPHY_0045","MURPHY_0047",
    "MURPHY_0048","MURPHY_0049","MURPHY_0050","MURPHY_0051",
]


def summarize_rule_frame(df: pd.DataFrame, family: str, rules: list[str]) -> pd.DataFrame:
    required = {"timestamp", "rule_id", "status"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    frame = df.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame[frame["timestamp"].dt.year.eq(2025)]
    rows: list[dict[str, object]] = []
    for rule_id in rules:
        sub = frame[frame["rule_id"].astype(str).eq(rule_id)]
        counts = sub["status"].astype(str).value_counts()
        available = int(sub["available"].fillna(False).astype(bool).sum()) if "available" in sub.columns else int(counts.get("PASS", 0) + counts.get("FAIL", 0))
        rows.append({
            "family": family,
            "rule_id": rule_id,
            "rows": int(len(sub)),
            "available_rows": available,
            "available_rate": (available / len(sub)) if len(sub) else 0.0,
            "pass_rows": int(counts.get("PASS", 0)),
            "fail_rows": int(counts.get("FAIL", 0)),
            "not_evaluable_rows": int(counts.get("NOT_EVALUABLE", 0)),
            "coverage_status": "OBSERVED_2025_OUTPUT" if len(sub) else "NO_2025_OUTPUT",
        })
    return pd.DataFrame(rows)


def build_coverage(nison_csv: str, murphy_snapshot_json: str, output_json: str) -> None:
    nison = pd.read_csv(nison_csv)
    nison_summary = summarize_rule_frame(nison, "NISON", NISON_RULES)

    # Murphy is intentionally reported from the last frozen OOS coverage snapshot
    # until a fresh authoritative Murphy 2025 producer stream is wired into CI.
    snapshot = json.loads(Path(murphy_snapshot_json).read_text(encoding="utf-8"))
    murphy_summary = pd.DataFrame(snapshot["rules"])
    murphy_summary["family"] = "MURPHY"
    murphy_summary = murphy_summary[[
        "family", "rule_id", "rows", "available_rows", "available_rate",
        "pass_rows", "fail_rows", "not_evaluable_rows", "coverage_status"
    ]]

    all_rules = pd.concat([murphy_summary, nison_summary], ignore_index=True)
    out = {
        "status": "OOS_COVERAGE_ONLY",
        "rule_count": int(len(all_rules)),
        "murphy_rules": int((all_rules.family == "MURPHY").sum()),
        "nison_rules": int((all_rules.family == "NISON").sum()),
        "observed_rules": int((all_rules.rows > 0).sum()),
        "rules_with_available_evidence": int((all_rules.available_rows > 0).sum()),
        "rules_with_full_available_rate": int((all_rules.available_rate >= 1.0).sum()),
        "no_2025_output_rules": int((all_rules.rows == 0).sum()),
        "notes": [
            "Nison counts are computed from the current full 2025 producer output.",
            "Murphy counts are from the previously frozen 2025 coverage snapshot and are not silently treated as a fresh producer run.",
            "Missing evidence remains NOT_EVALUABLE; this report does not invent semantics or tune 2025.",
        ],
        "rules": all_rules.to_dict(orient="records"),
    }
    Path(output_json).write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--nison-csv", required=True)
    parser.add_argument("--murphy-snapshot", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build_coverage(args.nison_csv, args.murphy_snapshot, args.output)
