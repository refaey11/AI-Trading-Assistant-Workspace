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
    hits = []
    for fam, toks in FAMILY_TOKENS.items():
        if any(tok in hay for tok in toks):
            hits.append(fam)
    return hits


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
                    if len(excerpts) < 3:
                        excerpts.append(f"L{line_no}:{line.strip()[:220]}")
                if line_no > 250000 and path.suffix.lower() == ".csv":
                    break
    except Exception:
        pass
    return ids, excerpts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--json", required=True, type=Path)
    args = ap.parse_args()

    rows = []
    evidence = {f"MURPHY_{rid}": [] for rid in RULE_IDS}
    for p in args.root.rglob("*"):
        if not p.is_file():
            continue
        ids: set[str] = set()
        excerpts: list[str] = []
        if p.suffix.lower() in TEXT_EXTS:
            ids, excerpts = scan_text(p)
        # Always add filename-based hints, even when the file body is huge/binary.
        name_ids = set(re.findall(r"MURPHY_(\d{4})", p.name.upper())) & set(RULE_IDS)
        ids |= name_ids
        if not ids:
            continue
        fams = family_hints(str(p), " ".join(excerpts))
        rel = str(p.relative_to(args.root))
        for rid in sorted(ids):
            evidence[f"MURPHY_{rid}"].append({"path": rel, "family_hints": fams, "excerpts": excerpts})

    for rid in RULE_IDS:
        rule = f"MURPHY_{rid}"
        items = evidence[rule]
        unique_paths = sorted({x["path"] for x in items})
        families = sorted({f for x in items for f in x["family_hints"]})
        if rid in {"0039"}:
            status = "PROCESS_ONLY_NO_MARKET_PRODUCER_EXPECTED"
        elif rid in {"0042","0043","0044","0045","0050","0051"}:
            status = "NON_MARKET_OR_PROCESS_GATE_REVIEW"
        elif unique_paths:
            status = "ARCHIVE_EVIDENCE_REFERENCES_FOUND_REQUIRES_RULE_MAPPING_REVIEW"
        else:
            status = "NO_ARCHIVE_REFERENCE_FOUND"
        rows.append({"rule_id": rule, "status": status, "reference_count": len(unique_paths), "family_hints": "|".join(families), "reference_paths": "|".join(unique_paths)})

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
        "rows": rows,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in report if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
