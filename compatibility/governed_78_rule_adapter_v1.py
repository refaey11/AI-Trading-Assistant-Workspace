"""Governed runtime adapter for the frozen 34 Murphy + 44 Nison envelope.

This is a transport/validation boundary, not a strategy. It preserves every
real rule row, rejects unknown or missing rule IDs, and returns an immutable-ish
package plus a deterministic receipt for downstream provenance.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

ALLOWLIST_PATH = Path("governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json")
SCHEMA_VERSION = "GOVERNED_78_RULE_ADAPTER_V1"
EXPECTED_COUNTS = {"MURPHY": 34, "NISON": 44}


@dataclass(frozen=True)
class RuleAdapterResult:
    status: str
    package: Mapping[str, Any]
    reason: str | None = None


def _allowed_ids() -> dict[str, set[str]]:
    data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    runtime = data["verified_runtime"]
    return {
        "MURPHY": set(runtime["MURPHY"]),
        "NISON": set(runtime["NISON"]),
    }


def _norm_rule_id(row: Mapping[str, Any]) -> str:
    return str(row.get("source_rule_id") or row.get("rule_id") or "").strip()


def _canonical_rows(rows: Any) -> list[dict[str, Any]]:
    if isinstance(rows, Mapping):
        rows = list(rows.values())
    if not isinstance(rows, list):
        return []
    out: list[dict[str, Any]] = []
    for row in rows:
        if isinstance(row, Mapping):
            item = dict(row)
            rid = _norm_rule_id(item)
            if rid:
                item["source_rule_id"] = rid
                out.append(item)
    return sorted(out, key=lambda r: (str(r.get("source_rule_id")), json.dumps(r, sort_keys=True, default=str)))


def _receipt_payload(murphy_rows: list[dict[str, Any]], nison_rows: list[dict[str, Any]], provenance: Mapping[str, Any]) -> bytes:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "murphy_rule_ids": sorted({_norm_rule_id(r) for r in murphy_rows}),
        "nison_rule_ids": sorted({_norm_rule_id(r) for r in nison_rows}),
        "murphy_rows": murphy_rows,
        "nison_rows": nison_rows,
        "provenance": dict(provenance),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def build_governed_78_package(
    *,
    query_as_of: Any,
    murphy_rows: Any,
    nison_rows: Any,
    mode: str,
    provenance: Mapping[str, Any] | None = None,
) -> RuleAdapterResult:
    """Validate and package the complete frozen 78-rule evidence for one timestamp."""
    prov = dict(provenance or {})
    if mode not in {"development", "oos_evaluation"}:
        return RuleAdapterResult("NOT_EVALUABLE", {}, "INVALID_MODE")

    m_rows = _canonical_rows(murphy_rows)
    n_rows = _canonical_rows(nison_rows)
    allowed = _allowed_ids()

    if not m_rows or not n_rows:
        return RuleAdapterResult("NOT_EVALUABLE", {}, "MISSING_FULL_RULE_EVIDENCE")

    m_ids = [_norm_rule_id(r) for r in m_rows]
    n_ids = [_norm_rule_id(r) for r in n_rows]
    m_set, n_set = set(m_ids), set(n_ids)

    unknown_m = sorted(m_set - allowed["MURPHY"])
    unknown_n = sorted(n_set - allowed["NISON"])
    if unknown_m or unknown_n:
        return RuleAdapterResult(
            "NOT_EVALUABLE", {}, f"UNKNOWN_RULE_IDS:MURPHY={unknown_m};NISON={unknown_n}"
        )

    if len(m_set) != EXPECTED_COUNTS["MURPHY"]:
        return RuleAdapterResult("NOT_EVALUABLE", {}, f"MURPHY_RULE_COUNT_{len(m_set)}_EXPECTED_34")
    if len(n_set) != EXPECTED_COUNTS["NISON"]:
        return RuleAdapterResult("NOT_EVALUABLE", {}, f"NISON_RULE_COUNT_{len(n_set)}_EXPECTED_44")

    if len(m_rows) != len(m_set) or len(n_rows) != len(n_set):
        return RuleAdapterResult("NOT_EVALUABLE", {}, "DUPLICATE_RULE_ROWS")

    receipt = sha256(_receipt_payload(m_rows, n_rows, prov)).hexdigest()
    package = {
        "schema_version": SCHEMA_VERSION,
        "query_as_of": query_as_of,
        "mode": mode,
        "murphy": {
            "rule_count": len(m_set),
            "rows": m_rows,
            "role": "TECHNICAL_CONTEXT",
        },
        "nison": {
            "rule_count": len(n_set),
            "rows": n_rows,
            "role": "CONFIRMATION_OR_CONTRADICTION_ONLY",
        },
        "receipt": {
            "sha256": receipt,
            "all_78_rules_present": True,
            "murphy_rule_count": len(m_set),
            "nison_rule_count": len(n_set),
        },
        "governance": {
            "2025_oos_unchanged": mode == "oos_evaluation",
            "synthetic_rules_created": False,
            "not_evaluable_promoted_to_signal": False,
            "nison_generates_direction": False,
            "adapter_generates_direction": False,
        },
        "provenance": prov,
    }
    return RuleAdapterResult("PASS", package)


def assert_governed_78_package(package: Mapping[str, Any]) -> None:
    """Consumer-side hard gate: the Brain may not consume a partial package."""
    if package.get("schema_version") != SCHEMA_VERSION:
        raise AssertionError("INVALID_RULE_ADAPTER_SCHEMA")
    murphy = package.get("murphy", {})
    nison = package.get("nison", {})
    receipt = package.get("receipt", {})
    if murphy.get("rule_count") != 34 or nison.get("rule_count") != 44:
        raise AssertionError("FULL_78_RULE_PACKAGE_INCOMPLETE")
    if receipt.get("all_78_rules_present") is not True:
        raise AssertionError("FULL_78_RULE_RECEIPT_INVALID")
    if len(murphy.get("rows", [])) != 34 or len(nison.get("rows", [])) != 44:
        raise AssertionError("FULL_78_RULE_ROWS_INCOMPLETE")
