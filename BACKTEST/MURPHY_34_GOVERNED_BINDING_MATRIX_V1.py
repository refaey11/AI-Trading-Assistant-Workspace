from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

RULE_IDS = [
    "0003","0004","0006","0007","0018","0019","0021","0022","0023","0025","0026","0028","0029",
    "0030","0031","0032","0033","0034","0035","0036","0037","0038","0039","0040","0041","0042",
    "0043","0044","0045","0047","0048","0049","0050","0051",
]

TEXT_EXTS = {".csv", ".json", ".md", ".txt", ".yaml", ".yml", ".py"}
AVAILABILITY_FIELDS = (
    "availability_timestamp",
    "safe_availability_timestamp",
    "evidence_availability_timestamp",
    "decision_availability_timestamp",
)
NEGATIVE = (
    "NOT_FROZEN", "NOT FROZEN", "UNFROZEN", "PENDING", "UNVERIFIED",
    "NOT_EVALUABLE", "NOT EVALUABLE", "REVIEW_REQUIRED", "REVIEW REQUIRED",
    "PARTIAL", "BLOCKED", "SOURCE_REVIEW_REQUIRED",
)


def kind(path: str) -> str:
    u = path.upper()
    if "MAPPING" in u or "EXACT_MAPPING" in u:
        return "MAPPING"
    if "EVALUAT" in u:
        return "EVALUATOR"
    if "CONTRACT" in u:
        return "CONTRACT"
    if "SPEC" in u:
        return "SPEC"
    if "FREEZE" in u or "FROZEN" in u:
        return "FROZEN"
    if "AUDIT" in u or "RECONCIL" in u:
        return "AUDIT"
    return "OTHER"


def rule_token(rid: str) -> str:
    return f"MURPHY_{rid}"


def read_csv_header(path: Path) -> tuple[list[str], str]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        sample = "".join(next(reader, []))[:4000]
    return [str(x).strip() for x in header], sample


def file_signal(path: Path, rid: str) -> dict:
    rel = str(path)
    token = rule_token(rid)
    text = ""
    cols: list[str] = []
    try:
        if path.suffix.lower() == ".csv":
            cols, sample = read_csv_header(path)
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f):
                    text += line
                    if i >= 5000 or len(text) >= 1_500_000:
                        break
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")[:1_500_000]
    except Exception:
        return {"path": rel, "kind": kind(rel), "rule_present": False}

    u = (rel + "\n" + text).upper()
    rule_present = token in u or re.search(rf"MURPHY[_ -]?{rid}\b", u) is not None
    neg = [x for x in NEGATIVE if x in u]
    years = sorted({int(x) for x in re.findall(r"\b(20(?:1[6-9]|2[0-9]))\b", text)})
    availability = [c for c in cols if c in AVAILABILITY_FIELDS]
    has_timestamp = "timestamp" in cols or any("timestamp" in c.lower() for c in cols)
    has_rule = any(c in {"source_rule_id", "rule_id", "murphy_rule_id"} for c in cols)
    has_direction = any(c.lower() in {"direction", "signal", "bias", "trade_direction"} or "direction" in c.lower() for c in cols)
    return {
        "path": rel,
        "kind": kind(rel),
        "rule_present": bool(rule_present),
        "columns": cols,
        "availability_fields": availability,
        "has_timestamp": bool(has_timestamp),
        "has_rule_id_field": bool(has_rule),
        "has_direction_field": bool(has_direction),
        "negative_signals": neg[:8],
        "years_observed": years,
        "2025_observed": 2025 in years,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out-csv", required=True, type=Path)
    ap.add_argument("--out-json", required=True, type=Path)
    args = ap.parse_args()

    files = [p for p in args.root.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_EXTS]
    rows = []
    detailed = []

    for rid in RULE_IDS:
        candidates = []
        for p in files:
            sig = file_signal(p, rid)
            if not sig.get("rule_present"):
                continue
            candidates.append(sig)

        evaluator = [x for x in candidates if x["kind"] == "EVALUATOR"]
        mapping = [x for x in candidates if x["kind"] == "MAPPING"]
        explicit_availability = sorted({f for x in candidates for f in x.get("availability_fields", [])})
        candidate_evaluator_binding = []
        for x in evaluator:
            if x.get("has_timestamp") and x.get("has_rule_id_field") and x.get("availability_fields") and not x.get("2025_observed"):
                candidate_evaluator_binding.append(x["path"])

        if rid == "0039":
            status = "PROCESS_ONLY"
        elif candidate_evaluator_binding:
            status = "EVALUATOR_WITH_EXPLICIT_AVAILABILITY_CANDIDATE"
        elif mapping:
            status = "MAPPING_REFERENCE_ONLY"
        elif candidates:
            status = "REFERENCE_FOUND_REVIEW_REQUIRED"
        else:
            status = "NO_REFERENCE_FOUND"

        row = {
            "rule_id": rule_token(rid),
            "status": status,
            "candidate_file_count": len(candidates),
            "mapping_file_count": len(mapping),
            "evaluator_file_count": len(evaluator),
            "evaluator_binding_candidates": len(candidate_evaluator_binding),
            "availability_fields_observed": " | ".join(explicit_availability),
            "current_fanin_eligibility": "FALSE",
            "decision_time_strict_asof_verified": "FALSE",
            "promoted_to_decision_brain": "FALSE",
            "synthetic_evidence": "FALSE",
            "2025_used": "FALSE",
            "top_paths": " | ".join(x["path"] for x in (evaluator + mapping + candidates)[:8]),
        }
        rows.append(row)
        detailed.append({"rule_id": rule_token(rid), "summary": row, "candidates": candidates[:20]})

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    report = {
        "status": "PASS",
        "scope": "MURPHY_34",
        "rule_count": len(RULE_IDS),
        "rules_with_any_archive_reference": sum(x["candidate_file_count"] > 0 for x in rows),
        "rules_with_evaluator_availability_candidates": sum(x["evaluator_binding_candidates"] > 0 for x in rows),
        "rules_with_only_mapping_or_reference": sum(x["candidate_file_count"] > 0 and x["evaluator_binding_candidates"] == 0 for x in rows),
        "decision_time_strict_asof_verified": False,
        "current_fanin_eligibility_promoted": False,
        "synthetic_evidence_generated": False,
        "2025_used": False,
        "note": "Matrix is an evidence-binding inventory. It does not promote any rule into the Decision Brain and does not synthesize missing evidence.",
        "rules": detailed,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({k: report[k] for k in (
        "status", "rule_count", "rules_with_any_archive_reference", "rules_with_evaluator_availability_candidates",
        "rules_with_only_mapping_or_reference", "decision_time_strict_asof_verified", "current_fanin_eligibility_promoted"
    )}, indent=2))
    for x in rows:
        print(f"{x['rule_id']}\t{x['status']}\tevaluator_binding_candidates={x['evaluator_binding_candidates']}")


if __name__ == "__main__":
    main()
