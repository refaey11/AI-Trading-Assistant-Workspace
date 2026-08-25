from MURPHY_EVALUATORS_V1.murphy_0028_0029_evaluator import evaluate_0028
from MURPHY_EVALUATORS_V1.murphy_0050_evaluator import evaluate_0050


def test_0028_confirmed_bearish_high_passes():
    result = evaluate_0028({"divergence_type": "BEARISH", "pivot_type": "HIGH"})
    assert result["status"] == "PASS"
    assert result["directional_confirmation"] == "BEARISH_WARNING"


def test_0028_wrong_direction_fails():
    result = evaluate_0028({"divergence_type": "BULLISH", "pivot_type": "HIGH"})
    assert result["status"] == "FAIL"


def test_0028_missing_evidence_is_not_evaluable():
    result = evaluate_0028({"divergence_type": None, "pivot_type": "HIGH"})
    assert result["status"] == "NOT_EVALUABLE"


def test_0050_complete_checklist_passes_without_direction():
    fields = {
        "general_trend": "PASS",
        "sector_direction": "PASS",
        "weekly_monthly_review": "PASS",
        "support_resistance_trendlines": "PASS",
        "volume_open_interest": "PASS",
        "retracements_gaps": "PASS",
        "reversal_continuation_patterns": "PASS",
        "moving_averages_oscillators": "PASS",
    }
    result = evaluate_0050(fields)
    assert result["status"] == "PASS"
    assert result["direction"] == "NONE"


def test_0050_partial_checklist_blocks_closed():
    result = evaluate_0050({"volume_open_interest": "PASS"})
    assert result["status"] == "NOT_EVALUABLE"
    assert result["direction"] == "NONE"
