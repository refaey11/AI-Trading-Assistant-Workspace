#!/usr/bin/env python3
"""Scan the extracted Nison source package for rule-level provenance.

This is a provenance/source-mapping tool only. It does not infer semantics,
thresholds, evaluators, scoring, direction, or freeze status.
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "nison_ci_source"
OUT = ROOT / "nison_batch" / "artifacts"
REGISTRY = SRC / "03_Rule_Registry" / "INTEGRATED_RULE_REGISTRY_V1.json"

TEXT_EXTS = {".md", ".json", ".txt", ".csv", ".py", ".yaml", ".yml", ".xml", ".html"}

def text_files():
    for p in SRC.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXTS:
            yield p

def nison_confirmation_rules(data):
    rules = data if isinstance(data, list) else data.get("rules", [])
    selected = []
    for r in rules:
        source = str(r.get("source", r.get("primary_source", ""))).lower()
        role = str(r.get("integration_role", "")).lower()
        if "nison" in source and role == "confirmation":
            selected.append(r)
    return selected

def main():
    if not REGISTRY.exists():
        raise SystemExit("Missing extracted Nison registry")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rules = nison_confirmation_rules(data)
    if len(rules) != 44:
        raise SystemExit(f"FAIL: expected exactly 44 Nison confirmation rules, found {len(rules)}")

    files = list(text_files())
    cache = {}
    for p in files:
        try:
            cache[p] = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            cache[p] = ""

    rows = []
    for r in rules:
        rid = str(r.get("rule_id", r.get("id", "UNKNOWN")))
        name = str(r.get("name", r.get("rule_name", "")))
        terms = [rid, name]
        hits = []
        for p, txt in cache.items():
            if any(t and re.search(re.escape(t), txt, re.I) for t in terms):
                hits.append(str(p.relative_to(SRC)))
        rows.append({
            "rule_id": rid,
            "name": name,
            "source_reference_files": sorted(set(hits)),
            "source_reference_count": len(set(hits)),
            "status": "SOURCE_REFERENCED" if hits else "NO_SOURCE_REFERENCE_FOUND",
            "semantic_status": "UNASSESSED",
            "evaluator_status": "UNASSESSED",
            "qa_status": "UNASSESSED",
            "freeze_status": "NOT_FROZEN",
        })

    report = {
        "rule_count": len(rows),
        "expected_rule_count": 44,
        "count_check": len(rows) == 44,
        "registry_total_rule_count": len(data) if isinstance(data, list) else len(data.get("rules", [])),
        "source_file_count": len(files),
        "rules": rows,
        "governance": {
            "confirmation_only": True,
            "no_invented_semantics": True,
            "no_invented_thresholds": True,
            "no_invented_lookbacks": True,
            "no_scoring": True,
            "no_direction_generation": True,
            "2025_oos": True,
            "auto_freeze": False,
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "nison_44_source_map.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "rule_count": len(rows),
        "count_check": len(rows) == 44,
        "registry_total_rule_count": report["registry_total_rule_count"],
        "source_file_count": len(files),
        "source_referenced": sum(x["source_reference_count"] > 0 for x in rows),
        "no_source_reference": sum(x["source_reference_count"] == 0 for x in rows),
    }, indent=2))

if __name__ == "__main__":
    main()
