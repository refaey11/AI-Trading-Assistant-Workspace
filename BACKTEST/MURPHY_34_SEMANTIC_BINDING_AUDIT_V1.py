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

KEYWORDS = {
    "MAPPING": 100,
    "FROZEN": 90,
    "FREEZE": 90,
    "EXACT": 80,
    "EVALUATOR": 70,
    "CONTRACT": 60,
    "SPEC": 50,
    "AUDIT": 40,
}


def rule_hits(text: str) -> set[str]:
    return {x for x in re.findall(r"MURPHY[_ -]?(\d{4})", text.upper()) if x in RULE_IDS}


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


def extract_rows(path: Path, rule: str) -> list[dict]:
    rows = []
    suffix = path.suffix.lower()
    try:
        if suffix == ".csv":
            with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    text = json.dumps(row, ensure_ascii=False)
                    if rule in text.upper():
                        rows.append({"line": i + 2, "text": text[:1200]})
                    if len(rows) >= 8:
                        break
        elif suffix in {".json", ".md", ".txt", ".yaml", ".yml", ".py"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()
            for i, line in enumerate(lines, 1):
                if rule in line.upper():
                    rows.append({"line": i, "text": line[:1200]})
                    if len(rows) >= 8:
                        break
    except Exception:
        return []
    return rows


def status_from_text(text: str) -> str:
    u = text.upper()
    negative = [
        "NOT_FROZEN", "NOT FROZEN", "UNFROZEN", "PENDING", "UNVERIFIED",
        "NOT_EVALUABLE", "NOT EVALUABLE", "REVIEW_REQUIRED", "REVIEW REQUIRED",
        "PARTIAL", "BLOCKED",
    ]
    positive = ["FROZEN", "EXACT", "ELIGIBLE", "PASS", "VERIFIED"]
    if any(x in u for x in negative):
        return "NEGATIVE_OR_REVIEW"
    if any(x in u for x in positive):
        return "POSITIVE_CANDIDATE"
    return "UNSPECIFIED"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--json", required=True, type=Path)
    args = ap.parse_args()

    files = [p for p in args.root.rglob("*") if p.is_file() and p.suffix.lower() in {".csv", ".json", ".md", ".txt", ".yaml", ".yml", ".py"}]
    results = []
    for rid in RULE_IDS:
        rule = f"MURPHY_{rid}"
        candidates = []
        for p in files:
            rel = str(p.relative_to(args.root))
            if "MURPHY" not in rel.upper() and kind(rel) not in {"MAPPING", "EVALUATOR", "CONTRACT", "FROZEN", "AUDIT", "SPEC"}:
                continue
            try:
                if rule not in p.name.upper():
                    txt = ""
                    if p.suffix.lower() == ".csv":
                        # inspect only the first 500k lines cheaply
                        with p.open("r", encoding="utf-8", errors="ignore") as f:
                            for j, line in enumerate(f):
                                txt += line
                                if j >= 5000:
                                    break
                    else:
                        txt = p.read_text(encoding="utf-8", errors="ignore")[:2_000_000]
                    if rule not in txt.upper():
                        continue
                rows = extract_rows(p, rule)
                text_blob = "\n".join(r["text"] for r in rows)
                k = kind(rel)
                score = KEYWORDS.get(k, 10)
                st = status_from_text(text_blob + " " + rel)
                candidates.append({"path": rel, "kind": k, "score": score, "status_signal": st, "rows": rows})
            except Exception:
                continue
        candidates.sort(key=lambda x: (-x["score"], x["path"]))
        positive = [x for x in candidates if x["status_signal"] == "POSITIVE_CANDIDATE"]
        negative = [x for x in candidates if x["status_signal"] == "NEGATIVE_OR_REVIEW"]
        if rid == "0039":
            overall = "PROCESS_ONLY"
        elif positive and not any("NOT_FROZEN" in json.dumps(x).upper() for x in positive):
            overall = "POSITIVE_CANDIDATE_REQUIRES_GOVERNED_CHECK"
        elif negative or candidates:
            overall = "REFERENCE_FOUND_REVIEW_REQUIRED"
        else:
            overall = "NO_REFERENCE_FOUND"
        results.append({"rule_id": rule, "overall_status": overall, "candidate_count": len(candidates), "top_candidates": candidates[:10]})

    report = {
        "status": "PASS",
        "scope": "MURPHY_34",
        "rule_count": len(RULE_IDS),
        "rules_with_references": sum(x["candidate_count"] > 0 for x in results),
        "rules_without_references": sum(x["candidate_count"] == 0 for x in results),
        "eligibility_promoted": False,
        "synthetic_evidence_generated": False,
        "note": "This is a discovery/audit report. It does not promote eligibility or invent mappings.",
        "rules": results,
    }
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rule_id", "overall_status", "candidate_count", "top_paths"])
        w.writeheader()
        for x in results:
            w.writerow({"rule_id": x["rule_id"], "overall_status": x["overall_status"], "candidate_count": x["candidate_count"], "top_paths": " | ".join(c["path"] for c in x["top_candidates"][:5])})
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "rule_count", "rules_with_references", "rules_without_references", "eligibility_promoted", "synthetic_evidence_generated")}, indent=2))
    print("--- 34 RULE BINDING AUDIT ---")
    for x in results:
        print(f"{x['rule_id']}\t{x['overall_status']}\trefs={x['candidate_count']}")
        for c in x["top_candidates"][:3]:
            print(f"  {c['kind']}\t{c['status_signal']}\t{c['path']}")


if __name__ == "__main__":
    main()
