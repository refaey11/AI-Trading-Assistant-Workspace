from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

BASE_RISK_PCT = 0.005
AFTER_TWO_LOSSES_RISK_PCT = 0.0025
MAX_RISK_PCT = 0.015
DRAWDOWN_BREAKER_PCT = 0.05
SL_ATR = 0.75
TP_R = 2.0


@dataclass(frozen=True)
class FrozenCandidateRiskResult:
    risk_pass: bool
    risk_percent: float
    stop_loss: Optional[float]
    take_profit: Optional[float]
    position_size: Optional[float]
    reason: str


def evaluate_frozen_candidate_risk(*, direction: str, equity: float, peak_equity: float, entry: float, atr: float, prior_loss_streak: int = 0, risk_budget_pct: Optional[float] = None) -> FrozenCandidateRiskResult:
    """Evaluation-only risk profile for the already-recorded V2+4H candidate.

    This preserves the stored 0.75 ATR / 2R candidate protocol and must not be
    used to redefine the canonical Risk Engine or the canonical three-book mode.
    """
    if direction not in {"BUY", "SELL"}:
        return FrozenCandidateRiskResult(False, 0.0, None, None, None, "INVALID_DIRECTION")
    if equity <= 0 or peak_equity <= 0 or entry <= 0 or atr <= 0:
        return FrozenCandidateRiskResult(False, 0.0, None, None, None, "INVALID_EXECUTION_INPUT")

    risk_pct = risk_budget_pct if risk_budget_pct is not None else (AFTER_TWO_LOSSES_RISK_PCT if prior_loss_streak >= 2 else BASE_RISK_PCT)
    if risk_pct <= 0 or risk_pct > MAX_RISK_PCT:
        return FrozenCandidateRiskResult(False, 0.0, None, None, None, "RISK_BUDGET_INVALID")

    drawdown = max(0.0, (peak_equity - equity) / peak_equity)
    if drawdown >= DRAWDOWN_BREAKER_PCT:
        return FrozenCandidateRiskResult(False, risk_pct, None, None, None, "DRAWDOWN_CIRCUIT_BREAKER")

    stop_distance = SL_ATR * atr
    reward_distance = TP_R * stop_distance
    if direction == "BUY":
        stop_loss = entry - stop_distance
        take_profit = entry + reward_distance
    else:
        stop_loss = entry + stop_distance
        take_profit = entry - reward_distance

    position_size = (equity * risk_pct) / stop_distance
    return FrozenCandidateRiskResult(True, risk_pct, stop_loss, take_profit, position_size, "FROZEN_CANDIDATE_RISK_PASS")
