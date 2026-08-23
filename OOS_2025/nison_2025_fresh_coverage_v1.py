from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

EXPECTED_RULES = 44
EXPECTED_ROWS_2025 = 6225


def build_report(evidence_path: Path) -> dict:
    df = pd.read_csv(evidence_path)
    required = {"timestamp", "rule_id", "status", "available"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing evidence columns: {sorted(missing)}")

    ts = pd.to_datetime(df["timestamp"], utc=True)
    if ts.dt.year.ne(2025).any():
        raise ValueError("Evidence contains non-2025 timestamps")
    if df["rule_id"].nunique() != EXPECTED_RULES:
        raise ValueError("Evidence does not contain all 44 Nison rules")
    expected_rows = EXPECTED_ROWS_2025 * EXPECTED_RULES
    if len(df) != expected_rows:
        raise ValueError(f"Evidence rows {len(df)} != expected {expected_rows}")

    available = df["available"].astype(bool)
    per_rule = []
    for rule_id, group in df.groupby("rule_id", sort=True):
        per_rule.append({
            "rule_id": rule_id,
            "rows": int(len(group)),
            "available_rows": int(group["available"].astype(bool).sum()),
            "pass": int((group["status"].astype(str) == "PASS").sum()),
            "fail": int((group["status"].astype(str) == "FAIL").sum()),
            "not_evaluable": int((group["status"].astype(str) == "NOT_EVALUABLE").sum()),
        })

    return {
        "scope": "2025-01-01T00:00:00Z..2025-12-31T23:59:59Z",
        "nison_rules": EXPECTED_RULES,
        "input_rows_2025": EXPECTED_ROWS_2025,
        "evidence_rows": int(len(df)),
        "available_rows": int(available.sum()),
        "available_rate": float(available.mean()),
        "rules_with_any_available_evidence": int(sum(x["available_rows"] > 0 for x in per_rule)),
        "rules_with_full_timestamp_coverage": int(sum(x["available_rows"] == EXPECTED_ROWS_2025 for x in per_rule)),
        "rules_with_no_available_evidence": int(sum(x["available_rows"] == 0 for x in per_rule)),
        "status_counts": {k: int(v) for k, v in df["status"].astype(str).value_counts().to_dict().items()},
        "per_rule": per_rule,
        "governance": {
            "2025": "OOS evaluation-only",
            "tuning": False,
            "threshold_selection": False,
            "lookahead": False,
        },
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: nison_2025_fresh_coverage_v1.py <evidence.csv> <report.json>", file=sys.stderr)
        return 2
    report = build_report(Path(sys.argv[1]))
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    print(f"NISON_2025_RULES={report['nison_rules']}")
    print(f"NISON_2025_INPUT_ROWS={report['input_rows_2025']}")
    print(f"NISON_2025_EVIDENCE_ROWS={report['evidence_rows']}")
    print(f"NISON_2025_AVAILABLE_ROWS={report['available_rows']}")
    print(f"NISON_2025_RULES_WITH_ANY_AVAILABLE={report['rules_with_any_available_evidence']}")
    print(f"NISON_2025_RULES_WITH_NO_AVAILABLE={report['rules_with_no_available_evidence']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
