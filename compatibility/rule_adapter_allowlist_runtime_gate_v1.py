"""Runtime gate enforcing the frozen Decision Brain rule allowlist.

This module does not implement or rewrite any book rule. It only checks that an
already-produced rule result is sourced from the frozen 78-rule allowlist before
it can be normalized for downstream Decision Brain evaluation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

ALLOWLIST_PATH = Path("governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json")


def load_allowlist() -> set[str]:
    data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    verified = data.get("verified_runtime", {})
    return set(verified.get("MURPHY", [])) | set(verified.get("NISON", []))


def gate_rule_result(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Return an eligibility decision; deny-by-default for unknown/unapproved IDs."""
    rule_id = raw.get("source_rule_id")
    allowed = load_allowlist()
    if not isinstance(rule_id, str) or rule_id not in allowed:
        return {
            "eligible": False,
            "status": "REJECT",
            "source_rule_id": rule_id,
            "reason": "RULE_NOT_IN_FROZEN_ALLOWLIST",
        }
    return {
        "eligible": True,
        "status": "PASS",
        "source_rule_id": rule_id,
        "reason": "RULE_IN_FROZEN_ALLOWLIST",
    }
