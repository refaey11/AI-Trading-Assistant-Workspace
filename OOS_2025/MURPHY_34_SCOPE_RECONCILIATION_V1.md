# Murphy 34 Scope Reconciliation V1

## Purpose
Freeze the distinction between the project-wide Murphy registry and the current Final OOS scope.

## Registry reality
The Trading Rules V2 / integrated registry contains 51 Murphy rules (`MURPHY_0001` through `MURPHY_0051`).

## Final OOS scope used in the current Decision Brain work
The current Final OOS scope is the 34-rule slice `MURPHY_0001` through `MURPHY_0034`. This document does not expand that scope to 51.

## Runtime reconciliation on branch
Current canonical Murphy runtime entrypoint directly wires 10 rules within the 34-rule scope:
- MURPHY_0006
- MURPHY_0007
- MURPHY_0018
- MURPHY_0019
- MURPHY_0025
- MURPHY_0026
- MURPHY_0030
- MURPHY_0031
- MURPHY_0032
- MURPHY_0033

MURPHY_0021 has a separate fresh historical producer and is also inside the 34-rule scope.

Therefore the current operational candidate set inside the 34-rule Final OOS scope is 11 rules, subject to historical evidence readiness.

## Not yet operational in the 34-rule scope
The current runtime audit shows the following additional rules with evaluator/runtime artifacts but no canonical entrypoint registration:
- MURPHY_0008
- MURPHY_0022
- MURPHY_0023
- MURPHY_0029

These are not counted as runnable until explicitly wired under the frozen rule adapter contract. `MURPHY_0022` and `MURPHY_0023` additionally require futures open-interest evidence, which is not supplied by the spot-FX market-state source.

## Historical evidence constraint
The frozen 2025 Murphy coverage snapshot currently has usable historical evidence only for MURPHY_0021 among the observed rules; MURPHY_0003, MURPHY_0004, MURPHY_0028 and MURPHY_0050 have zero available rows in that snapshot, while MURPHY_0022 and MURPHY_0023 are not evaluable without futures OI.

## Source-of-truth rule
Do not infer readiness from the rule number, from the presence of a Python file, or from a stale coverage snapshot. A rule is Final-OOS eligible only when:
1. it belongs to the frozen 34-rule scope;
2. its semantics are frozen and compatible;
3. it has a registered runtime/evaluator path;
4. its required historical evidence exists without lookahead or synthetic substitution;
5. its output can be joined at the Decision timestamp.

## Current conclusion
- Murphy registry: 51 rules.
- Current Final OOS scope: 34 rules.
- Operational candidates inside scope: 11.
- Historically demonstrated usable 2025 evidence inside scope: 1 (`MURPHY_0021`).
- Final OOS eligible count remains **1/34 until the remaining candidate rules receive source-backed historical evidence and pass the same eligibility gate**.
