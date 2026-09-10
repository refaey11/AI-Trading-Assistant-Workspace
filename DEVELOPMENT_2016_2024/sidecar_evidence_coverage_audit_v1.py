from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

MURPHY_IDS = {f"MURPHY_{i:04d}" for i in [3,4,6,7,18,19,21,22,23,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51]}
NISON_IDS = {f"NISON_{i:04d}" for i in range(1, 45)}


def split_ids(value: Any) -> list[str]:
    return [x.strip() for x in str(value or "").split("|") if x.strip() and x.strip().upper() not in {"NONE", "NULL", "NAN", "NISON_NONE"}]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--murphy", type=Path, required=True)
    p.add_argument("--nison", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()

    m = pd.read_csv(a.murphy)
    n = pd.read_csv(a.nison)
    if "source_rule_id" not in m.columns:
        raise ValueError("Murphy source_rule_id missing")
    if "rule_id" not in n.columns:
        raise ValueError("Nison rule_id missing")

    m_ids = {rid for value in m.source_rule_id.dropna() for rid in split_ids(value)}
    observed_m = sorted(m_ids & MURPHY_IDS)
    missing_m = sorted(MURPHY_IDS - m_ids)
    unknown_m = sorted(m_ids - MURPHY_IDS)

    n_ids = set(str(x).strip() for x in n.rule_id.dropna())
    observed_n = sorted(n_ids & NISON_IDS)
    missing_n = sorted(NISON_IDS - n_ids)
    unknown_n = sorted(n_ids - NISON_IDS)

    status = n.status.astype(str).str.upper().str.strip() if "status" in n.columns else pd.Series(dtype=object)
    direction = n.direction.astype(str).str.upper().str.strip() if "direction" in n.columns else pd.Series(dtype=object)
    directional_pass = int(((status == "PASS") & direction.isin({"BUY", "SELL", "BULLISH", "BEARISH"})).sum())
    directional_pass_rows = n.loc[(status == "PASS") & direction.isin({"BUY", "SELL", "BULLISH", "BEARISH"})]

    by_rule = {}
    for rid, g in n.groupby("rule_id", sort=True):
        s = g.status.astype(str).str.upper().str.strip()
        d = g.direction.astype(str).str.upper().str.strip() if "direction" in g.columns else pd.Series(dtype=object)
        by_rule[str(rid)] = {
            "rows": int(len(g)),
            "pass": int((s == "PASS").sum()),
            "fail": int((s == "FAIL").sum()),
            "not_evaluable": int((s == "NOT_EVALUABLE").sum()),
            "directional_pass": int(((s == "PASS") & d.isin({"BUY", "SELL", "BULLISH", "BEARISH"})).sum()),
        }

    report = {
        "status": "SIDE_CAR_EVIDENCE_COVERAGE_AUDIT_V1",
        "murphy": {
            "governed_count": len(MURPHY_IDS),
            "observed_count": len(observed_m),
            "observed_ids": observed_m,
            "missing_count": len(missing_m),
            "missing_ids": missing_m,
            "unknown_count": len(unknown_m),
            "unknown_ids": unknown_m,
            "decision_eligible_observed_count": len(observed_m),
            "note": "Observed means present in the selected Murphy source CSV; eligibility remains governed by the source manifest and replay contract.",
        },
        "nison": {
            "governed_count": len(NISON_IDS),
            "observed_count": len(observed_n),
            "missing_count": len(missing_n),
            "missing_ids": missing_n,
            "unknown_count": len(unknown_n),
            "unknown_ids": unknown_n,
            "total_rows": int(len(n)),
            "status_counts": {str(k): int(v) for k, v in status.value_counts(dropna=False).items()},
            "direction_counts": {str(k): int(v) for k, v in direction.value_counts(dropna=False).items()},
            "directional_pass_rows": directional_pass,
            "directional_pass_rule_ids": sorted(set(str(x) for x in directional_pass_rows.rule_id)),
            "by_rule": by_rule,
        },
        "decision_contract": {
            "murphy_generates_direction": True,
            "nison_generates_direction": False,
            "nison_opposite_directional_pass_is_contradiction": True,
            "nison_absence_or_fail_is_not_contradiction": True,
            "no_engine_changes": True,
        },
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
