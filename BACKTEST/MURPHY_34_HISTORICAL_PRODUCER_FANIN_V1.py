from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

STATUS_PASS = "PASS"
STATUS_FAIL = "FAIL"
STATUS_NE = "NOT_EVALUABLE"

# This bridge is intentionally conservative. It does not infer Murphy semantics,
# thresholds, direction, or missing producer values. It only routes producer rows
# that already contain the exact normalized fields required by the existing runtime.

RULE_SPECS: Dict[str, Dict[str, Any]] = {
    "MURPHY_0003": {"required": ["timestamp", "current_reaction_peak", "prior_reaction_peak", "current_reaction_trough", "prior_reaction_trough"]},
    "MURPHY_0004": {"required": ["timestamp", "current_reaction_peak", "prior_reaction_peak", "current_reaction_trough", "prior_reaction_trough"]},
    "MURPHY_0006": {"required": ["timestamp", "events"]},
    "MURPHY_0007": {"required": ["timestamp", "events"]},
    "MURPHY_0018": {"required": ["timestamp", "upper_line", "lower_line"]},
    "MURPHY_0019": {"required": ["timestamp", "upper_line", "lower_line"]},
    "MURPHY_0021": {"required": ["timestamp"]},
    "MURPHY_0022": {"required": ["timestamp"]},
    "MURPHY_0023": {"required": ["timestamp"]},
    "MURPHY_0025": {"required": ["timestamp"]},
    "MURPHY_0026": {"required": ["timestamp"]},
    "MURPHY_0028": {"required": ["timestamp", "divergence_type", "pivot_type"]},
    "MURPHY_0029": {"required": ["timestamp", "divergence_type", "pivot_type"]},
    "MURPHY_0030": {"required": ["timestamp"]},
    "MURPHY_0031": {"required": ["timestamp"]},
    "MURPHY_0032": {"required": ["timestamp"]},
    "MURPHY_0033": {"required": ["timestamp"]},
    "MURPHY_0034": {"required": ["timestamp", "wave1_high", "wave1_low", "wave2_extreme"]},
    "MURPHY_0035": {"required": ["timestamp", "length1", "length3", "length5"]},
    "MURPHY_0036": {"required": ["timestamp", "wave1_low", "wave1_high", "wave4_price"]},
    "MURPHY_0037": {"required": ["timestamp", "retracement_pct"]},
    "MURPHY_0038": {"required": ["timestamp", "previous_trough", "current_trough"]},
    "MURPHY_0039": {"required": ["timestamp", "system_defined", "regime_checked"]},
    "MURPHY_0040": {"required": ["timestamp", "trending"]},
    "MURPHY_0041": {"required": ["timestamp", "adx", "threshold"]},
    "MURPHY_0042": {"required": ["timestamp", "invested_pct"]},
    "MURPHY_0043": {"required": ["timestamp", "exposure_pct"]},
    "MURPHY_0044": {"required": ["timestamp", "risk_pct"]},
    "MURPHY_0045": {"required": ["timestamp", "margin_pct"]},
    "MURPHY_0047": {"required": ["timestamp", "index_new_high", "ad_fails_high"]},
    "MURPHY_0048": {"required": ["timestamp", "trin_ma10"]},
    "MURPHY_0049": {"required": ["timestamp", "trin"]},
    "MURPHY_0050": {"required": ["timestamp", "general_trend", "sector_direction", "weekly_monthly_review", "support_resistance_trendlines", "volume_open_interest", "retracements_gaps", "reversal_continuation_patterns", "moving_averages_oscillators"]},
    "MURPHY_0051": {"required": ["timestamp", "direction", "stance", "position_size", "acceptable_loss", "profit_objective", "entry", "order_type", "stop_loss"]},
}

# Producer family names discovered in the preserved Rule Evaluator workspace.
# These are routing hints, not semantic re-implementations.
PRODUCER_FAMILIES = {
    "FOUR_WEEK_LOOKBACK": "FOUR_WEEK_LOOKBACK_V1_OUTPUT",
    "DMI_ADX": "DMI_ADX_V1_OUTPUT",
    "PARABOLIC_SAR": "PARABOLIC_SAR_V1_OUTPUT",
    "OSCILLATOR_DIVERGENCE": "OSCILLATOR_DIVERGENCE_V1_OUTPUT",
    "TRENDLINE_GEOMETRY": "TRENDLINE_GEOMETRY_V1_OUTPUT",
    "OBV": "OBV_V1_OUTPUT",
    "VOLUME_CONFIRMATION": "VOLUME_CONFIRMATION_V2_OUTPUT",
    "OPEN_INTEREST": "OPEN_INTEREST_V1_OUTPUT",
    "PIVOT_SEQUENCE": "PIVOT_SEQUENCE_V1_OUTPUT",
    "PIVOT_SEQUENCE_V2": "PIVOT_SEQUENCE_V2_OUTPUT",
}


def _norm(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        v = value.strip()
        return v if v != "" else None
    return value


def _required_missing(row: Dict[str, Any], required: Iterable[str]) -> List[str]:
    return [k for k in required if _norm(row.get(k)) is None]


def validate_producer_row(rule_id: str, row: Dict[str, Any], source_artifact: str) -> Dict[str, Any]:
    if rule_id not in RULE_SPECS:
        raise ValueError(f"Unknown governed Murphy rule: {rule_id}")
    missing = _required_missing(row, RULE_SPECS[rule_id]["required"])
    if missing:
        return {
            "timestamp": row.get("timestamp"),
            "rule_id": rule_id,
            "source_rule_id": rule_id,
            "status": STATUS_NE,
            "directional_confirmation": "UNKNOWN",
            "reason": "Required normalized producer evidence is missing.",
            "missing_fields": missing,
            "provenance": {"source_artifact": source_artifact, "producer_bound": False},
        }
    return {
        "timestamp": row["timestamp"],
        "rule_id": rule_id,
        "source_rule_id": rule_id,
        "status": "EVIDENCE_AVAILABLE",
        "directional_confirmation": "UNKNOWN",
        "reason": "Required normalized producer evidence is present; canonical evaluator must determine PASS/FAIL.",
        "provenance": {"source_artifact": source_artifact, "producer_bound": True},
        "payload": row,
    }


def scan_csv(csv_path: Path, rule_id: str) -> Tuple[int, int]:
    available = 0
    not_evaluable = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return 0, 0
        for row in reader:
            result = validate_producer_row(rule_id, row, str(csv_path))
            if result["status"] == "EVIDENCE_AVAILABLE":
                available += 1
            else:
                not_evaluable += 1
    return available, not_evaluable


def build_inventory(root: Path) -> List[Dict[str, Any]]:
    inventory: List[Dict[str, Any]] = []
    for rule_id, spec in RULE_SPECS.items():
        matches = list(root.rglob("*.csv")) if root.exists() else []
        inventory.append({
            "rule_id": rule_id,
            "required_fields": spec["required"],
            "csv_candidates": len(matches),
            "status": STATUS_NE,
            "reason": "No exact producer binding is assumed until a source CSV is proven to contain the normalized required fields.",
        })
    return inventory


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Conservative Murphy-34 historical producer fan-in audit bridge")
    parser.add_argument("--root", type=Path, required=True, help="Root containing preserved producer outputs")
    parser.add_argument("--out", type=Path, required=True, help="Inventory JSON output path")
    args = parser.parse_args()

    write_json(args.out, {
        "schema_version": "1.0",
        "scope": "governed_murphy_34",
        "locked_year": 2025,
        "rules": build_inventory(args.root),
        "governance": {
            "synthetic_evidence": False,
            "threshold_invention": False,
            "direction_generation": False,
            "strict_asof_required": True,
        },
    })
