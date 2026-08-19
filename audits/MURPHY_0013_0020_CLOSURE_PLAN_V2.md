# Murphy 0013–0020 — Closure Plan V2

## Objective
Close the eight rules as a batch without inventing thresholds or importing foreign strategy assumptions.

## Shared primitives
- PF-H1: confirmed horizontal level wrapper over existing pivot/SR representation.
- PF-G1: converging/parallel geometry wrapper over existing trendline geometry.
- PF-B1: completed-bar breakout confirmation wrapper with explicit availability timestamp; no unapproved significance threshold.
- PF-F1: flagpole relation wrapper over existing structure; ambiguous “sharp” evidence returns NOT_EVALUABLE.

## Rule dependencies
- 0013: G1 + B1
- 0014: H1 + B1
- 0015: H1 + B1
- 0016: F1 + G1 + B1
- 0017: F1 + G1 + B1
- 0018: G1 + B1
- 0019: G1 + B1
- 0020: H1 + B1

## Gate sequence
1. Compatibility audit against existing Pivot Sequence V2 and TRENDLINE_GEOMETRY_V1.
2. Deterministic unit tests for each primitive.
3. Availability/no-lookahead tests.
4. Historical QA 2016–2024.
5. Provenance/evidence reconciliation.
6. Freeze only rules that pass every gate.

## Non-negotiables
- Never select thresholds by backtest optimization.
- Never use 2025 for tuning or operator selection.
- Never modify the existing 33 frozen Murphy rules.
- External research is corroboration, not authority.
- Missing/ambiguous source evidence remains NOT_EVALUABLE.

## Status
Ready for implementation/test work; not itself a freeze record.
