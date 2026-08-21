# RUN 073 — Market Pipeline Evidence Normalization Adapter
# Normalizes existing Market Pipeline artifacts without modifying source modules.
# It emits evidence only. It does not generate BUY/SELL, entry, SL, TP, or position size.

_DIRECTION = {
    "BULL": "bullish", "BULLISH": "bullish", "UP": "bullish", "UPTREND": "bullish",
    "BEAR": "bearish", "BEARISH": "bearish", "DOWN": "bearish", "DOWNTREND": "bearish",
    "NEUTRAL": "neutral", "SIDEWAYS": "neutral", "RANGE": "neutral",
    "MIXED": "mixed", "TRANSITION": "mixed", "UNKNOWN": "unknown"
}

def _direction(value):
    if value is None:
        return "unknown"
    text = str(value).upper()
    for key, normalized in _DIRECTION.items():
        if key in text:
            return normalized
    return "unknown"

def _strength_from_state(value):
    text = str(value or "").upper()
    if text in {"NORMAL", "CONTRACTION", "EXPANSION"}:
        return "moderate"
    if text in {"UNKNOWN", ""}:
        return "none"
    return "weak"

def _evidence(module, evidence_type, statement, direction, strength, available,
              pair, timestamp, timeframe, oos_status, source_ref, metadata=None):
    return {
        "module": module,
        "evidence_type": evidence_type,
        "statement": statement,
        "direction": direction,
        "strength": strength,
        "available": bool(available),
        "pair": pair,
        "timestamp": timestamp,
        "timeframe": timeframe,
        "oos_status": oos_status,
        "source_ref": source_ref,
        "metadata": metadata or {}
    }

def normalize_market_pipeline(state_row, mtf_row, scenario_row, query_mode="runtime"):
    pair = state_row.get("pair")
    timestamp = state_row.get("timestamp")
    year = str(timestamp)[:4] if timestamp else None
    oos_status = "OOS_2025_READ_ONLY" if year == "2025" else "NON_2025"
    evidence = []

    trend = state_row.get("trend")
    evidence.append(_evidence("market_state_reader", "trend", f"Market State trend={trend}", _direction(trend), "moderate", trend is not None, pair, timestamp, "H1", oos_status, "LATEST_MARKET_READINGS.json"))

    structure = state_row.get("structure")
    evidence.append(_evidence("market_state_reader", "structure", f"Market structure={structure}", _direction(structure), "moderate", structure is not None, pair, timestamp, "H1", oos_status, "LATEST_MARKET_READINGS.json"))

    volatility = state_row.get("volatility")
    evidence.append(_evidence("market_state_reader", "volatility", f"Volatility={volatility}", "neutral", _strength_from_state(volatility), volatility is not None, pair, timestamp, "H1", oos_status, "LATEST_MARKET_READINGS.json"))

    volume = state_row.get("volume")
    evidence.append(_evidence("market_state_reader", "volume", f"Volume state={volume}", "neutral", _strength_from_state(volume), volume is not None, pair, timestamp, "H1", oos_status, "LATEST_MARKET_READINGS.json"))

    for candle in ["bull_engulf", "bear_engulf", "hammer", "shooting_star"]:
        value = state_row.get(candle)
        direction = "bullish" if candle in {"bull_engulf", "hammer"} else "bearish"
        evidence.append(_evidence("market_state_reader", "candlestick", f"{candle}={value}", direction if value is True else "neutral", "moderate" if value is True else "none", value is not None, pair, timestamp, "H1", oos_status, "LATEST_MARKET_READINGS.json"))

    evidence.append(_evidence("multi_timeframe_reader", "higher_timeframe_context", f"H4 trend={mtf_row.get('H4_trend')}; H4 structure={mtf_row.get('H4_structure')}", _direction(mtf_row.get("H4_trend")), "moderate", mtf_row.get("H4_trend") is not None, pair, timestamp, "H4", oos_status, "LATEST_MTF_READINGS.json", {"role": "higher_timeframe_context"}))
    evidence.append(_evidence("multi_timeframe_reader", "local_structure", f"H1 trend={mtf_row.get('H1_trend')}; H1 structure={mtf_row.get('H1_structure')}", _direction(mtf_row.get("H1_trend")), "moderate", mtf_row.get("H1_trend") is not None, pair, timestamp, "H1", oos_status, "LATEST_MTF_READINGS.json", {"role": "local_structure"}))
    evidence.append(_evidence("multi_timeframe_reader", "mtf_alignment", f"MTF state={mtf_row.get('MTF_state')}", _direction(mtf_row.get("MTF_state")), "moderate", mtf_row.get("MTF_state") is not None, pair, timestamp, "H4/H1", oos_status, "LATEST_MTF_READINGS.json"))

    scenario = scenario_row.get("scenario_analysis", {})
    evidence.append(_evidence("market_scenario_engine", "scenario_context", f"Primary scenario={scenario.get('primary_scenario')}; source decision={scenario.get('decision')}", _direction(scenario.get("primary_scenario")), "weak", scenario.get("primary_scenario") is not None, pair, timestamp, "context", oos_status, "MARKET_SCENARIOS.json", {"candidate_context_only": True, "source_decision": scenario.get("decision"), "source_confidence": scenario.get("confidence"), "required_confirmation": scenario.get("required_confirmation")}))

    missing = []
    for name, value in {"H4_volume_ratio": mtf_row.get("H4_volume_ratio"), "H1_volume_ratio": mtf_row.get("H1_volume_ratio")}.items():
        if value in (None, 0, 0.0):
            missing.append(name)

    warnings = []
    if missing:
        warnings.append({"code": "FEATURE_COVERAGE_WARNING", "message": "Volume ratios are absent/zero and are not interpreted as directional confirmation.", "fields": missing})
    warnings.append({"code": "M15_UNAVAILABLE", "message": "M15 is not fabricated from H1 and remains unavailable until real approved M15 data exists."})

    return {
        "status": "OOS_READ_ONLY" if oos_status == "OOS_2025_READ_ONLY" else "OK",
        "pair": pair,
        "timestamp": timestamp,
        "oos_status": oos_status,
        "time_context": {"H4": "higher_timeframe_context", "H1": "local_structure", "M15": "unavailable_requires_real_data", "standalone_time_engine": "not_implemented"},
        "evidence": evidence,
        "candidate_context": {"available": True, "binding": False, "final_decision_generated": False},
        "final_decision": None,
        "execution_fields_generated": False,
        "warnings": warnings,
        "next_layer": "knowledge_alignment"
    }
