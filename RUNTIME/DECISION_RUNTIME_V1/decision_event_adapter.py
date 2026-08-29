from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class WiringError(ValueError):
    pass


def _parse_ts(value: str) -> datetime:
    ts = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if ts.tzinfo is None:
        raise WiringError("timestamp must be timezone-aware")
    return ts.astimezone(timezone.utc)


def _check_as_of(item: Dict[str, Any], as_of: datetime, label: str) -> None:
    raw = item.get("timestamp") or item.get("signal_time") or item.get("as_of")
    if raw is None:
        raise WiringError(f"{label}: missing timestamp/as_of")
    if _parse_ts(raw) > as_of:
        raise WiringError(f"{label}: future evidence relative to event as_of")


def evidence(module: str, statement: str, direction: Optional[str], strength: Optional[str],
             available: bool, source_rule_id: Optional[str] = None) -> Dict[str, Any]:
    return {"module": module, "statement": statement, "direction": direction,
            "strength": strength, "available": available, "source_rule_id": source_rule_id}


def assemble_event(*, market: Dict[str, Any], murphy: List[Dict[str, Any]],
                   nison: List[Dict[str, Any]], memory: Dict[str, Any],
                   tiz: Optional[Dict[str, Any]], risk: Optional[Dict[str, Any]] = None,
                   symbol: str = "GBPUSD") -> Dict[str, Any]:
    raw = market.get("timestamp") or market.get("as_of")
    if not raw:
        raise WiringError("market: missing authoritative timestamp")
    as_of = _parse_ts(raw)
    _check_as_of(market, as_of, "market")
    for item in murphy:
        _check_as_of(item, as_of, "murphy")
    for item in nison:
        _check_as_of(item, as_of, "nison")
    if memory.get("timestamp") or memory.get("as_of"):
        _check_as_of(memory, as_of, "memory")
    if tiz and (tiz.get("timestamp") or tiz.get("as_of")):
        _check_as_of(tiz, as_of, "tiz")

    for item in murphy:
        if item.get("direction") not in {None, "BUY", "SELL", "NEUTRAL"}:
            raise WiringError("murphy: unsupported direction value")

    patterns = [str(x["candlestick_patterns"]) for x in nison if x.get("candlestick_patterns")]
    confirmation = "ABSENT"
    if any(x.get("candlestick_confirmed") is True for x in nison):
        confirmation = "CONFIRMED"
    elif nison:
        confirmation = "WEAK"

    tiz_payload = tiz if tiz is not None else {
        "process_state": "NOT_EVALUABLE", "rule_adherence": None,
        "risk_accepted": None, "impulse_override": None,
        "loss_chasing": None, "revenge_trade": None,
    }

    return {
        "signal": {"direction": "NO_TRADE", "confidence": 0.0, "status": "CANDIDATE"},
        "murphy": {
            "trend": market.get("trend", ""),
            "market_structure": market.get("structure_event", market.get("structure", "")),
            "support_resistance": market.get("location", ""), "pattern": "",
            "breakout_confirmed": False, "target_method": "",
        },
        "nison": {
            "candlestick_pattern": ",".join(patterns),
            "context": market.get("market_interpretation", ""),
            "confirmation": confirmation, "contradiction": any(x.get("contradiction") is True for x in nison),
        },
        "trading_zone": tiz_payload,
        "risk_engine": risk or {"risk_pass": False, "risk_percent": 0.0, "stop_loss": "",
                                   "take_profit": "", "rr": "", "position_size": ""},
        "decision": {"logic": "WIRING_ONLY: adapter does not generate direction",
                     "reasons_for": [], "reasons_against": [], "final": "NO_TRADE"},
        "audit": {"source_refs": [], "timestamp": as_of.isoformat(), "backtest_status": "UNTESTED"},
        "_meta": {"symbol": symbol, "as_of": as_of.isoformat(), "adapter": "wiring-only-v1"},
    }
