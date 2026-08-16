#!/usr/bin/env python3
"""Deterministic batch planner for the Murphy 39-rule Hybrid Factory.

This tool accelerates mechanics only. It never invents semantics, thresholds,
box sizes, scores, or freeze decisions. It reads the canonical queue and
factory manifest, validates their one-to-one coverage, and emits a machine-
readable batch audit matrix plus a human-readable summary.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "project_state" / "MURPHY_39_BATCH_AUDIT_QUEUE_V1.csv"
MANIFEST = ROOT / "project_state" / "MURPHY_HYBRID_39_FACTORY_MANIFEST_V1.csv"
OUT_JSON = ROOT / "project_state" / "MURPHY_39_FACTORY_BATCH_RESULT_V1.json"
OUT_MD = ROOT / "project_state" / "MURPHY_39_FACTORY_BATCH_RESULT_V1.md"

FROZEN = {
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007",
    "MURPHY_0008", "MURPHY_0021", "MURPHY_0022", "MURPHY_0023",
    "MURPHY_0025", "MURPHY_0026", "MURPHY_0028", "MURPHY_0029",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify(row: dict[str, str], manifest: dict[str, str]) -> str:
    status = row["current_status"]
    if status == "NOT_EVALUABLE":
        return "NOT_EVALUABLE"
    if status in {"REVIEW", "PARTIAL"}:
        return "AUDIT_READY"
    if status == "UNBLOCKED":
        return "AUDIT_READY"
    return "REVIEW_REQUIRED"


def main() -> int:
    queue = read_csv(QUEUE)
    manifest_rows = read_csv(MANIFEST)
    manifest = {r["rule_id"]: r for r in manifest_rows}

    ids = [r["rule_id"] for r in queue]
    errors: list[str] = []
    if len(queue) != 39:
        errors.append(f"queue cardinality={len(queue)}; expected 39")
    if len(ids) != len(set(ids)):
        errors.append("duplicate rule_id in queue")
    if set(ids) & FROZEN:
        errors.append("frozen rule re-entered queue: " + ",".join(sorted(set(ids) & FROZEN)))
    if any(r.get("protected") != "NO" for r in queue):
        errors.append("queue contains protected != NO")
    missing_manifest = sorted(set(ids) - set(manifest))
    extra_manifest = sorted(set(manifest) - set(ids))
    if missing_manifest:
        errors.append("missing manifest rows: " + ",".join(missing_manifest))
    if extra_manifest:
        errors.append("manifest has non-queue rows: " + ",".join(extra_manifest))
    if any("2025" in json.dumps(r) for r in queue):
        errors.append("2025 value detected in queue")

    matrix = []
    for row in queue:
        mid = row["rule_id"]
        m = manifest.get(mid, {})
        matrix.append({
            "rule_id": mid,
            "current_status": row["current_status"],
            "work_lane": row["work_lane"],
            "shared_accelerator": row["shared_accelerator"],
            "next_gate": row["next_gate"],
            "clause_strategy": m.get("clause_strategy", "MISSING"),
            "freeze_policy": m.get("freeze_policy", "MISSING"),
            "batch_class": classify(row, m),
        })

    counts: dict[str, int] = {}
    for item in matrix:
        counts[item["batch_class"]] = counts.get(item["batch_class"], 0) + 1

    result = {
        "status": "PASS" if not errors else "BLOCKED",
        "rule_count": len(matrix),
        "counts": counts,
        "governance": {
            "no_auto_freeze": True,
            "no_invented_semantics": True,
            "2025_oos": True,
            "frozen_rules_excluded": True,
        },
        "errors": errors,
        "matrix": matrix,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Murphy 39 Factory Batch Result V1",
        "",
        f"Status: **{result['status']}**",
        f"Rules: **{len(matrix)}**",
        "",
        "This is a mechanics/governance batch result. It does not certify semantic compatibility or freeze any rule.",
        "",
        "## Batch classes",
    ]
    for k in sorted(counts):
        lines.append(f"- {k}: {counts[k]}")
    if errors:
        lines += ["", "## Errors"] + [f"- {e}" for e in errors]
    lines += ["", "## Next gates"]
    for item in matrix:
        lines.append(f"- {item['rule_id']}: {item['next_gate']} ({item['batch_class']})")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"MURPHY_39_FACTORY_BATCH status={result['status']} rules={len(matrix)}")
    for k in sorted(counts):
        print(f"{k}={counts[k]}")
    for e in errors:
        print(f"ERROR: {e}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
