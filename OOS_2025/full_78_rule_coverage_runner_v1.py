from __future__ import annotations

from pathlib import Path
from typing import Iterable
import pandas as pd

MURPHY_RULES = [
    'MURPHY_0003','MURPHY_0004','MURPHY_0006','MURPHY_0007','MURPHY_0018','MURPHY_0019',
    'MURPHY_0021','MURPHY_0022','MURPHY_0023','MURPHY_0025','MURPHY_0026','MURPHY_0028',
    'MURPHY_0029','MURPHY_0030','MURPHY_0031','MURPHY_0032','MURPHY_0033','MURPHY_0034',
    'MURPHY_0035','MURPHY_0036','MURPHY_0037','MURPHY_0038','MURPHY_0039','MURPHY_0040',
    'MURPHY_0041','MURPHY_0042','MURPHY_0043','MURPHY_0044','MURPHY_0045','MURPHY_0047',
    'MURPHY_0048','MURPHY_0049','MURPHY_0050','MURPHY_0051',
]
NISON_RULES = [f'NISON_{i:04d}' for i in range(1, 45)]
ALLOWLIST = MURPHY_RULES + NISON_RULES


def run_2025_coverage(smoke: pd.DataFrame) -> pd.DataFrame:
    """Run the complete 78-rule evidence boundary for 2025.

    This runner does not invent missing evidence. A rule with no authoritative
    2025 producer output is recorded as NO_2025_OUTPUT. Observed smoke output
    is summarized without promoting it to final Decision-Brain evidence.
    """
    required = {"timestamp", "rule_id", "status"}
    missing = required - set(smoke.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = smoke.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df[df["timestamp"].dt.year.eq(2025)]

    rows = []
    for rule_id in ALLOWLIST:
        subset = df[df["rule_id"].astype(str).eq(rule_id)]
        if subset.empty:
            rows.append({
                "rule_id": rule_id,
                "family": "MURPHY" if rule_id.startswith("MURPHY") else "NISON",
                "coverage_status": "NO_2025_OUTPUT",
                "rows": 0,
                "pass": 0,
                "fail": 0,
                "not_evaluable": 0,
                "decision_evidence_status": "NOT_EVALUABLE",
            })
            continue
        counts = subset["status"].astype(str).value_counts()
        rows.append({
            "rule_id": rule_id,
            "family": "MURPHY" if rule_id.startswith("MURPHY") else "NISON",
            "coverage_status": "OBSERVED_2025_OUTPUT",
            "rows": len(subset),
            "pass": int(counts.get("PASS", 0)),
            "fail": int(counts.get("FAIL", 0)),
            "not_evaluable": int(counts.get("NOT_EVALUABLE", 0)),
            "decision_evidence_status": "BOUNDARY_ONLY",
        })
    return pd.DataFrame(rows)


def run_from_csv(path: str | Path) -> pd.DataFrame:
    return run_2025_coverage(pd.read_csv(path))
