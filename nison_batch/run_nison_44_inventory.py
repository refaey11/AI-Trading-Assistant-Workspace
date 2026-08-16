#!/usr/bin/env python3
"""Source-bounded Nison 44-rule batch inventory.

This runner does not invent evaluators or semantics. It inventories the Nison
registry and emits an auditable classification scaffold for the 44 Nison
confirmation rules. Unsupported/ambiguous clauses remain NOT_EVALUABLE.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "nison_batch" / "artifacts"
REGISTRY_CANDIDATES = [
    ROOT / "nison_ci_source/03_Rule_Registry/INTEGRATED_RULE_REGISTRY_V1.json",
    ROOT / "03_Rule_Registry/INTEGRATED_RULE_REGISTRY_V1.json",
]

def load_registry():
    for p in REGISTRY_CANDIDATES:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8")), p
    raise FileNotFoundError("Nison registry is not extracted; source verification must run first")

def main():
    registry, source = load_registry()
    if isinstance(registry, list):
        rules = registry
    elif isinstance(registry, dict):
        rules = registry.get("rules", [])
    else:
        raise TypeError(f"Unsupported registry JSON type: {type(registry).__name__}")
    nison = []
    for r in rules:
        source_name = str(r.get("source", r.get("primary_source", ""))).lower()
        role = str(r.get("integration_role", "")).lower()
        if "nison" in source_name and role == "confirmation":
            nison.append(r)
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for r in nison:
        rid = r.get("rule_id", r.get("id", "UNKNOWN"))
        rows.append({
            "rule_id": rid,
            "source": r.get("source", r.get("primary_source")),
            "integration_role": r.get("integration_role"),
            "status": "PENDING_COMPATIBILITY_AUDIT",
            "evaluator": None,
            "decision": "NOT_EVALUABLE",
            "reason": "No evaluator is assigned by this inventory runner; operationalization requires a compatible existing primitive/adapter.",
            "governance": {
                "confirmation_only": True,
                "no_invented_thresholds": True,
                "no_invented_lookbacks": True,
                "no_scoring": True,
                "no_direction_generation": True,
                "no_2025_tuning": True,
                "no_auto_freeze": True,
            },
        })
    report = {
        "source_registry": str(source),
        "nison_rule_count": len(rows),
        "expected_nison_rule_count": 44,
        "count_check": len(rows) == 44,
        "rules": rows,
    }
    (OUT / "nison_44_batch_inventory.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"nison_rule_count": len(rows), "count_check": len(rows) == 44, "output": str(OUT / 'nison_44_batch_inventory.json')}, indent=2))
    if len(rows) != 44:
        raise SystemExit("FAIL: expected exactly 44 Nison confirmation rules")

if __name__ == "__main__":
    main()
