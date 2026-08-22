from dataclasses import dataclass


@dataclass(frozen=True)
class TIZGateResult:
    process_state: str
    rule_adherence: bool
    risk_accepted: bool
    impulse_override: bool
    loss_chasing: bool
    revenge_trade: bool
    reason: str


def evaluate_tiz_gate(*, rule_adherence: bool, risk_accepted: bool,
                      impulse_override: bool, loss_chasing: bool,
                      revenge_trade: bool) -> TIZGateResult:
    """Contract-derived TIZ gate.

    Uses only the existing Decision Schema / Three-Book contract fields.
    It cannot create direction and contains no psychological numeric threshold.
    """
    values = {
        "rule_adherence": bool(rule_adherence),
        "risk_accepted": bool(risk_accepted),
        "impulse_override": bool(impulse_override),
        "loss_chasing": bool(loss_chasing),
        "revenge_trade": bool(revenge_trade),
    }
    ready = (
        values["rule_adherence"]
        and values["risk_accepted"]
        and not values["impulse_override"]
        and not values["loss_chasing"]
        and not values["revenge_trade"]
    )
    if ready:
        return TIZGateResult("READY", **values, reason="PROCESS_GATE_PASS")
    failed = [
        k for k, v in values.items()
        if (k in {"rule_adherence", "risk_accepted"} and not v)
        or (k in {"impulse_override", "loss_chasing", "revenge_trade"} and v)
    ]
    return TIZGateResult(
        "NOT_READY", **values,
        reason="PROCESS_GATE_FAIL:" + ",".join(failed),
    )
