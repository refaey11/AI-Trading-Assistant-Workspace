"""Murphy 0042-0045 risk-rule evaluators + Risk Engine gate adapter.

Source: Murphy Ch.16 Capital Allocation.
The numeric rule semantics are source-derived; the adapter itself does not
infer PASS from text or from missing evidence. The existing Risk Engine remains
the authoritative hard gate.
"""

SOURCE_GUIDELINES = {
    "MURPHY_0042": {"name": "capital_reserve", "max_total_investment": 0.50},
    "MURPHY_0043": {"name": "single_market_exposure", "source_range": (0.10, 0.15), "operational_upper_bound": 0.15},
    "MURPHY_0044": {"name": "max_risk_per_market", "max_risk": 0.05},
    "MURPHY_0045": {"name": "total_margin_limit", "source_range": (0.20, 0.25), "operational_upper_bound": 0.25},
}


def evaluate_0042(total_investment: float) -> bool:
    return 0 <= total_investment <= 0.50


def evaluate_0043(single_market_exposure: float) -> bool:
    return 0 <= single_market_exposure <= 0.15


def evaluate_0044(risk_per_market: float) -> bool:
    return 0 <= risk_per_market <= 0.05


def evaluate_0045(total_margin: float) -> bool:
    return 0 <= total_margin <= 0.25


def evaluate_portfolio(*, total_investment: float, single_market_exposure: float,
                       risk_per_market: float, total_margin: float) -> dict:
    checks = {
        "MURPHY_0042": evaluate_0042(total_investment),
        "MURPHY_0043": evaluate_0043(single_market_exposure),
        "MURPHY_0044": evaluate_0044(risk_per_market),
        "MURPHY_0045": evaluate_0045(total_margin),
    }
    return {"pass": all(checks.values()), "checks": checks}


def normalize_risk_gate(*, rule_id: str, risk_status: str,
                        risk_available: bool, risk_evidence: dict | None = None) -> dict:
    """Normalize authoritative Risk Engine evidence into Rule Adapter output.

    PASS/FAIL must come from the authoritative risk producer. Missing evidence
    never becomes PASS. This function does not calculate risk from text.
    """
    allowed_rules = {"MURPHY_0042", "MURPHY_0043", "MURPHY_0044", "MURPHY_0045"}
    if rule_id not in allowed_rules:
        raise ValueError("unsupported Murphy risk rule")

    status = risk_status.upper()
    if not risk_available or status not in {"PASS", "FAIL", "NOT_EVALUABLE"}:
        return {"module": "murphy_risk", "source_rule_id": rule_id, "available": False,
                "gate": "needs_review", "conflict": "insufficient",
                "statement": "Required authoritative risk evidence is unavailable or unsupported."}

    if status == "PASS":
        return {"module": "murphy_risk", "source_rule_id": rule_id, "available": True,
                "gate": "pass", "conflict": "neutral",
                "statement": (risk_evidence or {}).get("statement", "Authoritative risk evidence passed.")}

    if status == "FAIL":
        return {"module": "murphy_risk", "source_rule_id": rule_id, "available": True,
                "gate": "fail", "conflict": "neutral",
                "statement": (risk_evidence or {}).get("statement", "Authoritative risk evidence failed.")}

    return {"module": "murphy_risk", "source_rule_id": rule_id, "available": False,
            "gate": "needs_review", "conflict": "insufficient",
            "statement": "Risk rule is not evaluable from the available authoritative evidence."}
