#!/usr/bin/env python3
"""Emit a deterministic, evidence-first 51-rule coverage report.

This report is intentionally conservative: absence of a recognized gate is not
converted into a failure, and a status claim is never treated as proof of the
gate that would normally justify that status. The report is a coverage/index
layer for the reducer, not a semantic inference engine.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from tools.murphy_evidence_collector import collect_repository_surface
from tools.murphy_evidence_chain import EvidenceRecord, reduce_state
from tools.murphy_state_verifier import State

RULE_IDS = tuple(f"{n:04d}" for n in range(1, 52))


def _group(records: Iterable[EvidenceRecord]) -> dict[str, list[EvidenceRecord]]:
    grouped: dict[str, list[EvidenceRecord]] = defaultdict(list)
    for record in records:
        if record.rule_id in RULE_IDS:
            grouped[record.rule_id].append(record)
    return grouped


def build_report(records: Iterable[EvidenceRecord]) -> dict:
    grouped = _group(records)
    rows = []
    for rule_id in RULE_IDS:
        items = sorted(grouped.get(rule_id, []), key=lambda r: (r.timestamp, r.commit_sha, r.evidence_type))
        state, reasons = reduce_state(items)
        claims = Counter(r.status_claim.upper() for r in items if r.status_claim)
        rows.append({
            "rule_id": rule_id,
            "state": state.value,
            "evidence_count": len(items),
            "git_commit_count": len({r.commit_sha for r in items}),
            "artifact_count": len({r.artifact_path for r in items if r.artifact_path}),
            "status_claims": dict(sorted(claims.items())),
            "latest_evidence": items[-1].timestamp.isoformat() if items else None,
            "latest_commit": items[-1].commit_sha if items else None,
            "reasons": list(reasons),
        })

    state_counts = Counter(row["state"] for row in rows)
    return {
        "schema": "murphy-51-evidence-coverage-v1",
        "rule_count": len(RULE_IDS),
        "state_counts": dict(sorted(state_counts.items())),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path)
    parser.add_argument("--max-commits", type=int, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    records = collect_repository_surface(args.repo, max_commits=args.max_commits)
    report = build_report(records)
    payload = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
