"""Deterministic audit for Murphy governed coverage before Brain execution."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

MURPHY_IDS = {f"MURPHY_{i:04d}" for i in [3,4,6,7,18,19,21,22,23,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51]}

def split(value: object) -> list[str]:
    return [x.strip() for x in str(value or "").split("|") if x.strip() and x.strip().upper() not in {"NONE", "NULL", "NAN"}]

def audit(path: Path) -> dict[str, object]:
    df = pd.read_csv(path)
    if "source_rule_id" not in df.columns:
        raise SystemExit("BLOCKED_MURPHY_SCHEMA_SCOPE: missing source_rule_id")
    ids = sorted({rid for value in df["source_rule_id"] for rid in split(value)})
    unknown = sorted(set(ids) - MURPHY_IDS)
    missing = sorted(MURPHY_IDS - set(ids))
    duplicate_rows = int(df["source_rule_id"].duplicated().sum())
    result = {
        "status": "PASS" if not missing and not unknown else "BLOCKED",
        "murphy_registry_rules": len(MURPHY_IDS),
        "murphy_loaded_rules": len(ids),
        "murphy_mapped_rules": len(set(ids) & MURPHY_IDS),
        "murphy_missing_rule_ids": missing,
        "murphy_unknown_rule_ids": unknown,
        "duplicate_source_rows": duplicate_rows,
        "source_rows": int(len(df)),
    }
    print(result)
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("csv", type=Path)
    result = audit(p.parse_args().csv)
    raise SystemExit(0 if result["status"] == "PASS" else 2)
