from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "brain_assessment_diagnostics",
    ROOT / "evaluation" / "brain_assessment_diagnostics_v1.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _row():
    return {
        "mtf_trend_score": 1,
        "M5_trend_regime": -1,
        "M15_trend_regime": -1,
        "M30_trend_regime": 0,
        "H1_trend_regime": 1,
        "H4_trend_regime": 1,
        "D1_trend_regime": 1,
    }


def test_detects_mixed_regime_votes_even_when_aggregate_score_is_bullish():
    result = MODULE.diagnose_brain_assessment(
        _row(),
        {"directional_bias": "bullish", "confidence": 1.0, "evidence": []},
    )
    mtf = result["mtf"]
    assert mtf["vote_counts"] == {"bearish": 2, "neutral": 1, "bullish": 3}
    assert mtf["vote_direction"] == "bullish"
    assert mtf["score_direction"] == "bullish"
    assert mtf["both_bullish_and_bearish_regimes_present"] is True
    assert result["diagnostic_only"] is True
    assert result["direction_generation"] is False


def test_flags_aggregate_score_disagreement_with_majority_regime_votes():
    row = _row()
    row["mtf_trend_score"] = -1
    result = MODULE.diagnose_brain_assessment(row, {"evidence": []})
    assert result["mtf"]["score_vs_regime_vote_disagreement"] is True


def test_reports_missing_regime_fields_without_imputing_them():
    row = _row()
    row["H4_trend_regime"] = None
    result = MODULE.diagnose_brain_assessment(row, {"evidence": []})
    assert result["mtf"]["available_regime_count"] == 5
    assert result["mtf"]["missing_regime_fields"] == ["H4_trend_regime"]


def test_exposes_neutral_evidence_excluded_from_directional_confidence():
    assessment = {
        "confidence": 1.0,
        "evidence": [
            {"direction": "bullish", "strength": 1.0},
            {"direction": "neutral", "strength": 0.35},
            {"direction": "neutral", "strength": 0.0},
        ],
    }
    result = MODULE.diagnose_brain_assessment(_row(), assessment)
    audit = result["confidence_audit"]
    assert audit["reproduced_directional_confidence"] == 1.0
    assert audit["neutral_evidence_count"] == 2
    assert audit["neutral_strength_excluded_from_directional_denominator"] == 0.35
    assert "not a calibrated probability" in audit["note"]


def test_flags_no_trade_reason_handoff_gap_but_does_not_decide():
    assessment = {"no_trade_reasons": ["Volume confirmation is unavailable."]}
    result = MODULE.diagnose_brain_assessment(_row(), assessment, {"final": "SELL"})
    audit = result["no_trade_handoff_audit"]
    assert audit["reasons_present_but_directional_decision_returned"] is True
    assert result["decision_authority"] is False


def test_no_trade_reasons_are_not_a_gap_when_final_decision_is_no_trade():
    assessment = {"no_trade_reasons": ["Volume confirmation is unavailable."]}
    result = MODULE.diagnose_brain_assessment(_row(), assessment, {"final": "NO_TRADE"})
    assert result["no_trade_handoff_audit"]["reasons_present_but_directional_decision_returned"] is False


def test_reproduces_brain_v1_structure_mean_and_flags_volume_no_trade_reason():
    row = {
        "mtf_trend_score": 1,
        "M5_trend_regime": -1,
        "M15_trend_regime": -1,
        "M30_trend_regime": 0,
        "H1_trend_regime": 1,
        "H4_trend_regime": 1,
        "D1_trend_regime": 1,
    }
    assessment = {
        "directional_bias": "bullish",
        "confidence": 1.0,
        "evidence": [
            {"module": "MTF", "direction": "bullish", "strength": 1.0},
            {"module": "Structure", "direction": "neutral", "strength": 0.35},
            {"module": "Volume", "direction": "neutral", "strength": 0.0},
        ],
        "no_trade_reasons": [
            "Volume confirmation is unavailable for this historical regime."
        ],
    }
    result = MODULE.diagnose_brain_assessment(
        row,
        assessment,
        {"final": "NO_TRADE"},
        {"eligible": True, "hard_blocks": [], "needs_review": []},
    )
    assert result["mtf"]["regime_mean"] == 1.0 / 6.0
    assert result["mtf"]["structure_direction_using_brain_v1_threshold"] == "neutral"
    assert result["confidence_audit"]["reproduced_directional_confidence"] == 1.0
    assert result["no_trade_handoff_audit"]["eligible_while_brain_reports_no_trade_reasons"] is True
    assert result["no_trade_handoff_audit"]["reasons_present_but_directional_decision_returned"] is False
