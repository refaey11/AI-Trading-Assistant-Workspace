from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re

RULE_IDS = [
    "0003","0004","0006","0007","0018","0019","0021","0022","0023","0025","0026","0028","0029",
    "0030","0031","0032","0033","0034","0035","0036","0037","0038","0039","0040","0041","0042",
    "0043","0044","0045","0047","0048","0049","0050","0051",
]

TEXT_EXTS = {".csv", ".json", ".md", ".txt", ".yml", ".yaml", ".py"}
FAMILY_TOKENS = {
    "p_and_f": ("POINT", "PNF", "P&F", "POINT_AND_FIGURE"),
    "trendline": ("TRENDLINE",),
    "pivot": ("PIVOT",),
    "elliott": ("ELLIOTT", "WAVE"),
    "fibonacci": ("FIBONACCI", "FIB"),
    "cycle": ("CYCLE",),
    "psar": ("PSAR", "PARABOLIC_SAR", "SAR"),
    "dmi_adx": ("DMI", "ADX"),
    "volume": ("VOLUME",),
    "open_interest": ("OPEN_INTEREST", "OI_"),
    "obv": ("OBV",),
    "breadth": ("BREADTH", "TRIN", "A_D", "ADVANCE_DECLINE"),
    "risk": ("RISK", "MARGIN", "EXPOSURE", "CAPITAL"),
    "process": ("PROCESS", "DISCIPLINE", "TRADE_PLAN"),
}


def family_hints(path: str, text: str = "") -> list[str]:
    hay = (path + "\n" + text[:50000]).upper()
    return [fam for fam, toks in FAMILY_TOKENS.items() if any(tok in hay for tok in toks)]


def path_kind(path: str) -> str:
    u = path.upper()
    if "MAPPING" in u or "MAP" in Path(path).stem.upper():
        return "MAPPING"
    if "CONTRACT" in u or "SPEC" in u:
        return "CONTRACT_OR_SPEC"
    if "EVALUAT" in u or "EVAL" in u:
        return "EVALUATOR"
    if "FROZEN" in u or "FREEZE" in u:
        return "FREEZE_OR_EVIDENCE"
    if any(x in u for x in ("EVIDENCE", "AUDIT", "RECONCIL")):
        return "AUDIT_OR_EVIDENCE"
    return "OTHER"


def scan_text(path: Path) -> tuple[set[str], list[str]]:
    ids: set[str] = set()
    excerpts: list[str] = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, 1):
                found = re.findall(r"MURPHY_(\d{4})", line.upper())
                wanted = [x for x in found if x in RULE_IDS]
                if wanted:
                    ids.update(wanted)
                    if len(excerpts) < 5:
                        excerpts.append(f"L{line_no}:{line.strip()[:260]}")
                if line_no > 500000 and path.suffix.lower() == ".csv":
                    break
    except Exception:
        pass
    return ids, excerpts


def score(kind: str, families: list[str]) -> int:
    base = {"MAPPING": 100, "CONTRACT_OR_SPEC": 80, "EVALUATOR": 70, "FREEZE_OR_EVIDENCE": 60, "AUDIT_OR_EVIDENCE": 50, "OTHER": 10}[kind]
    return base + min(30, 5 * len(families))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--json", required=True, type=Path)
    args = ap.parse_args()

    evidence = {f"MURPHY_{rid}": [] for rid in RULE_IDS}
    for p in args.root.rglob("*"):
        if not p.is_file():
            continue
        ids: set[str] = set()
        excerpts: list[str] = []
        if p.suffix.lower() in TEXT_EXTS:
            ids, excerpts = scan_text(p)
        ids |= set(re.findall(r"MURPHY_(\d{4})", p.name.upper())) & set(RULE_IDS)
        if not ids:
            continue
        rel = str(p.relative_to(args.root))
        fams = family_hints(rel, " ".join(excerpts))
        kind = path_kind(rel)
        for rid in sorted(ids):
            evidence[f"MURPHY_{rid}"].append({
                "path": rel,
                "kind": kind,
                "score": score(kind, fams),
                "family_hints": fams,
                "excerpts": excerpts,
            })

    rows = []
    detailed = {}
    for rid in RULE_IDS:
        rule = f"MURPHY_{rid}"
        items = evidence[rule]
        by_path = {}
        for item in items:
            by_path[item["path"]] = item
        candidates = sorted(by_path.values(), key=lambda x: (-x["score"], x["path"]))
        families = sorted({f for x in candidates for f in x["family_hints"]})
        kinds = sorted({x["kind"] for x in candidates})
        if rid == "0039":
            status = "PROCESS_ONLY_NO_MARKET_PRODUCER_EXPECTED"
        elif rid in {"0042","0043","0044","0045","0050","0051"}:
            status = "NON_MARKET_OR_PROCESS_GATE_REVIEW"
        elif candidates:
            status = "ARCHIVE_REFERENCES_FOUND_MAPPING_REVIEW_REQUIRED"
        else:
            status = "NO_ARCHIVE_REFERENCE_FOUND"
        top = candidates[:8]
        rows.append({
            "rule_id": rule,
            "status": status,
            "reference_count": len(candidates),
            "kinds": "|".join(kinds),
            "family_hints": "|".join(families),
            "top_reference_paths": "|".join(x["path"] for x in top),
        })
        detailed[rule] = {"status": status, "reference_count": len(candidates), "candidates": top}

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    report = {
        "status": "PASS",
        "scope_rule_count": len(RULE_IDS),
        "rules_with_archive_references": sum(r["reference_count"] > 0 for r in rows),
        "rules_without_archive_references": sum(r["reference_count"] == 0 for r in rows),
        "do_not_promote_eligibility": True,
        "do_not_synthesize": True,
        "note": "Reference discovery is not equivalent to semantic mapping or decision eligibility.",
        "rows": rows,
        "detailed": detailed,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({k: report[k] for k in ("status", "scope_rule_count", "rules_with_archive_references", "rules_without_archive_references", "do_not_promote_eligibility", "do_not_synthesize")}, indent=2))
    print("--- MURPHY 34 BINDING CANDIDATE SUMMARY ---")
    for r in rows:
        print(f"{r['rule_id']}\t{r['status']}\trefs={r['reference_count']}\tkinds={r['kinds']}\tfamilies={r['family_hints']}")
        top = detailed[r['rule_id']]['candidates']
        for c in top[:3]:
            ex = " || ".join(c['excerpts'][:1])
            print(f"  - {c['kind']}\t{c['path']}\tfam={','.join(c['family_hints'])}\t{ex}")


if __name__ == "__main__":
    main()
