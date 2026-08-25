from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

import pandas as pd

ALLOWLIST = Path("governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json")
MURPHY_ENTRYPOINT = Path("MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py")


def registered_rule_ids(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    ids: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            if isinstance(node.left, ast.Name) and node.left.id == "rule_id":
                for comp in node.comparators:
                    if isinstance(comp, ast.Constant) and isinstance(comp.value, str):
                        if comp.value.startswith("MURPHY_"):
                            ids.add(comp.value)
        if isinstance(node, ast.Set):
            for elt in node.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str) and elt.value.startswith("MURPHY_"):
                    ids.add(elt.value)
    return ids


def audit(allowlist_path: Path, murphy_entrypoint: Path, murphy_candidate: Path, nison_full: Path, decision_events: Path | None) -> dict:
    policy = json.loads(allowlist_path.read_text(encoding="utf-8"))
    allowed_m = set(policy["verified_runtime"]["MURPHY"])
    allowed_n = set(policy["verified_runtime"]["NISON"])

    m = pd.read_csv(murphy_candidate)
    n = pd.read_csv(nison_full)
    m_ids = set(m["source_rule_id"].dropna().astype(str)) if "source_rule_id" in m.columns else set()
    n_ids = set(n["rule_id"].dropna().astype(str)) if "rule_id" in n.columns else set()

    registered = registered_rule_ids(murphy_entrypoint)
    observed_decision_ids: set[str] = set()
    event_status_counts = {}
    if decision_events and decision_events.exists():
        e = pd.read_csv(decision_events)
        if "source_rule_ids" in e.columns:
            for raw in e["source_rule_ids"].dropna().astype(str):
                try:
                    observed_decision_ids.update(json.loads(raw))
                except Exception:
                    pass
        if "status" in e.columns:
            event_status_counts = e["status"].value_counts().to_dict()

    unknown_m = sorted(m_ids - allowed_m)
    unknown_n = sorted(n_ids - allowed_n)
    missing_m_from_candidate = sorted(allowed_m - m_ids)
    missing_m_from_entrypoint = sorted(allowed_m - registered)

    report = {
        "status": "READY_ONLY_IF_ALL_REQUIRED_EVIDENCE_IS_WIRED",
        "allowlist": {"murphy": len(allowed_m), "nison": len(allowed_n), "total": len(allowed_m | allowed_n)},
        "candidate_stream": {"murphy_rule_ids_observed": sorted(m_ids), "murphy_rule_count_observed": len(m_ids), "unknown_rule_ids": unknown_m},
        "nison_production": {"rule_ids_observed": sorted(n_ids), "rule_count_observed": len(n_ids), "unknown_rule_ids": unknown_n},
        "murphy_runtime_entrypoint": {"registered_rule_count": len(registered), "registered_rule_ids": sorted(registered), "allowlisted_but_not_registered": missing_m_from_entrypoint},
        "decision_events": {"observed_source_rule_ids": sorted(observed_decision_ids), "status_counts": event_status_counts},
        "gates": {
            "all_34_allowlisted_murphy_rules_in_candidate_stream": len(m_ids) == len(allowed_m) and not unknown_m,
            "all_44_nison_rule_ids_in_production": len(n_ids) == len(allowed_n) and not unknown_n,
            "no_synthetic_rule_ids": "NISON_NONE" not in observed_decision_ids,
            "runtime_entrypoint_matches_allowlisted_murphy_scope": allowed_m.issubset(registered),
        },
        "required_action": "Do not calculate official P&L until the 34-rule Murphy evidence fan-in and per-rule provenance are wired. Missing/deferred rules must remain NOT_EVALUABLE; no synthetic substitute is permitted.",
        "oos_tuning": False,
    }
    report["blocking_gates"] = [k for k, ok in report["gates"].items() if not ok]
    return report


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--murphy-candidate", required=True, type=Path)
    p.add_argument("--nison-full", required=True, type=Path)
    p.add_argument("--decision-events", type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--allowlist", type=Path, default=ALLOWLIST)
    p.add_argument("--murphy-entrypoint", type=Path, default=MURPHY_ENTRYPOINT)
    a = p.parse_args()

    report = audit(a.allowlist, a.murphy_entrypoint, a.murphy_candidate, a.nison_full, a.decision_events)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))

    # This is deliberately fail-closed: a passing pipeline must not imply that
    # a partial Murphy evidence stream represents the full 34-rule brain.
    return 0 if not report["blocking_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
