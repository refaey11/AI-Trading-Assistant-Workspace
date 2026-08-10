from typing import Dict, Any, Optional


def _not_evaluable(rule_id: str) -> Dict[str, Any]:
    return {"rule_id": rule_id, "status": "NOT_EVALUABLE", "direction": "NONE"}


def evaluate_0003(
    current_reaction_peak: Optional[float],
    prior_reaction_peak: Optional[float],
    current_reaction_trough: Optional[float],
    prior_reaction_trough: Optional[float],
) -> Dict[str, Any]:
    """Murphy 0003: successive reaction peaks AND troughs are higher."""
    if any(v is None for v in (current_reaction_peak, prior_reaction_peak, current_reaction_trough, prior_reaction_trough)):
        return _not_evaluable("MURPHY_0003")
    peaks_higher = current_reaction_peak > prior_reaction_peak
    troughs_higher = current_reaction_trough > prior_reaction_trough
    ok = peaks_higher and troughs_higher
    return {
        "rule_id": "MURPHY_0003",
        "status": "PASS" if ok else "FAIL",
        "direction": "BULLISH_STRUCTURE" if ok else "NONE",
        "peaks_higher": peaks_higher,
        "troughs_higher": troughs_higher,
    }


def evaluate_0004(
    current_reaction_peak: Optional[float],
    prior_reaction_peak: Optional[float],
    current_reaction_trough: Optional[float],
    prior_reaction_trough: Optional[float],
) -> Dict[str, Any]:
    """Murphy 0004: successive reaction peaks AND troughs are lower."""
    if any(v is None for v in (current_reaction_peak, prior_reaction_peak, current_reaction_trough, prior_reaction_trough)):
        return _not_evaluable("MURPHY_0004")
    peaks_lower = current_reaction_peak < prior_reaction_peak
    troughs_lower = current_reaction_trough < prior_reaction_trough
    ok = peaks_lower and troughs_lower
    return {
        "rule_id": "MURPHY_0004",
        "status": "PASS" if ok else "FAIL",
        "direction": "BEARISH_STRUCTURE" if ok else "NONE",
        "peaks_lower": peaks_lower,
        "troughs_lower": troughs_lower,
    }
