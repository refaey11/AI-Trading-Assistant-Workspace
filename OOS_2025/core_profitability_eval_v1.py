from __future__ import annotations
from typing import Any, Dict

from frozen_candidate_risk_profile_v1 import evaluate_frozen_candidate_risk


def _direction(value: Any) -> str:
    parts = {p for p in str(value or "").split("|") if p in {"BULLISH", "BEARISH"}}
    if parts == {"BULLISH"}:
        return "BUY"
    if parts == {"BEARISH"}:
        return "SELL"
    return "NO_TRADE"


def evaluate_event(event: Dict[str, Any], *, equity: float = 10000.0, peak_equity: float = 10000.0, prior_loss_streak: int = 0) -> Dict[str, Any]:
    """Evaluation-only core profitability gate.

    Murphy supplies the candidate direction. Nison is confirmation/context only:
    absence is allowed on the medium-confirmation path, but an explicit
    contradiction rejects the event. TIZ remains optional only in this isolated
    evaluation mode. The frozen candidate 0.75 ATR / 2R protocol is preserved.
    """
    direction = _direction(event.get("directional_confirmation"))
    if int(event.get("murphy_pass", 0) or 0) <= 0 or direction == "NO_TRADE":
        return {"status": "NO_TRADE", "reason": "MURPHY_SETUP_OR_DIRECTION_INVALID", "direction": direction}

    nison_status = str(event.get("nison_status", "NOT_EVALUABLE"))
    if nison_status in {"CONTRADICTORY", "CONTRADICTION", "FAIL_CONTRADICTION"}:
        return {"status": "NO_TRADE", "reason": "NISON_CONTRADICTION", "direction": direction}

    entry = event.get("entry_price", event.get("close", event.get("price")))
    atr = event.get("atr20", event.get("atr"))
    try:
        entry = float(entry)
        atr = float(atr)
    except (TypeError, ValueError):
        return {"status": "NO_TRADE", "reason": "MISSING_ENTRY_OR_ATR", "direction": direction}

    risk = evaluate_frozen_candidate_risk(
        direction=direction,
        equity=equity,
        peak_equity=peak_equity,
        entry=entry,
        atr=atr,
        prior_loss_streak=prior_loss_streak,
    )
    if not risk.risk_pass:
        return {"status": "NO_TRADE", "reason": risk.reason, "direction": direction, "risk_pass": False}

    return {
        "status": "ELIGIBLE_FOR_CORE_PROFITABILITY_BACKTEST",
        "reason": "CORE_EVAL_PASS",
        "direction": direction,
        "nison_status": nison_status,
        "tiz_verified": str(event.get("tiz_process_state", "NOT_EVALUABLE")) in {"PASS", "READY", "AVAILABLE"},
        "risk_pass": True,
        "risk_percent": risk.risk_percent,
        "entry_price": entry,
        "atr": atr,
        "stop_loss": risk.stop_loss,
        "take_profit": risk.take_profit,
        "position_size": risk.position_size,
    }
