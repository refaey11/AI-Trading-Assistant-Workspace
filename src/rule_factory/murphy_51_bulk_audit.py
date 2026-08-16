"""Bulk Murphy-51 triage for Rule Factory V1.

This module is deliberately conservative. It does not infer missing operators,
change canonical semantics, or promote a rule to frozen. It only classifies the
existing project state and creates a work queue for the smallest missing piece.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List

FROZEN_IDS = {
    "0003", "0004", "0006", "0007", "0008",
    "0021", "0022", "0023", "0025", "0026", "0028", "0029",
}


def classify_rule(rule: Dict[str, Any]) -> str:
    """Classify without changing source meaning."""
    rule_id = str(rule["rule_id"]).zfill(4)
    if rule_id in FROZEN_IDS:
        return "FROZEN"

    status = str(rule.get("source_status", "")).upper()
    if status in {"READY_FOR_BACKTEST", "EXECUTABLE"} and rule.get("all_gates_passed") is True:
        return "EXECUTABLE"
    if status in {"NOT_EVALUABLE", "BLOCKED_NEEDS_RULE_DEFINITION"}:
        return "NOT_EVALUABLE"
    return "PARTIAL_NEED_SOLUTION"


def build_work_queue(rules: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    queue: List[Dict[str, Any]] = []
    for rule in rules:
        classification = classify_rule(rule)
        if classification == "FROZEN":
            continue
        queue.append({
            "rule_id": str(rule["rule_id"]).zfill(4),
            "classification": classification,
            "missing": rule.get("missing"),
            "next_action": (
                "compatibility_audit -> existing primitive check -> smallest missing implementation"
                if classification == "PARTIAL_NEED_SOLUTION"
                else "source/provenance/operator investigation; remain NOT_EVALUABLE if unsupported"
            ),
        })
    return queue


def summarize(rules: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    rows = list(rules)
    counts = Counter(classify_rule(r) for r in rows)
    return {
        "total": len(rows),
        "frozen": counts.get("FROZEN", 0),
        "executable": counts.get("EXECUTABLE", 0),
        "partial_need_solution": counts.get("PARTIAL_NEED_SOLUTION", 0),
        "not_evaluable": counts.get("NOT_EVALUABLE", 0),
    }


def audit_report(rules: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    rows = list(rules)
    return {
        "summary": summarize(rows),
        "work_queue": build_work_queue(rows),
        "governance": {
            "frozen_read_only": True,
            "invented_thresholds": False,
            "invented_operators": False,
            "use_2025_for_tuning": False,
            "similarity_is_decision_maker": False,
            "canonical_meaning_mutation": False,
        },
    }
