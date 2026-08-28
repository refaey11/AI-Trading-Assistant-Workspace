from __future__ import annotations

"""Adapter over the existing TIZ process gate.

Historical market data cannot manufacture private psychological state. Missing
process evidence therefore remains NOT_EVALUABLE. TIZ is neutral, never
creates direction, and never overrides technical direction.
"""
import argparse
import json
from typing import Any
from pathlib import Path

from RUNTIME.TIZ_PROCESS_GATE_V1.tiz_process_gate_v1 import evaluate_tiz_gate

FIELDS = ("rule_adherence", "risk_accepted", "impulse_override", "loss_chasing", "revenge_trade")


def evaluate(process: dict[str, Any] | None) -> dict[str, Any]:
    p = process or {}
    missing = [k for k in FIELDS if k not in p or p[k] is None]
    if missing:
        return {"status": "NOT_EVALUABLE", "direction": "NEUTRAL", "direction_generated": False,
                "reason": "MISSING_PROCESS_EVIDENCE:" + ",".join(missing)}
    r = evaluate_tiz_gate(
        rule_adherence=bool(p["rule_adherence"]),
        risk_accepted=bool(p["risk_accepted"]),
        impulse_override=bool(p["impulse_override"]),
        loss_chasing=bool(p["loss_chasing"]),
        revenge_trade=bool(p["revenge_trade"]),
    )
    return {"status": r.process_state, "direction": "NEUTRAL", "direction_generated": False,
            "reason": r.reason, "rule_adherence": r.rule_adherence,
            "risk_accepted": r.risk_accepted, "impulse_override": r.impulse_override,
            "loss_chasing": r.loss_chasing, "revenge_trade": r.revenge_trade}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8")) if args.input else {}
    result = evaluate(payload)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
