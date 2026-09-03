from __future__ import annotations

"""Fail-closed merge of frozen Murphy 0006/0007 evaluator evidence into an existing Murphy fan-in.

This utility does not evaluate Murphy semantics and does not create evidence. It only:
1) finds candidate evaluator/confirmation CSVs by schema/content,
2) accepts the frozen confirmation-availability artifact shape,
3) bridges confirmation availability to the first canonical H1 decision timestamp strictly after availability,
4) verifies explicit availability is strictly before that decision timestamp,
5) normalizes schema-only fields, and
6) appends only confirmed rows for each target rule to an existing Murphy fan-in source.

The H1 bridge is a timing adapter only. It does not alter Murphy semantics, create
PASS/FAIL decisions, invent thresholds, or use 2025.
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


def normalized_ids(series: pd.Series) -> set[str]:
    out: set[str] = set()
    for value in series.dropna():
        for token in str(value).split("|"):
            token = token.strip().upper()
            if token in RULES:
                out.add(token)
    return out


def find_candidates(root: Path) -> list[dict]:
    candidates: list[dict] = []
    for path in sorted(root.rglob("*.csv")):
        try:
            head = pd.read_csv(path, nrows=5, low_memory=False)
        except Exception:
            continue
        id_field = next((c for c in ID_FIELDS if c in head.columns), None)
        avail_field = next((c for c in AVAIL_FIELDS if c in head.columns), None)
        if not id_field or not avail_field:
            continue
        # Two supported source shapes:
        # A) already normalized with a canonical `timestamp` decision column;
        # B) frozen confirmation artifact with confirmation_available_timestamp
        #    plus third_touch/reaction timestamps but no decision timestamp.
        has_timestamp = "timestamp" in head.columns
        has_confirmation_shape = {"third_touch_timestamp", "reaction_timestamp", "confirmation"}.issubset(head.columns)
        if not (has_timestamp or has_confirmation_shape):
            continue
        try:
            df = pd.read_csv(path, low_memory=False)
            hits = sorted(normalized_ids(df[id_field]))
            if not hits:
                continue
            if has_timestamp:
                ts = parse_ts(df["timestamp"])
            elif "reaction_timestamp" in df.columns:
                ts = parse_ts(df["reaction_timestamp"])
            else:
                ts = parse_ts(df["third_touch_timestamp"])
            av = parse_ts(df[avail_field])
            in_window = (
                ts.notna() & av.notna()
                & (ts >= pd.Timestamp("2016-01-01", tz="UTC"))
                & (ts < pd.Timestamp("2025-01-01", tz="UTC"))
                & (av >= pd.Timestamp("2016-01-01", tz="UTC"))
                & (av < pd.Timestamp("2025-01-01", tz="UTC"))
            )
            non_strict = int((in_window & ~(av < ts)).sum()) if has_timestamp else 0
            candidates.append({
                "path": path,
                "id_field": id_field,
                "availability_field": avail_field,
                "rules": hits,
                "rows": int(len(df)),
                "window_rows": int(in_window.sum()),
                "non_strict_rows": non_strict,
                "has_timestamp": has_timestamp,
                "has_confirmation_shape": has_confirmation_shape,
            })
        except Exception:
            continue
    return candidates


def first_h1_after(h1_timestamps: list[pd.Timestamp], availability: pd.Timestamp) -> pd.Timestamp | None:
    # h1_timestamps is sorted and represents actual H1 decision timestamps.
    pos = int(pd.Series(h1_timestamps).searchsorted(availability, side="right"))
    return None if pos >= len(h1_timestamps) else h1_timestamps[pos]


def normalize_candidate(candidate: dict, rule: str, h1_timestamps: list[pd.Timestamp]) -> pd.DataFrame:
    df = pd.read_csv(candidate["path"], low_memory=False)
    id_field = candidate["id_field"]
    avail_field = candidate["availability_field"]
    out = df.copy()
    out["source_rule_id"] = out[id_field].astype("string")
    rule_mask = out["source_rule_id"].astype("string").fillna("").map(
        lambda value: rule in {x.strip().upper() for x in value.split("|") if x.strip()}
    )
    out = out.loc[rule_mask].copy()

    # Only frozen confirmations are admitted. Candidates are never promoted here.
    if "confirmation" not in out.columns:
        raise SystemExit(f"BLOCKED_0006_0007_MISSING_CONFIRMATION_FIELD:{rule}:{candidate['path']}")
    confirmation = out["confirmation"].astype("string").str.strip().str.lower()
    out = out.loc[confirmation.isin({"true", "1", "yes"})].copy()
    if out.empty:
        return out

    out["availability_timestamp"] = parse_ts(out[avail_field])
    if out["availability_timestamp"].isna().any():
        raise SystemExit(f"BLOCKED_0006_0007_MISSING_CONFIRMATION_AVAILABILITY:{rule}:{candidate['path']}")

    if candidate["has_timestamp"]:
        out["timestamp"] = parse_ts(out["timestamp"])
    else:
        out["third_touch_timestamp"] = parse_ts(out["third_touch_timestamp"])
        out["reaction_timestamp"] = parse_ts(out["reaction_timestamp"])
        # Timing bridge: first real H1 decision bar strictly after evidence availability.
        out["timestamp"] = out["availability_timestamp"].map(
            lambda ts: first_h1_after(h1_timestamps, ts) if pd.notna(ts) else pd.NaT
        )

    out = out.loc[
        out["timestamp"].notna()
        & out["availability_timestamp"].notna()
        & (out["timestamp"] >= pd.Timestamp("2016-01-01", tz="UTC"))
        & (out["timestamp"] < pd.Timestamp("2025-01-01", tz="UTC"))
        & (out["availability_timestamp"] >= pd.Timestamp("2016-01-01", tz="UTC"))
        & (out["availability_timestamp"] < pd.Timestamp("2025-01-01", tz="UTC"))
        & (out["availability_timestamp"] < out["timestamp"])
    ].copy()
    out["direction"] = "BULLISH" if rule == "MURPHY_0006" else "BEARISH"
    out["status"] = "PASS"
    out["strict_asof_status"] = "PASS"
    out["timing_bridge"] = "first_H1_decision_timestamp_strictly_after_confirmation_available_timestamp"
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, type=Path)
    ap.add_argument("--archive-root", required=True, type=Path)
    ap.add_argument("--h1", required=True, type=Path)
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

    h1 = pd.read_csv(args.h1, low_memory=False)
    if "timestamp" not in h1.columns:
        raise SystemExit("BLOCKED_H1_MISSING_TIMESTAMP")
    h1_ts = parse_ts(h1["timestamp"]).dropna()
    h1_ts = sorted(set(h1_ts[(h1_ts >= pd.Timestamp("2016-01-01", tz="UTC")) & (h1_ts < pd.Timestamp("2025-01-01", tz="UTC"))].tolist()))
    if not h1_ts:
        raise SystemExit("BLOCKED_H1_EMPTY_2016_2024")

    existing = {x.strip().upper() for v in base["source_rule_id"].dropna() for x in str(v).split("|") if x.strip()}
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
        part = normalize_candidate(c, rule, h1_ts)
        if part.empty:
            raise SystemExit(f"BLOCKED_EMPTY_NORMALIZED_RULE:{rule}:{c['path']}")
        if part["timestamp"].duplicated().any():
            dup_ts = int(part["timestamp"].duplicated().sum())
            raise SystemExit(f"BLOCKED_DUPLICATE_H1_DECISION_TIMESTAMP:{rule}:{dup_ts}")
        ids = normalized_ids(part["source_rule_id"])
        if rule not in ids:
            raise SystemExit(f"BLOCKED_NORMALIZATION_LOST_RULE:{rule}:{c['path']}")
        if not ((part["availability_timestamp"] < part["timestamp"]).all()):
            raise SystemExit(f"BLOCKED_POST_NORMALIZATION_STRICT_ASOF:{rule}:{c['path']}")
        parts.append(part)
        provenance.append({
            "rule": rule,
            "path": str(c["path"]),
            "source_shape": "canonical_timestamp" if c["has_timestamp"] else "frozen_confirmation_artifact",
            "rows_before_window": c["rows"],
            "confirmed_rows_after_strict_asof_bridge": int(len(part)),
            "id_field": c["id_field"],
            "availability_field": c["availability_field"],
            "timing_bridge": "first_H1_decision_timestamp_strictly_after_confirmation_available_timestamp",
        })

    columns = sorted(set().union(*(set(p.columns) for p in parts)))
    merged = pd.concat([p.reindex(columns=columns) for p in parts], ignore_index=True, sort=False)
    merged["timestamp"] = parse_ts(merged["timestamp"])
    merged["availability_timestamp"] = parse_ts(merged["availability_timestamp"])
    merged = merged.sort_values(["timestamp", "source_rule_id"], kind="stable").reset_index(drop=True)
    merged.to_csv(args.output, index=False)

    report = {
        "status": "PASS",
        "base_rows": int(len(base)),
        "merged_rows": int(len(merged)),
        "added_rows": int(len(merged) - len(base)),
        "rules_added": sorted(RULES),
        "provenance": provenance,
        "strict_operator": "confirmation_available_timestamp < H1_decision_timestamp",
        "timing_bridge": "first_H1_decision_timestamp_strictly_after_confirmation_available_timestamp",
        "bridge_is_timing_only": True,
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
