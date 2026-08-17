"""Murphy 0042-0045 portfolio risk adapter.
Source: Murphy Ch.16 Capital Allocation.
These are portfolio-level constraints, not trade-entry signals.
"""

SOURCE_GUIDELINES = {
    "MURPHY_0042": {"name": "capital_reserve", "max_total_investment": 0.50},
    "MURPHY_0043": {"name": "single_market_exposure", "source_range": (0.10, 0.15), "operational_max": 0.15},
    "MURPHY_0044": {"name": "max_risk_per_market", "max_risk": 0.05},
    "MURPHY_0045": {"name": "total_margin_limit", "source_range": (0.20, 0.25), "operational_max": 0.25},
}


def evaluate_0042(total_investment: float) -> bool:
    return 0 <= total_investment <= 0.50


def evaluate_0043(single_market_exposure: float) -> bool:
    return 0 <= single_market_exposure <= SOURCE_GUIDELINES["MURPHY_0043"]["operational_max"]


def evaluate_0044(risk_per_market: float) -> bool:
    return 0 <= risk_per_market <= 0.05


def evaluate_0045(total_margin: float) -> bool:
    return 0 <= total_margin <= SOURCE_GUIDELINES["MURPHY_0045"]["operational_max"]


def evaluate_portfolio(*, total_investment: float, single_market_exposure: float,
                       risk_per_market: float, total_margin: float) -> dict:
    checks = {
        "MURPHY_0042": evaluate_0042(total_investment),
        "MURPHY_0043": evaluate_0043(single_market_exposure),
        "MURPHY_0044": evaluate_0044(risk_per_market),
        "MURPHY_0045": evaluate_0045(total_margin),
    }
    return {"pass": all(checks.values()), "checks": checks}
