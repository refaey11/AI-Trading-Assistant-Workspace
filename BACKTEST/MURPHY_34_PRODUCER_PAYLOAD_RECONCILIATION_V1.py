#!/usr/bin/env python3
from __future__ import annotations

"""Evidence-preserving reconciliation of the original Murphy workspace payloads.

This is an audit/reconciliation tool, not an evaluator. It never invents values,
does not infer missing direction, and never promotes a rule to eligibility.
It inventories exact source files, fields, timestamps and rule references so that
only source-backed producer streams can be bound later.
"""

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any

RULE_IDS = [
    "MURPHY_0003","MURPHY_0004","MURPHY_0006","MURPHY_0007","MURPHY_0018","MURPHY_0019",
    "MURPHY_0021","MURPHY_0022","MURPHY_0023","MURPHY_0025","MURPHY_0026","MURPHY_0028",
    "MURPHY_0029","MURPHY_0030","MURPHY_0031","MURPHY_0032","MURPHY_0033","MURPHY_0034",
    "MURPHY_0035","MURPHY_0036","MURPHY_0037","MURPHY_0038","MURPHY_0039","MURPHY_0040",
    "MURPHY_0041","MURPHY_0042","MURPHY_0043","MURPHY_0044","MURPHY_0045","MURPHY_0047",
    "MURPHY_0048","MURPHY_0049","MURPHY_0050","MURPHY_0051",
]

FAMILY_TOKENS = {
    "FOUR_WEEK_LOOKBACK": "FOUR_WEEK_LOOKBACK",
    "DMI_ADX": "DMI_ADX",
    "PARABOLIC_SAR": "PARABOLIC_SAR",
    "OSCILLATOR_DIVERGENCE": "OSCILLATOR_DIVERGENCE",
    "TRENDLINE_GEOMETRY": "TRENDLINE_GEOMETRY",
    "OBV": "OBV",
    "VOLUME_CONFIRMATION": "VOLUME_CONFIRMATION",
    "OPEN_INTEREST": "OPEN_INTEREST",
    "PIVOT_SEQUENCE": "PIVOT_SEQUENCE",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def text_sample(path: Path, limit: int = 2_000_000) -> bytes:
    try:
        with path.open("rb") as f:
            return f.read(limit)
    except OSError:
        return b""


def detect_family(name: str) -> str:
    upper = name.upper()
    for token, family in FAMILY_TOKENS.items():
        if token in upper:
            return family
    return "UNKNOWN"


def rules_in_text(data: bytes) -> list[str]:
    text = data.decode("utf-8", errors="ignore")
    found = set(re.findall(r"MURPHY[_-]\\d{4}", text, flags=re.I))
    normalized = sorted({x.replace("-", "_").upper() for x in found if x.replace("-", "_").upper() in RULE_IDS})
    return normalized


def csv_profile(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"readable": False, "columns": [], "rows": 0, "timestamp_min": None, "timestamp_max": None, "rule_columns": [], "rule_values": [], "contains_2025": False}
    try:
        with path.open("r", encoding="utf-8-sig", newline="", errors="replace") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames or []
            result["columns"] = fields
            result["readable"] = True
            rule_cols = [c for c in fields if c.lower() in {"rule_id", "source_rule_id", "pass_rule_id"} or "rule_id" in c.lower()]
            result["rule_columns"] = rule_cols
            timestamps: list[str] = []
            rules: set[str] = set()
            for row in reader:
                result["rows"] += 1
                for c in rule_cols:
                    value = row.get(c)
                    if value:
                        for part in str(value).split("|"):
                            rid = part.strip().replace("-", "_").upper()
                            if rid in RULE_IDS:
                                rules.add(rid)
                ts = row.get("timestamp") or row.get("Timestamp")
                if ts:
                    timestamps.append(str(ts))
            if timestamps:
                result["timestamp_min"] = min(timestamps)
                result["timestamp_max"] = max(timestamps)
                result["contains_2025"] = any(str(x).startswith("2025") or "2025-" in str(x) for x in timestamps)
            result["rule_values"] = sorted(rules)
    except Exception as exc:
        result["error"] = str(exc)
    return result


def main() -> int:
    root = Path("artifacts/murphy_34_workspace_audit/extracted")
    out = Path("artifacts/murphy_34_workspace_reconciliation")
    out.mkdir(parents=True, exist_ok=True)
    if not root.exists():
        raise SystemExit(f"BLOCKED: extracted archive root missing: {root}")

    records: list[dict[str, Any]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        data = text_sample(path)
        rel = str(path.relative_to(root))
        ext = path.suffix.lower()
        rec: dict[str, Any] = {
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
            "family": detect_family(path.name),
            "rule_ids_in_text": rules_in_text(data),
            "contains_2025_text_sample": b"2025" in data,
        }
        if ext == ".csv":
            rec["csv"] = csv_profile(path)
        records.append(rec)

    per_rule: dict[str, dict[str, Any]] = {}
    for rid in RULE_IDS:
        matches = []
        for rec in records:
            hits = set(rec["rule_ids_in_text"])
            csv_hits = set(rec.get("csv", {}).get("rule_values", []))
            if rid in hits or rid in csv_hits or rid in rec["path"].upper().replace("-", "_"):
                matches.append(rec["path"])
        per_rule[rid] = {
            "candidate_payload_paths": sorted(set(matches)),
            "candidate_count": len(set(matches)),
            "decision_eligible": False,
            "status": "UNVERIFIED",
        }

    family_counts: dict[str, int] = {}
    for rec in records:
        family_counts[rec["family"]] = family_counts.get(rec["family"], 0) + 1

    report = {
        "schema_version": "1.0",
        "scope": "2016-2024",
        "locked_year": 2025,
        "source_root": str(root),
        "files_scanned": len(records),
        "producer_family_file_counts": family_counts,
        "rules": per_rule,
        "governance": {
            "synthetic_evidence_generated": False,
            "direction_generated": False,
            "eligibility_promoted": False,
            "threshold_invention": False,
            "missing_evidence_policy": "NOT_EVALUABLE",
            "strict_asof_required": True,
        },
        "next_gate": "prove exact producer-field semantics + provenance + availability timestamp + strict-asof 2016-2024 coverage per candidate",
    }

    (out / "MURPHY_34_PRODUCER_PAYLOAD_RECONCILIATION_V1.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    with (out / "MURPHY_34_PRODUCER_PAYLOAD_RECONCILIATION_V1.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rule_id", "candidate_count", "status", "candidate_payload_paths"])
        for rid in RULE_IDS:
            item = per_rule[rid]
            w.writerow([rid, item["candidate_count"], item["status"], " | ".join(item["candidate_payload_paths"])])

    print(json.dumps({
        "files_scanned": len(records),
        "rules_with_candidates": sum(1 for x in per_rule.values() if x["candidate_count"]),
        "rules_without_candidates": sum(1 for x in per_rule.values() if not x["candidate_count"]),
        "synthetic_evidence_generated": False,
        "eligibility_promoted": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
