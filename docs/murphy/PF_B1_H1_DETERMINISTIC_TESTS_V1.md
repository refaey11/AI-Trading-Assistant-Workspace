# PF-B1 / PF-H1 Deterministic Tests V1

## PF-B1

| Case | Expected |
|---|---|
| approved boundary + completed-bar close beyond | BREAKOUT |
| intrabar penetration + close back inside | NO_BREAKOUT |
| missing/unapproved boundary | NOT_EVALUABLE |
| availability timestamp before bar close | REJECT_AVAILABILITY |

## PF-H1

| Case | Expected |
|---|---|
| confirmed pivot + authoritative horizontal label | HORIZONTAL_AVAILABLE |
| confirmed pivot without horizontal label | NOT_EVALUABLE |
| raw swing without confirmed pivot | NOT_EVALUABLE |
| classification requires an invented tolerance | REJECT_NEW_THRESHOLD |

No external numeric threshold is used.
