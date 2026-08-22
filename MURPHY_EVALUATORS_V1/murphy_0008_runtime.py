"""Runtime adapter for Murphy 0008.

Source boundary: the canonical 0006-0008 freeze artifacts do NOT approve a
numeric or generic operational definition for 'decisively broken'. The rule
therefore fails closed until an approved PF-B1 binding explicitly defines the
break condition.
"""


def evaluate_0008(*_args, **_kwargs):
    return {
        "rule_id": "MURPHY_0008",
        "status": "NOT_EVALUABLE",
        "directional_confirmation": "UNKNOWN",
        "reason": "Approved decisive-break definition is absent; fail closed.",
    }
