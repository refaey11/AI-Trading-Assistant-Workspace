#!/usr/bin/env python3
"""Reconcile two Murphy evidence CSVs against the canonical 34-rule allowlist.

The gate is intentionally source-agnostic: it compares normalized rule coverage,
unknown IDs, duplicate timestamp/rule pairs, and date bounds without assuming
that row ordering or producer-specific metadata is identical.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def load_allowlist(path: Path) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    ids = data.get("murphy_rule_ids") or data.get("murphy_rules")
    if isinstance(ids, dict):
        ids = ids.keys()
    if not ids:
        ids = [x["id"] for x in data.get("rules", []) if str(x.get("id", "")).startswith("MURPHY_")]
    return {str(x) for x in ids}


def inspect_csv(path: Path, expected: set[str]) -> dict:
    rows = 0
    timestamps: list[str] = []
    observed: set[str] = set()
    unknown: set[str] = set()
    pairs: list[tuple[str, str]] = []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or "timestamp" not in reader.fieldnames:
            raise ValueError(f"{path}: missing timestamp column")
        rule_field = next((x for x in ("source_rule_id", "rule_id", "source_rule_ids") if x in reader.fieldnames), None)
        if not rule_field:
            raise ValueError(f"{path}: missing Murphy rule-id column")
        for row in reader:
            rows += 1
            ts = (row.get("timestamp") or "").strip()
            if ts:
                timestamps.append(ts)
            ids = [x.strip() for x in (row.get(rule_field) or "").split("|") if x.strip()]
            for rid in ids:
                observed.add(rid)
                pairs.append((ts, rid))
                if rid not in expected:
                    unknown.add(rid)
    duplicate_pairs = sorted([f"{ts}|{rid}" for (ts, rid), n in Counter(pairs).items() if n > 1])
    missing = sorted(expected - observed)
    return {
        "path": str(path),
        "row_count": rows,
        "observed_rule_count": len(observed),
        "missing_rule_ids": missing,
        "unknown_rule_ids": sorted(unknown),
        "duplicate_timestamp_rule_pairs": duplicate_pairs,
        "first_timestamp": min(timestamps) if timestamps else None,
        "last_timestamp": max(timestamps) if timestamps else None,
        "complete": not missing and not unknown and not duplicate_pairs,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--github-source", required=True, type=Path)
    ap.add_argument("--dropbox-source", required=True, type=Path)
    ap.add_argument("--allowlist", required=True, type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    expected = load_allowlist(args.allowlist)
    if len(expected) != 34:
        raise SystemExit(f"canonical Murphy allowlist must contain 34 IDs, got {len(expected)}")
    github = inspect_csv(args.github_source, expected)
    dropbox = inspect_csv(args.dropbox_source, expected)
    result = {
        "expected_rule_count": 34,
        "github": github,
        "dropbox": dropbox,
        "coverage_match": set(github["missing_rule_ids"]) == set(dropbox["missing_rule_ids"]) and set(github["unknown_rule_ids"]) == set(dropbox["unknown_rule_ids"]),
        "complete": github["complete"] and dropbox["complete"],
    }
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["complete"] and result["coverage_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
