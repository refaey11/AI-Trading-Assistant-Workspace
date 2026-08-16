# Murphy 0013-0020 — PF-G1 Compatibility Audit V1

Status: GOVERNANCE / COMPATIBILITY AUDIT — NOT PRODUCTION FROZEN
Date: 2026-08-16

## Objective
Determine whether PF-G1 (boundary convergence/parallelism) can be satisfied from explicit line geometry without introducing an unapproved tolerance.

## Findings
1. The existing project direction is to preserve source semantics and avoid inventing numeric tolerances when the source/registry does not provide them.
2. Exact line geometry is deterministic: equal slopes with different intercepts are exactly parallel; unequal slopes have an exact intersection.
3. Near-parallel and near-convergent cases require an explicit engineering tolerance. No such tolerance is approved by this audit.
4. Therefore PF-G1 can safely expose exact geometry states, but cannot classify approximate geometry as convergent/parallel.

## Rule compatibility
- 0013 Symmetrical Triangle: requires upper descending and lower ascending boundaries that converge. Exact line geometry can represent the convergence direction; pivot chronology and boundary provenance remain separate prerequisites.
- 0018 Falling Wedge: requires two downward-sloping converging boundaries. Exact line geometry can represent this when both slopes are negative and unequal and the intersection is future-valid under the rule's chronology contract.
- 0019 Rising Wedge: requires two upward-sloping converging boundaries. Exact line geometry can represent this when both slopes are positive and unequal and the intersection is future-valid under the rule's chronology contract.
- 0020 Rectangle: requires horizontal parallel boundaries. Exact horizontal/parallel geometry can represent this only when the upstream boundaries are already explicitly horizontal; no near-horizontal tolerance is introduced.

## Decision
PF-G1 exact-geometry support is compatible as a deterministic primitive.
It is NOT evidence that the complete four rules are production-evaluable. Pivot/geometry provenance, chronology, breakout confirmation, and any missing source-specific semantics remain independent gates.

## Prohibited changes
No ATR multiplier, percentage tolerance, pip tolerance, arbitrary lookback, clustering threshold, or backtest-derived parameter may be introduced here.

## OOS rule
2025 remains OOS and must not be used to select or tune an engineering tolerance.
