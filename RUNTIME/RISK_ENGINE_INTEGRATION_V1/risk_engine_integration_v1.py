from dataclasses import dataclass
from math import isclose, isfinite
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
    try:
        equity, entry, peak_equity = float(equity), float(entry), float(peak_equity)
        loss_streak = float(prior_loss_streak)
    except (TypeError, ValueError, OverflowError):
        return RiskResult(False, 0.0, None, None, None, "INVALID_EQUITY_OR_ENTRY", stop_loss, take_profit)
    if not all(isfinite(value) for value in (equity, entry, peak_equity, loss_streak)):
        return RiskResult(False, 0.0, None, None, None, "INVALID_EQUITY_OR_ENTRY", stop_loss, take_profit)
    if equity <= 0 or peak_equity <= 0 or entry <= 0:
        return RiskResult(False, 0.0, None, None, None, "INVALID_EQUITY_OR_ENTRY", stop_loss, take_profit)
    try:
        risk_pct = float(risk_budget_pct) if risk_budget_pct is not None else (AFTER_TWO_LOSSES_RISK_PCT if loss_streak >= 2 else BASE_RISK_PCT)
    except (TypeError, ValueError, OverflowError):
        return RiskResult(False, 0.0, None, None, None, "RISK_BUDGET_INVALID", stop_loss, take_profit)
    if not isfinite(risk_pct) or risk_pct <= 0 or risk_pct > MAX_RISK_PCT:
        return RiskResult(False, 0.0, None, None, None, "RISK_BUDGET_INVALID", stop_loss, take_profit)
    drawdown = max(0.0, (peak_equity - equity) / peak_equity)
    if drawdown >= DRAWDOWN_BREAKER_PCT:
        return RiskResult(False, risk_pct, None, None, None, "DRAWDOWN_CIRCUIT_BREAKER", stop_loss, take_profit)
    if stop_loss is None or take_profit is None or atr is None:
        return RiskResult(False, risk_pct, None, None, None, "MISSING_EXECUTION_INPUT", stop_loss, take_profit)
    try:
        stop_loss, take_profit, atr = float(stop_loss), float(take_profit), float(atr)
    except (TypeError, ValueError, OverflowError):
        return RiskResult(False, risk_pct, None, None, None, "NON_FINITE_EXECUTION_INPUT", stop_loss, take_profit)
    if not all(isfinite(value) for value in (stop_loss, take_profit, atr)):
        return RiskResult(False, risk_pct, None, None, None, "NON_FINITE_EXECUTION_INPUT", stop_loss, take_profit)
    if atr <= 0:
        return RiskResult(False, risk_pct, None, None, None, "MISSING_EXECUTION_INPUT", stop_loss, take_profit)
    stop_distance = abs(entry - stop_loss)
    if stop_distance <= 0:
        return RiskResult(False, risk_pct, stop_distance, None, None, "NON_POSITIVE_STOP_DISTANCE", stop_loss, take_profit)
    # A valid bracket must put stop-loss and take-profit on opposite sides of entry.
    # This check is direction-agnostic: it accepts either a long or a short bracket.
    if (stop_loss < entry and take_profit <= entry) or (stop_loss > entry and take_profit >= entry):
        return RiskResult(False, risk_pct, stop_distance, None, None, "INVALID_STOP_TARGET_ORIENTATION", stop_loss, take_profit)
    stop_atr = stop_distance / atr
    if not isfinite(stop_atr):
        return RiskResult(False, risk_pct, stop_distance, None, None, "NON_FINITE_STOP_DISTANCE", stop_loss, take_profit)
    if stop_atr < MIN_STOP_ATR or stop_atr > MAX_STOP_ATR:
        return RiskResult(False, risk_pct, stop_distance, None, None, "STOP_DISTANCE_OUT_OF_RANGE", stop_loss, take_profit)
    target_distance = abs(take_profit - entry)
    rr = target_distance / stop_distance
    if not isfinite(rr):
        return RiskResult(False, risk_pct, stop_distance, rr, None, "NON_FINITE_RR", stop_loss, take_profit)
    if isclose(rr, CURRENT_CANONICAL_MIN_RR, rel_tol=0.0, abs_tol=RR_BOUNDARY_TOLERANCE):
        rr = CURRENT_CANONICAL_MIN_RR
    if rr < CURRENT_CANONICAL_MIN_RR:
        return RiskResult(False, risk_pct, stop_distance, rr, None, "RR_BELOW_CURRENT_CANONICAL_MINIMUM", stop_loss, take_profit)
    position_size = (equity * risk_pct) / stop_distance
    if not isfinite(position_size):
        return RiskResult(False, risk_pct, stop_distance, rr, None, "NON_FINITE_POSITION_SIZE", stop_loss, take_profit)
    return RiskResult(True, risk_pct, stop_distance, rr, position_size, "RISK_GATE_PASS", stop_loss, take_profit)
