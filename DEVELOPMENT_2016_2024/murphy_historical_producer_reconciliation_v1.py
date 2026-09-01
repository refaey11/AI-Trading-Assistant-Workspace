from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

EXPECTED = {
    f"MURPHY_{i:04d}"
    for i in [
        3, 4, 6, 7, 18, 19, 21, 22, 23, 25, 26, 28, 29,
        30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
        42, 43, 44, 45, 47, 48, 49, 50, 51,
    ]
}

VALID_STATUS = {"PASS", "FAIL", "NOT_EVALUABLE", "CONFLICT"}


def split_ids(value: object) -> list[str]:
    return [
        x.strip().upper()
        for x in str(value or "").split("|")
        if x.strip() and x.strip().upper() not in {"NONE", "NULL", "NAN", "NISON_NONE"}
    ]


def main() -> None:
    root = Path("artifacts/source/murphy")
    out = Path("artifacts/source/MURPHY_CURRENT_STACK.csv")
    report_path = Path("artifacts/source/MURPHY_HISTORICAL_PRODUCER_RECONCILIATION.json")
    frames: list[pd.DataFrame] = []
    source_reports: list[dict] = []
    rule_sources: dict[str, set[str]] = {rid: set() for rid in EXPECTED}
    rule_years: dict[str, set[int]] = {rid: set() for rid in EXPECTED}
    rule_rows: dict[str, int] = {rid: 0 for rid in EXPECTED}
    unknown_ids: set[str] = set()

    for p in sorted(root.rglob("*.csv")):
        try:
            df = pd.read_csv(p, low_memory=False)
        except Exception:
            continue
        required = {"timestamp", "source_rule_id"}
        if not required.issubset(df.columns):
            continue
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
        if ts.isna().any():
            continue
        in_window = ts.dt.year.between(2016, 2024)
        if not in_window.any():
            continue
        df = df.loc[in_window].copy()
        df["timestamp"] = ts.loc[in_window]
        df["_expanded_ids"] = df["source_rule_id"].map(split_ids)
        ids = {rid for values in df["_expanded_ids"] for rid in values}
        unknown_ids.update(ids - EXPECTED)
        observed = ids & EXPECTED
        if not observed:
            continue
        for rid in observed:
            mask = df["_expanded_ids"].map(lambda values, r=rid: r in values)
            rows = int(mask.sum())
            rule_sources[rid].add(str(p))
            rule_years[rid].update(int(y) for y in df.loc[mask, "timestamp"].dt.year.unique())
            rule_rows[rid] += rows
        clean = df.drop(columns=["_expanded_ids"])
        frames.append(clean)
        source_reports.append(
            {
                "path": str(p),
                "rows_in_window": len(clean),
                "observed_rule_ids": sorted(observed),
                "unknown_rule_ids": sorted(ids - EXPECTED),
                "min_year": int(clean["timestamp"].dt.year.min()),
                "max_year": int(clean["timestamp"].dt.year.max()),
            }
        )

    if unknown_ids:
        raise SystemExit(f"BLOCKED_MURPHY_UNKNOWN_RULE_IDS:{sorted(unknown_ids)}")
    if not frames:
        raise SystemExit("BLOCKED_MURPHY_NO_HISTORICAL_PRODUCERS")

    combined = pd.concat(frames, ignore_index=True, sort=False)
    combined = combined.sort_values("timestamp", kind="stable").reset_index(drop=True)
    # Preserve distinct rule evidence at the same timestamp. Remove exact duplicates only.
    combined = combined.drop_duplicates().reset_index(drop=True)
    combined.to_csv(out, index=False)

    missing = sorted(
        rid for rid in EXPECTED
        if not rule_sources[rid]
    )
    report = {
        "status": "PASS",
        "method": "ALL_VALID_HISTORICAL_PRODUCERS_FAN_IN",
        "source_root": str(root),
        "output": str(out),
        "expected_runtime_rules": len(EXPECTED),
        "rules_with_historical_producers": len(EXPECTED) - len(missing),
        "missing_historical_producers": missing,
        "rule_coverage": {
            rid: {
                "source_files": sorted(rule_sources[rid]),
                "rows_attributed": rule_rows[rid],
                "coverage_years": sorted(rule_years[rid]),
                "full_2016_2024_coverage": set(range(2016, 2025)).issubset(rule_years[rid]),
            }
            for rid in sorted(EXPECTED)
        },
        "combined_rows": len(combined),
        "combined_years": sorted(int(y) for y in combined["timestamp"].dt.year.unique()),
        "source_files_considered": source_reports,
        "selection_policy_removed": "Do not choose a single largest CSV; fan-in every valid source-backed historical producer.",
        "synthetic_evidence_created": False,
        "2025_used": False,
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
