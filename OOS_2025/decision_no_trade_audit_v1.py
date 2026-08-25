"""Governed diagnostic for 2025 NO_TRADE events.

This module is diagnostic-only. It does not alter Decision Brain rules,
thresholds, risk parameters, or trading semantics. It consumes an already
produced FINAL_2025_DECISION_EVENTS.csv and creates a deterministic breakdown
of execution blockers, preserving the 78-rule provenance fields.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import pandas as pd


def _json_list(value):
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def audit(events_path: Path, output_dir: Path) -> dict:
    df = pd.read_csv(events_path)
    required = {
        "timestamp", "status", "execution_status", "reason", "primary_reason",
        "murphy_rule_count", "nison_rule_count", "governed_78_receipt_sha256",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required event columns: {missing}")

    output_dir.mkdir(parents=True, exist_ok=True)
    no_trade = df[df["status"].astype(str).eq("NO_TRADE")].copy()

    primary = Counter(no_trade["primary_reason"].fillna("UNKNOWN").astype(str))
    execution = Counter(no_trade["execution_status"].fillna("UNKNOWN").astype(str))
    risk = Counter(no_trade.get("risk_pass", pd.Series(dtype=str)).fillna("UNKNOWN").astype(str))
    tiz = Counter(no_trade.get("tiz_status", pd.Series(dtype=str)).fillna("UNKNOWN").astype(str))

    # Governance checks: the audit must never be allowed to mask a broken
    # 78-rule event stream while diagnosing execution.
    if not df.empty:
        if int(df["murphy_rule_count"].min()) != 34:
            raise AssertionError("Audit refused: not every event contains 34 Murphy rules")
        if int(df["nison_rule_count"].min()) != 44:
            raise AssertionError("Audit refused: not every event contains 44 Nison rules")
        if df["governed_78_receipt_sha256"].astype(str).replace("nan", "").eq("").any():
            raise AssertionError("Audit refused: event missing governed 78-rule receipt")

    # Stable diagnostic table: one row per event, with the first gate reason
    # already selected by the frozen decision boundary.
    audit_cols = [
        "timestamp", "status", "direction", "execution_status", "primary_reason",
        "risk_pass", "tiz_status", "murphy_status", "murphy_direction",
        "nison_confirmation", "nison_contradiction",
        "murphy_rule_count", "nison_rule_count", "governed_78_receipt_sha256",
    ]
    audit_cols = [c for c in audit_cols if c in df.columns]
    df[audit_cols].to_csv(output_dir / "NO_TRADE_EVENT_AUDIT.csv", index=False)

    top = primary.most_common()
    result = {
        "status": "PASS",
        "mode": "DIAGNOSTIC_ONLY",
        "evaluation_year": 2025,
        "events": int(len(df)),
        "no_trade_events": int(len(no_trade)),
        "executable_events": int(df["status"].astype(str).eq("EXECUTABLE").sum()),
        "primary_reason_counts": dict(top),
        "execution_status_counts": dict(execution.most_common()),
        "risk_status_counts": dict(risk.most_common()),
        "tiz_status_counts": dict(tiz.most_common()),
        "rule_counts_verified": {
            "murphy": 34,
            "nison": 44,
            "all_events_preserved": bool(df.empty or ((df["murphy_rule_count"] == 34) & (df["nison_rule_count"] == 44)).all()),
        },
        "trading_semantics_changed": False,
        "oos_tuning": False,
        "purpose": "Identify the first dominant execution blocker without modifying any frozen trading semantics.",
    }
    (output_dir / "NO_TRADE_AUDIT_MANIFEST.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--events", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(audit(args.events, args.output_dir), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
