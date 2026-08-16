# Murphy Structural Evaluator Contract V1

Status: CONTRACT / NOT PRODUCTION FROZEN

## Scope
Structural detection only for Murphy rules 0013, 0014, 0018, 0019, 0020. Breakout confirmation remains a separate PF-B1 gate.

## 0013 Symmetrical Triangle
Required structural evidence:
- explicit upper boundary with negative slope
- explicit lower boundary with positive slope
- exact boundary convergence under PF-G1

No tolerance is introduced for near-slope cases.

## 0014 Ascending Triangle
Required structural evidence:
- explicit lower boundary with positive slope
- explicit upper boundary confirmed horizontal by PF-H1

No near-horizontal tolerance is introduced.

## 0018 Falling Wedge
Required structural evidence:
- both boundaries explicitly negative slope
- exact convergence under PF-G1

## 0019 Rising Wedge
Required structural evidence:
- both boundaries explicitly positive slope
- exact convergence under PF-G1

## 0020 Rectangle
Required structural evidence:
- upper boundary confirmed horizontal by PF-H1
- lower boundary confirmed horizontal by PF-H1
- exact parallel relationship under PF-G1

## Common gates
Structural status does not imply a complete Murphy rule confirmation. Pivot provenance, chronology, breakout confirmation, and any additional source-required evidence remain independent gates.

If required structural evidence is missing or depends on an unapproved tolerance, return NOT_EVALUABLE rather than infer it.

2025 remains OOS and must not be used for tuning.
