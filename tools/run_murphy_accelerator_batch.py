#!/usr/bin/env python3
"""Execute available shared-accelerator checks for the Murphy 39 batch.

Fail-closed by design: missing accelerator-specific checks become NOT_EVALUABLE;
no semantics, thresholds, box sizes, scores, tuning, or freeze decisions are
invented here. The runner is an execution/orchestration layer, not a rule
semantic authority.
"""
from __future__ import annotations

import csv
import json
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "project_state" / "MURPHY_39_BATCH_AUDIT_QUEUE_V1.csv"
MANIFEST = ROOT / "project_state" / "MURPHY_HYBRID_39_FACTORY_MANIFEST_V1.csv"
OUT_JSON = ROOT / "project_state" / "MURPHY_39_ACCELERATOR_BATCH_RESULT_V1.json"
OUT_MD = ROOT / "project_state" / "MURPHY_39_ACCELERATOR_BATCH_RESULT_V1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    queue = read_csv(QUEUE)
    manifest = {r["rule_id"]: r for r in read_csv(MANIFEST)}
    groups: dict[str, list[str]] = defaultdict(list)
    errors: list[str] = []

    if len(queue) != 39:
        errors.append(f"queue cardinality={len(queue)}; expected 39")

    for row in queue:
        rid = row["rule_id"]
        m = manifest.get(rid)
        if not m:
            errors.append(f"missing manifest row: {rid}")
            continue
        groups[m["shared_accelerator"]].append(rid)

    results = []
    # Existing concrete test entrypoints. Other accelerators remain
    # NOT_EVALUABLE until a source-backed test entrypoint exists.
    test_map = {
        "EXISTING_PNF_WORK": ["tests/murphy_0030"],
    }

    for accelerator, rule_ids in sorted(groups.items()):
        paths = test_map.get(accelerator, [])
        existing = [ROOT / p for p in paths if (ROOT / p).exists()]
        if not existing:
            results.append({
                "accelerator": accelerator,
                "rules": sorted(rule_ids),
                "status": "NOT_EVALUABLE",
                "reason": "No accelerator-specific executable test entrypoint is present; no semantics were invented.",
            })
            continue

        cmd = ["python", "-m", "pytest", "-q", *[str(p.relative_to(ROOT)) for p in existing]]
        proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        results.append({
            "accelerator": accelerator,
            "rules": sorted(rule_ids),
            "status": "PASS" if proc.returncode == 0 else "BLOCKED",
            "command": cmd,
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        })

    result = {
        "status": "BLOCKED" if errors or any(r["status"] == "BLOCKED" for r in results) else "PASS",
        "rule_count": len(queue),
        "accelerator_count": len(results),
        "errors": errors,
        "results": results,
        "governance": {
            "no_auto_freeze": True,
            "no_invented_semantics": True,
            "2025_oos": True,
            "not_evaluable_on_missing_entrypoint": True,
        },
    }
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Murphy 39 Accelerator Batch Result V1", "",
        f"Status: **{result['status']}**", f"Rules: **{len(queue)}**", "",
        "Missing accelerator entrypoints are NOT_EVALUABLE; this runner never invents semantics or freezes rules.", "",
    ]
    for r in results:
        lines.append(f"- **{r['accelerator']}** — {r['status']} — {len(r['rules'])} rules")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"MURPHY_39_ACCELERATOR_BATCH status={result['status']} rules={len(queue)} accelerators={len(results)}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
