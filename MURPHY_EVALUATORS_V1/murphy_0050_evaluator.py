from typing import Dict, Any

REQUIRED = [
    "general_trend",
    "sector_direction",
    "weekly_monthly_review",
    "support_resistance_trendlines",
    "volume_open_interest",
    "retracements_gaps",
    "reversal_continuation_patterns",
    "moving_averages_oscillators",
]


def evaluate_0050(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0050 exact checklist evaluator; never generates direction."""
    item_status = {}
    for item in REQUIRED:
        value = evidence.get(item)
        item_status[item] = value if value in {"PASS", "FAIL", "NOT_EVALUABLE"} else "NOT_EVALUABLE"

    if any(value == "FAIL" for value in item_status.values()):
        overall = "FAIL"
    elif all(value == "PASS" for value in item_status.values()):
        overall = "PASS"
    else:
        overall = "NOT_EVALUABLE"

    return {
        "rule_id": "MURPHY_0050",
        "status": overall,
        "direction": "NONE",
        "checklist": item_status,
        "reason": "0050 is a pre-trade checklist; incomplete evidence cannot be converted to PASS and it cannot generate direction.",
    }
