from __future__ import annotations

"""Fail-closed merge of frozen Murphy 0006/0007 evaluator evidence into an existing Murphy fan-in.

This utility does not evaluate Murphy semantics and does not create evidence. It only:
1) finds exactly one evaluator/confirmation CSV per 0006/0007 in an already-extracted archive,
2) verifies explicit availability is strictly before the decision timestamp,
3) normalizes schema-only fields, and
4) appends those rows to an existing Murphy fan-in source.

The existing fan-in rows are preserved byte-for-byte at the pandas value level except for
normal column alignment.  No rule logic, thresholds, direction generation, or tuning is
performed here.
"""

import argparse
from pathlib import Path
import json
import pandas as pd

RULES = {"MURPHY_0006", "MURPHY_0007"}
ID_FIELDS = ["source_rule_id", "rule_id", "murphy_rule_id"]
AVAIL_FIELDS = [
    "confirmation_available_timestamp",
    "confirmation_available_at",
    "evidence_availability_timestamp",
    "availability_timestamp",
    "available_at",
]


def parse_ts(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, utc=True, errors="coerce", format="mixed")


def find_candidates(root: Path) -> list[dict]:
    candidates: list[dict] = []
    for path in sorted(root.rglob("*.csv")):
        text = str(path).lower()
        if "0006" not in text and "0007" not in text:
            continue
        if "evaluator" not in text and "confirmation" not in text:
            continue
        try:
            head = pd.read_csv(path, nrows=5, low_memory=False)
        except Exception:
            continue
        id_field = next((c for c in ID_FIELDS if c in head.columns), None)
        avail_field = next((c for c in AVAIL_FIELDS if c in head.columns), None)
        if not id_field or not avail_field or "timestamp" not in head.columns:
            continue
        try:
            df = pd.read_csv(path, low_memory=False)
            ids = set()
            for value in df[id_field].dropna():
                ids.update(x.strip() for x in str(value).split("|") if x.strip())
            hits = sorted(ids & RULES)
            if not hits:
                continue
            ts = parse_ts(df["timestamp"])
            av = parse_ts(df[avail_field])
            in_window = (
                ts.notna() & av.notna()
                & (ts >= pd.Timestamp("2016-01-01", tz="UTC"))
                & (ts < pd.Timestamp("2025-01-01", tz="UTC"))
                & (av >= pd.Timestamp("2016-01-01", tz="UTC"))
                & (av < pd.Timestamp("2025-01-01", tz="UTC"))
            )
            non_strict = int((in_window & ~(av < ts)).sum())
            candidates.append({
                "path": path,
                "id_field": id_field,
                "availability_field": avail_field,
                "rules": hits,
                "rows": int(len(df)),
                "window_rows": int(in_window.sum()),
                "non_strict_rows": non_strict,
            })
        except Exception:
            continue
    return candidates


def normalize_candidate(candidate: dict) -> pd.DataFrame:
    df = pd.read_csv(candidate["path"], low_memory=False)
    id_field = candidate["id_field"]
    avail_field = candidate["availability_field"]
    out = df.copy()
    out["timestamp"] = parse_ts(out["timestamp"])
    out["availability_timestamp"] = parse_ts(out[avail_field])
    out["source_rule_id"] = out[id_field].astype("string")

    mask = (
        out["timestamp"].notna()
        & out["availability_timestamp"].notna()
        & (out["timestamp"] >= pd.Timestamp("2016-01-01", tz="UTC"))
        & (out["timestamp"] < pd.Timestamp("2025-01-01", tz="UTC"))
        & (out["availability_timestamp"] >= pd.Timestamp("2016-01-01", tz="UTC"))
        & (out["availability_timestamp"] < pd.Timestamp("2025-01-01", tz="UTC"))
        & (out["availability_timestamp"] < out["timestamp"])
    )
    out = out.loc[mask].copy()
    out["strict_asof_status"] = "PASS"
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, type=Path)
    ap.add_argument("--archive-root", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    base = pd.read_csv(args.base, low_memory=False)
    required = {"timestamp", "source_rule_id"}
    missing = sorted(required - set(base.columns))
    if missing:
        raise SystemExit(f"BLOCKED_BASE_MURPHY_SCHEMA:{missing}")
    base["timestamp"] = parse_ts(base["timestamp"])
    if base["timestamp"].isna().any():
        raise SystemExit("BLOCKED_BASE_MURPHY_INVALID_TIMESTAMP")
    base = base[(base["timestamp"] >= pd.Timestamp("2016-01-01", tz="UTC")) & (base["timestamp"] < pd.Timestamp("2025-01-01", tz="UTC"))].copy()

    existing = {x.strip() for v in base["source_rule_id"].dropna() for x in str(v).split("|") if x.strip()}
    if RULES & existing:
        raise SystemExit(f"BLOCKED_0006_0007_ALREADY_PRESENT_IN_BASE:{sorted(RULES & existing)}")

    candidates = find_candidates(args.archive_root)
    by_rule = {rule: [c for c in candidates if rule in c["rules"]] for rule in RULES}
    problems = {rule: len(items) for rule, items in by_rule.items() if len(items) != 1}
    if problems:
        raise SystemExit(f"BLOCKED_AMBIGUOUS_OR_MISSING_0006_0007_CANDIDATES:{problems}")

    for c in candidates:
        if c["non_strict_rows"]:
            raise SystemExit(f"BLOCKED_NON_STRICT_EVALUATOR_ROWS:{c['path']}:{c['non_strict_rows']}")

    parts = [base]
    provenance = []
    for rule in sorted(RULES):
        c = by_rule[rule][0]
        part = normalize_candidate(c)
        ids = {x.strip() for v in part["source_rule_id"].dropna() for x in str(v).split("|") if x.strip()}
        if rule not in ids:
            raise SystemExit(f"BLOCKED_NORMALIZATION_LOST_RULE:{rule}:{c['path']}")
        if not ((part["availability_timestamp"] < part["timestamp"]).all()):
            raise SystemExit(f"BLOCKED_POST_NORMALIZATION_STRICT_ASOF:{rule}:{c['path']}")
        parts.append(part)
        provenance.append({
            "rule": rule,
            "path": str(c["path"]),
            "rows_before_window": c["rows"],
            "rows_after_strict_asof": int(len(part)),
            "id_field": c["id_field"],
            "availability_field": c["availability_field"],
        })

    columns = sorted(set().union(*(set(p.columns) for p in parts)))
    merged = pd.concat([p.reindex(columns=columns) for p in parts], ignore_index=True, sort=False)
    merged["timestamp"] = parse_ts(merged["timestamp"])
    merged["availability_timestamp"] = parse_ts(merged["availability_timestamp"]) if "availability_timestamp" in merged.columns else pd.NaT
    merged = merged.sort_values(["timestamp", "source_rule_id"], kind="stable").reset_index(drop=True)
    merged.to_csv(args.output, index=False)

    report = {
        "status": "PASS",
        "base_rows": int(len(base)),
        "merged_rows": int(len(merged)),
        "added_rows": int(len(merged) - len(base)),
        "rules_added": sorted(RULES),
        "provenance": provenance,
        "strict_operator": "availability_timestamp < decision_timestamp(timestamp)",
        "synthetic_evidence_generated": False,
        "direction_generated": False,
        "tuning_applied": False,
        "2025_used": False,
        "output": str(args.output),
    }
    report_path = args.output.with_name(args.output.stem + "_REPORT.json")
    report_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
