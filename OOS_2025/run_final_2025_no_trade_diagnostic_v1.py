#!/usr/bin/env python3
"""Standalone read-only diagnostic for the frozen 2025 Final Brain manifest.

This tool does not modify rules, thresholds, evidence, or the Decision Brain.
It only reads an already-produced FINAL_2025_GOVERNED_78_RULE_MANIFEST.json (or
its embedded source_manifest) and emits a compact blocker report.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


KEYS = [
    "events",
    "executable",
    "no_trade",
    "not_evaluable",
    "murphy_rule_count_in_event",
    "nison_rule_count_in_event",
    "tiz_verified_events",
    "primary_reason_counts",
    "event_status_counts",
    "execution_status_counts",
    "risk_pass_counts",
    "tiz_status_counts",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, default=Path("FINAL_2025_NO_TRADE_DIAGNOSTIC.json"))
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    source = data.get("final_brain_provenance", {}).get("source_manifest", {})
    if not source:
        source = data.get("source_manifest", {})
    if not source:
        raise SystemExit("Manifest does not contain a source_manifest; diagnostic cannot be derived safely.")

    diagnostic = {key: source.get(key) for key in KEYS}
    diagnostic["trades"] = data.get("core", {}).get("trades")
    diagnostic["pnl"] = data.get("core", {}).get("pnl")
    diagnostic["total_R"] = data.get("core", {}).get("total_R")
    diagnostic["expectancy_R"] = data.get("core", {}).get("expectancy_R")
    diagnostic["profit_factor"] = data.get("core", {}).get("profit_factor")
    diagnostic["status"] = data.get("status")
    diagnostic["read_only"] = True
    diagnostic["oos_tuning"] = source.get("oos_tuning")
    diagnostic["new_rule_semantics"] = source.get("new_rule_semantics")

    args.output.write_text(json.dumps(diagnostic, indent=2, sort_keys=True), encoding="utf-8")
    print("FINAL_2025_NO_TRADE_DIAGNOSTIC=" + json.dumps(diagnostic, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
