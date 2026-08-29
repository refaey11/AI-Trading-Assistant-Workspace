from dataclasses import dataclass
from math import isclose
from typing import Optional

BASE_RISK_PCT = 0.005
AFTER_TWO_LOSSES_RISK_PCT = 0.0025
MAX_RISK_PCT = 0.015
MIN_STOP_ATR = 0.5
MAX_STOP_ATR = 4.0
DRAWDOWN_BREAKER_PCT = 0.05
CURRENT_CANONICAL_MIN_RR = 3.0
RR_BOUNDARY_TOLERANCE = 1e-12

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


def evaluate_risk(*, equity: float, entry: float, stop_loss: Optional[float], take_profit: Optional[float], atr: Optional[float], prior_loss_streak: int, peak_equity: float, risk_budget_pct: Optional[float] = None) -> RiskResult:
    if equity <= 0 or peak_equity <= 0 or entry <= 0:
        return RiskResult(False, 0.0, None, None, None, "INVALID_EQUITY_OR_ENTRY", stop_loss, take_profit)
    risk_pct = risk_budget_pct if risk_budget_pct is not None else (AFTER_TWO_LOSSES_RISK_PCT if prior_loss_streak >= 2 else BASE_RISK_PCT)
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
    if rr < CURRENT_CANONICAL_MIN_RR and not isclose(rr, CURRENT_CANONICAL_MIN_RR, rel_tol=0.0, abs_tol=RR_BOUNDARY_TOLERANCE):
        return RiskResult(False, risk_pct, stop_distance, rr, None, "RR_BELOW_CURRENT_CANONICAL_MINIMUM", stop_loss, take_profit)
    return RiskResult(True, risk_pct, stop_distance, rr, (equity * risk_pct) / stop_distance, "RISK_GATE_PASS", stop_loss, take_profit)
