"""Normalize existing pre-entry Trading-in-the-Zone evidence.

This adapter does not invent psychological semantics, thresholds, direction,
SL/TP, or risk rules. It only copies explicitly produced evidence into the
Decision Schema shape. Missing evidence remains NOT_EVALUABLE.
"""

REQUIRED_META = ("value", "availability", "timestamp", "provenance", "state_semantics")


def _is_envelope(value):
    return isinstance(value, dict) and all(k in value for k in REQUIRED_META)


def normalize_preentry(record: dict) -> dict:
    tz = record.get("trading_zone") or {}
    fields = (
        "process_state",
        "rule_adherence",
        "risk_accepted",
        "impulse_override",
        "loss_chasing",
        "revenge_trade",
    )
    out = {}
    missing = []
    for field in fields:
        item = tz.get(field)
        if not _is_envelope(item):
            missing.append(field)
        out[field] = item

    return {
        "process_state": out["process_state"],
        "rule_adherence": out["rule_adherence"],
        "risk_accepted": out["risk_accepted"],
        "impulse_override": out["impulse_override"],
        "loss_chasing": out["loss_chasing"],
        "revenge_trade": out["revenge_trade"],
        "state": "NOT_EVALUABLE" if missing else "AVAILABLE",
        "missing": missing,
        "direction": "NEUTRAL",
    }
