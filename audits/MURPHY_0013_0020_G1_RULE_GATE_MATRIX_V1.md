# Murphy 0013–0020 — G1 Rule Gate Matrix V1

Status: COMPATIBILITY / GOVERNANCE — NOT PRODUCTION FROZEN
Date: 2026-08-16

Source basis: MURPHY_0013_0020_SOURCE_RECONCILIATION_V2, MURPHY_0013_0020_PATTERN_DERIVED_FEATURE_CONTRACT_V1, MURPHY_PATTERN_PRIMITIVES_IMPLEMENTATION_SPEC_V1.

## Purpose
Record exactly what PF-G1 can and cannot establish for the eight pattern rules, without creating new pattern semantics or numeric tolerances.

## Exact-geometry gate
PF-G1 may classify only explicit line geometry:
- unequal slopes -> exact intersection/convergence geometry;
- equal slopes with different intercepts -> exact parallel geometry;
- coincident boundaries -> insufficient distinct-boundary evidence;
- missing line geometry -> NOT_EVALUABLE.

No near-parallel or near-convergent classification is permitted without a separately approved tolerance.

## Rule gates

0013 Symmetrical Triangle
- Required: PF-01/PF-02, descending upper, ascending lower, PF-G1 convergence, PF-B1 breakout event.
- G1 contribution: exact convergence geometry only.
- Remaining blocker: PF-B1 decisive/confirmed breakout contract.

0018 Falling Wedge
- Required: two downward boundaries, PF-G1 convergence, PF-B1 upside breakout.
- G1 contribution: exact convergence geometry only.
- Remaining blocker: PF-B1 breakout contract.

0019 Rising Wedge
- Required: two upward boundaries, PF-G1 convergence, PF-B1 downside breakout.
- G1 contribution: exact convergence geometry only.
- Remaining blocker: PF-B1 breakout contract.

0020 Rectangle
- Required: horizontal support/resistance range, PF-G1 parallel boundaries, PF-B1 confirmed breakout.
- G1 contribution: exact parallel geometry only.
- Remaining blockers: approved horizontal-level contract and PF-B1 breakout contract.

0014 Ascending Triangle
- G1 is not a required primitive in the current derived-feature mapping; it requires PF-H1 + ascending lower boundary + PF-B1.

0015 Descending Triangle
- G1 is not a required primitive in the current derived-feature mapping; it requires PF-H1 + descending upper boundary + PF-B1.

0016 Flag
- G1 is used for the parallel-channel relation, but PF-F1 sharpness and PF-B1 remain unresolved.

0017 Pennant
- G1 is inherited through the symmetrical-triangle geometry, while PF-F1 and PF-B1 remain unresolved.

## Decision
PF-G1 is compatible as an exact-geometry evidence primitive. It does not close any Rule to Production/Frozen status. The current source contracts explicitly require separate evaluator, deterministic tests, 2016–2024 QA, availability/no-lookahead, provenance, and freeze gates.

2025 remains OOS and is excluded from operator selection/tuning.
