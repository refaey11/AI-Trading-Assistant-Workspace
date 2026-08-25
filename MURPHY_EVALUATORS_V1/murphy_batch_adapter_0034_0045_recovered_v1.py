from dataclasses import dataclass
from typing import Optional, Literal

State = Literal["CONFIRMED", "CONFLICT", "NOT_EVALUABLE"]


@dataclass(frozen=True)
class Evidence:
    rule_id: str
    evaluator_state: Optional[str]
    confirmation_ok: Optional[bool]


@dataclass(frozen=True)
class Result:
    state: State
    reason: str


def adapt(e: Evidence) -> Result:
    if e.evaluator_state is None or e.confirmation_ok is None:
        return Result("NOT_EVALUABLE", "Required evaluator/confirmation evidence is missing.")
    if e.evaluator_state != "PASS":
        return Result("CONFLICT", "Murphy evaluator did not pass.")
    if not e.confirmation_ok:
        return Result("CONFLICT", "Required confirmation evidence did not pass.")
    return Result("CONFIRMED", "Murphy context and confirmation evidence both pass.")
