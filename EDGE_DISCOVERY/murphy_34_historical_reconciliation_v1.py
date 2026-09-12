#!/usr/bin/env python3
"""Reconcile the frozen Murphy runtime set against historical evidence.

Audit-only: no synthetic evidence, no rule-semantic changes, no signal generation.
The governed runtime set is read directly from the frozen allowlist so this audit
cannot silently drift to a hand-maintained list.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from collections import defaultdict

RULE_RE = re.compile(r"MURPHY_(\d{4})")
TEXT_EXTS = {".csv", ".json", ".jsonl", ".txt", ".md", ".sql", ".yaml", ".yml", ".py"}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}


def iter_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TEXT_EXTS:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def classify(path: Path) -> str:
    s = path.as_posix().lower()
    if any(x in s for x in ("evidence", "historical", "fan", "producer", "event", "backtest")):
        return "historical_or_pipeline"
    if any(x in s for x in ("rule", "allowlist", "registry", "adapter", "murphy")):
        return "runtime_or_governance"
    return "other"


def load_allowlist(path: Path) -> list[str]:
    outer = json.loads(path.read_text(encoding="utf-8"))
    # Current allowlist is a JSON document whose content field contains the
    # canonical JSON payload. Support both forms without weakening validation.
    payload = json.loads(outer["content"]) if isinstance(outer.get("content"), str) else outer
    ids = payload.get("verified_runtime", {}).get("MURPHY", [])
    expected = sorted(set(ids))
    if len(expected) != 34 or len(set(expected)) != 34:
        raise SystemExit(f"FAIL: frozen allowlist must expose exactly 34 unique Murphy runtime IDs; got {len(expected)}")
    return expected


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--allowlist", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("EDGE_DISCOVERY/murphy_34_reconciliation_v1.json"))
    args = ap.parse_args()
    expected = load_allowlist(args.allowlist)

    hits = defaultdict(lambda: {"runtime_or_governance": [], "historical_or_pipeline": [], "other": []})
    for p in iter_files(args.root):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for n in set(RULE_RE.findall(text)):
            rid = f"MURPHY_{n}"
            if rid in expected:
                hits[rid][classify(p)].append(str(p.relative_to(args.root)))

    rows = []
    for rid in expected:
        h = hits[rid]
        historical = sorted(set(h["historical_or_pipeline"]))
        runtime = sorted(set(h["runtime_or_governance"]))
        other = sorted(set(h["other"]))
        status = "HISTORICAL_REFERENCED" if historical else "NOT_EVALUABLE_CANDIDATE"
        rows.append({"rule_id": rid, "status": status,
                     "historical_refs": historical, "runtime_refs": runtime, "other_refs": other})

    doc = {
        "schema": "MURPHY_34_HISTORICAL_RECONCILIATION_V1",
        "mode": "AUDIT_ONLY",
        "governance": {"development_period": "2016-2024", "oos_locked": "2025",
                       "no_synthetic_evidence": True, "no_semantic_changes": True},
        "expected_count": 34,
        "rows": rows,
        "summary": {
            "historical_referenced": sum(r["status"] == "HISTORICAL_REFERENCED" for r in rows),
            "not_evaluable_candidate": sum(r["status"] == "NOT_EVALUABLE_CANDIDATE" for r in rows),
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(doc["summary"], sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
