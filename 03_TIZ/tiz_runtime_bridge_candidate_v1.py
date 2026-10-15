"""Candidate-only TIZ runtime bridge.

This module is intentionally NOT authoritative and must not be promoted to
production without the existing project governance gates.

Role: normalize already-produced runtime evidence into the seven existing
Trading in the Zone rule inputs. It does not invent evidence, thresholds,
market direction, SL/TP mechanics, or producer semantics.
"""

RULE_OUTPUTS = {
    "PSY_0001": ("pre_trade_state_gate",),
    "PSY_0002": ("risk_acceptance",),
    "PSY_0003": ("post_trade_review",),
    "PSY_0004": ("pre_trade_state_gate",),
    "PSY_0005": ("loss_sequence_control",),
    "PSY_0006": ("post_trade_review",),
    "PSY_0007": ("rule_adherence", "no_impulsive_override"),
}

REQUIRED_EVIDENCE_META = ("value", "availability", "timestamp", "provenance", "state_semantics")


def normalize(runtime: dict) -> dict:
    """Return source-shaped evidence only; missing fields remain NOT_EVALUABLE."""
    out = {"direction": "NEUTRAL", "rules": {}}
    tiz = runtime.get("trading_zone") or {}
    for rule_id, fields in RULE_OUTPUTS.items():
        evidence = {}
        missing = False
        for field in fields:
            item = tiz.get(field)
            if not isinstance(item, dict) or not all(k in item for k in REQUIRED_EVIDENCE_META):
                missing = True
            evidence[field] = item
        out["rules"][rule_id] = {
            "state": "NOT_EVALUABLE" if missing else "AVAILABLE",
            "evidence": evidence,
        }
    return out


def can_generate_direction() -> bool:
    return False
