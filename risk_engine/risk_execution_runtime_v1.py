from __future__ import annotations
from dataclasses import dataclass
from math import isfinite

ALLOWED_RISK_PROFILES = (0.0025, 0.005, 0.01, 0.015)
ALLOWED_STOP_MODES = ("structure", "2x ATR", "hybrid")

@dataclass(frozen=True)
class RiskRequest:
    equity: float
    risk_percent: float
    entry_price: float
    stop_distance: float
    take_profit_distance: float
    stop_mode: str
    risk_budget_locked: bool

@dataclass(frozen=True)
class RiskResult:
    risk_pass: bool
    reason: str
    risk_money: float | None
    position_size: float | None
    stop_loss: float | None
    take_profit: float | None

def evaluate_risk(req: RiskRequest, direction: str, atr: float) -> RiskResult:
    vals = (req.equity, req.risk_percent, req.entry_price, req.stop_distance, req.take_profit_distance, atr)
    if not all(isfinite(float(v)) for v in vals):
        return RiskResult(False, "NON_FINITE_INPUT", None, None, None, None)
    if direction not in {"BUY", "SELL"}:
        return RiskResult(False, "INVALID_DIRECTION", None, None, None, None)
    if req.equity <= 0:
        return RiskResult(False, "NON_POSITIVE_EQUITY", None, None, None, None)
    if req.risk_percent not in ALLOWED_RISK_PROFILES:
        return RiskResult(False, "RISK_PROFILE_NOT_FROZEN", None, None, None, None)
    if req.stop_mode not in ALLOWED_STOP_MODES:
        return RiskResult(False, "STOP_MODE_NOT_SUPPORTED", None, None, None, None)
    if req.stop_distance <= 0:
        return RiskResult(False, "NON_POSITIVE_STOP_DISTANCE", None, None, None, None)
    if req.take_profit_distance <= 0:
        return RiskResult(False, "TAKE_PROFIT_UNDEFINED", None, None, None, None)
    if not req.risk_budget_locked:
        return RiskResult(False, "RISK_BUDGET_NOT_LOCKED", None, None, None, None)
    if atr <= 0:
        return RiskResult(False, "INVALID_ATR", None, None, None, None)
    ratio = req.stop_distance / atr
    if ratio < 0.5 or ratio > 4.0:
        return RiskResult(False, "STOP_DISTANCE_OUTSIDE_0_5_TO_4_ATR", None, None, None, None)
    risk_money = req.equity * req.risk_percent
    position_size = risk_money / req.stop_distance
    if direction == "BUY":
        sl = req.entry_price - req.stop_distance
        tp = req.entry_price + req.take_profit_distance
    else:
        sl = req.entry_price + req.stop_distance
        tp = req.entry_price - req.take_profit_distance
    return RiskResult(True, "PASS", risk_money, position_size, sl, tp)
