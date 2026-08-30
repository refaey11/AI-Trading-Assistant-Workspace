from dataclasses import dataclass
from typing import Optional
import math

# Preserved from the existing Risk Engine V1 research policy where compatible.
BASE_RISK_PCT = 0.005
AFTER_TWO_LOSSES_RISK_PCT = 0.0025
MAX_RISK_PCT = 0.015
MIN_STOP_ATR = 0.5
MAX_STOP_ATR = 4.0
DRAWDOWN_BREAKER_PCT = 0.05

# Reconciled from the existing frozen execution contract:
# the recovered execution adapter explicitly derives a 2R target.
# The recovered Risk Engine V1 research prototype itself uses 1.5R, but is
# documented as research-only and is not the current execution target.
CURRENT_CANONICAL_MIN_RR = 2.0
RR_ABS_TOLERANCE = 1e-12
RR_REL_TOLERANCE = 1e-12


@dataclass(frozen=True)
class RiskResult:
    risk_pass: bool
    risk_percent: float
    stop_distance: Optional[float]
    rr: Optional[float]
    position_size: Optional[float]
    reason: str
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


def evaluate_risk(
    *,
    equity: float,
    entry: float,
    stop_loss: Optional[float],
    take_profit: Optional[float],
    atr: Optional[float],
    prior_loss_streak: int,
    peak_equity: float,
    risk_budget_pct: Optional[float] = None,
) -> RiskResult:
    """Validate the existing hard-gate contract without inventing SL/TP semantics.

    Numeric SL/TP/ATR must be supplied by the upstream execution component.
    """
    if equity <= 0 or peak_equity <= 0 or entry <= 0:
        return RiskResult(False, 0.0, None, None, None, "INVALID_EQUITY_OR_ENTRY")

    risk_pct = (
        risk_budget_pct
        if risk_budget_pct is not None
        else (AFTER_TWO_LOSSES_RISK_PCT if prior_loss_streak >= 2 else BASE_RISK_PCT)
    )
    if risk_pct <= 0 or risk_pct > MAX_RISK_PCT:
        return RiskResult(False, 0.0, None, None, None, "RISK_BUDGET_INVALID", stop_loss, take_profit)

    drawdown = max(0.0, (peak_equity - equity) / peak_equity)
    if drawdown >= DRAWDOWN_BREAKER_PCT:
        return RiskResult(False, risk_pct, None, None, None, "DRAWDOWN_CIRCUIT_BREAKER", stop_loss, take_profit)

    if stop_loss is None or take_profit is None or atr is None or atr <= 0:
        return RiskResult(False, risk_pct, None, None, None, "MISSING_EXECUTION_INPUT", stop_loss, take_profit)

    stop_distance = abs(entry - stop_loss)
    if stop_distance <= 0:
        return RiskResult(False, risk_pct, stop_distance, None, None, "NON_POSITIVE_STOP_DISTANCE", stop_loss, take_profit)

    stop_atr = stop_distance / atr
    if stop_atr < MIN_STOP_ATR or stop_atr > MAX_STOP_ATR:
        return RiskResult(False, risk_pct, stop_distance, None, None, "STOP_DISTANCE_OUT_OF_RANGE", stop_loss, take_profit)

    target_distance = abs(take_profit - entry)
    rr = target_distance / stop_distance
    rr_ok = math.isclose(rr, CURRENT_CANONICAL_MIN_RR, rel_tol=RR_REL_TOLERANCE, abs_tol=RR_ABS_TOLERANCE) or rr > CURRENT_CANONICAL_MIN_RR
    if not rr_ok:
        return RiskResult(
            False,
            risk_pct,
            stop_distance,
            rr,
            None,
            "RR_BELOW_CURRENT_CANONICAL_MINIMUM",
            stop_loss,
            take_profit,
        )

    risk_money = equity * risk_pct
    position_size = risk_money / stop_distance
    return RiskResult(
        True,
        risk_pct,
        stop_distance,
        rr,
        position_size,
        "RISK_GATE_PASS",
        stop_loss,
        take_profit,
    )
