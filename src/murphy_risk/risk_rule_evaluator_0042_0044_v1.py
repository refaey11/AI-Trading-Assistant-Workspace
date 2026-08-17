"""Source-backed Murphy 0042-0044 risk gate.

This is a rule-specific evaluator over caller-supplied authoritative Risk Engine
measurements. It does not create a risk engine, position-sizing model, or stop
mechanics. 0043 preserves the source's 10-15% range: values above 15% fail;
values inside the range pass; values below 10% are NOT_EVALUABLE because the
source guideline does not establish a project violation for being below the
lower guideline boundary.
"""
from typing import Literal, Optional

Status = Literal["PASS", "FAIL", "NOT_EVALUABLE"]


def evaluate_0042(total_investment_pct: Optional[float], available: bool = True) -> Status:
    if not available or total_investment_pct is None:
        return "NOT_EVALUABLE"
    return "PASS" if total_investment_pct <= 50.0 else "FAIL"


def evaluate_0043(single_market_entry_pct: Optional[float], available: bool = True) -> Status:
    if not available or single_market_entry_pct is None:
        return "NOT_EVALUABLE"
    if single_market_entry_pct > 15.0:
        return "FAIL"
    if 10.0 <= single_market_entry_pct <= 15.0:
        return "PASS"
    return "NOT_EVALUABLE"


def evaluate_0044(single_market_risk_pct: Optional[float], available: bool = True) -> Status:
    if not available or single_market_risk_pct is None:
        return "NOT_EVALUABLE"
    return "PASS" if single_market_risk_pct <= 5.0 else "FAIL"


def evaluate(rule_id: str, value_pct: Optional[float], available: bool = True) -> Status:
    if rule_id == "0042":
        return evaluate_0042(value_pct, available)
    if rule_id == "0043":
        return evaluate_0043(value_pct, available)
    if rule_id == "0044":
        return evaluate_0044(value_pct, available)
    return "NOT_EVALUABLE"
