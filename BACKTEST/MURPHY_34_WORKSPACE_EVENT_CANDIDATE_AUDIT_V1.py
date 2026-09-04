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
WANTED = {f"MURPHY_{x}" for x in RULE_IDS}

def read_head(path: Path, limit: int = 200_000) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except Exception:
        return ""

def extract_ids(text: str) -> set[str]:
    return {f"MURPHY_{x}" for x in re.findall(r"MURPHY_(\d{4})", text.upper()) if f"MURPHY_{x}" in WANTED}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--json", required=True, type=Path)
    args = ap.parse_args()

    rows = []
    rule_hits = {r: 0 for r in sorted(WANTED)}
    direct_backed = {r: 0 for r in sorted(WANTED)}

    for p in args.root.rglob("*.csv"):
        head = read_head(p)
        if not head:
            continue
        lines = head.splitlines()
        if not lines:
            continue
        header = lines[0].lower()
        cols = [x.strip().lower() for x in lines[0].split(",")]
        text_ids = extract_ids(head) | extract_ids(str(p))
        if not text_ids:
            continue

        has_timestamp = "timestamp" in cols or "time" in cols or "datetime" in cols
        has_status = any(c in cols for c in ("status", "rule_status", "evaluation_status", "signal_status"))
        has_direction = any(c in cols for c in ("direction", "signal", "side", "trade_direction"))
        has_result = any(c in cols for c in ("pass", "passed", "is_pass", "eligible", "decision"))
        kind = "DIRECT_EVENT_CSV" if (has_timestamp and (has_status or has_direction or has_result)) else "REFERENCE_CSV"

        for rid in sorted(text_ids):
            rule_hits[rid] += 1
            if kind == "DIRECT_EVENT_CSV":
                direct_backed[rid] += 1
            rows.append({
                "rule_id": rid,
                "path": str(p.relative_to(args.root)),
                "kind": kind,
                "columns": "|".join(cols[:80]),
                "has_timestamp": has_timestamp,
                "has_status": has_status,
                "has_direction": has_direction,
                "has_result": has_result,
            })

    by_rule = {}
    for rid in sorted(WANTED):
        rr = [x for x in rows if x["rule_id"] == rid]
        direct = [x for x in rr if x["kind"] == "DIRECT_EVENT_CSV"]
        status = "DIRECT_EVENT_CANDIDATES_FOUND" if direct else ("REFERENCE_ONLY" if rr else "NO_CSV_REFERENCE")
        by_rule[rid] = {
            "status": status,
            "reference_csv_count": len(rr),
            "direct_event_csv_count": len(direct),
            "top_direct_event_paths": [x["path"] for x in direct[:20]],
            "top_reference_paths": [x["path"] for x in rr[:20]],
        }

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["rule_id","path","kind","columns","has_timestamp","has_status","has_direction","has_result"])
        w.writeheader(); w.writerows(rows)

    report = {
        "status": "PASS",
        "scope_rule_count": len(WANTED),
        "rules_with_any_csv_reference": sum(v["reference_csv_count"] > 0 for v in by_rule.values()),
        "rules_with_direct_event_csv_candidates": sum(v["direct_event_csv_count"] > 0 for v in by_rule.values()),
        "rules_without_csv_reference": sum(v["reference_csv_count"] == 0 for v in by_rule.values()),
        "no_synthetic_evidence": True,
        "no_eligibility_promotion": True,
        "note": "This audit only identifies CSVs whose path/content explicitly references a governed Murphy ID; direct-event status is a candidate classification, not eligibility.",
        "by_rule": by_rule,
        "rows": rows,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: report[k] for k in report if k.startswith("rules_")}, indent=2))
    for rid, info in by_rule.items():
        print(f"{rid}\t{info['status']}\trefs={info['reference_csv_count']}\tdirect={info['direct_event_csv_count']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
