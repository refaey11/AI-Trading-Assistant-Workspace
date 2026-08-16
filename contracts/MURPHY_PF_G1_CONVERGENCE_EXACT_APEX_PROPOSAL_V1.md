# Murphy PF-G1 — Exact Apex Convergence Proposal V1

Status: GOVERNANCE PROPOSAL / NOT PRODUCTION FROZEN
Date: 2026-08-16

## Purpose

Define the smallest deterministic, source-bounded operationalization for the Chapter 6 requirement that two pattern boundaries converge toward an apex, without introducing a numeric tolerance, ATR/pip threshold, percentage threshold, arbitrary lookback, or outcome-based tuning.

## Source boundary

Murphy Chapter 6 describes a symmetrical triangle as having a descending upper boundary and an ascending lower boundary that converge toward an Apex. The project rule record requires at least four reversal points and says breakout direction must be observed rather than assumed.

This contract is an engineering translation of that qualitative geometry. It is not claimed to be verbatim Murphy wording.

## Inputs

- canonical upper boundary from `TRENDLINE_GEOMETRY_V1`;
- canonical lower boundary from `TRENDLINE_GEOMETRY_V1`;
- boundary slope/orientation;
- boundary anchor timestamps/prices;
- boundary availability timestamps;
- evaluation timestamp.

## Output

```text
upper_boundary_id
lower_boundary_id
relationship = CONVERGING | NOT_CONVERGING | NOT_EVALUABLE
apex_timestamp
apex_price
availability_timestamp
provenance
```

## Deterministic operator

1. Both boundaries must exist and have complete provenance.
2. The upper boundary must have a strictly negative slope.
3. The lower boundary must have a strictly positive slope.
4. Treat each canonical boundary as its existing straight-line geometry; do not refit or modify it.
5. Compute the exact mathematical intersection of the two lines.
6. The intersection must exist and its timestamp must be strictly later than the joint boundary availability timestamp.
7. The intersection must also be forward of the latest defining boundary anchor timestamp.
8. At the evaluation timestamp, the upper boundary price must be above the lower boundary price.
9. If all conditions pass, classify `CONVERGING` and expose the computed apex.
10. If the required geometry exists but any convergence condition fails, classify `NOT_CONVERGING`.
11. If required geometry, provenance, or availability is missing/ambiguous, classify `NOT_EVALUABLE`.

## Why no tolerance is required

The operator does not ask whether two lines are "close enough." It tests the exact geometric relationship already represented by the canonical lines: opposite directional slopes plus a forward mathematical intersection while the upper boundary remains above the lower boundary.

No percentage, ATR, pip, point-distance, slope-difference, or lookback threshold is introduced.

## Availability / no-lookahead

- The operator may use only boundary geometry that is already available at the evaluation timestamp.
- The apex is a deterministic projection from already-available lines; it is not evidence that future prices will reach the apex.
- A future price/pivot cannot create or modify the boundary used by an already-evaluated event.
- A later refit of a boundary must not rewrite an earlier evaluated convergence record.

## 0013 compatibility

This proposal is intended for:
- MURPHY_0013 Symmetrical Triangle;
- and, only after separate compatibility approval, other rules whose source semantics explicitly require converging boundaries.

For MURPHY_0013 the intended assembly is:

`PIVOT_SEQUENCE_V2 → TRENDLINE_GEOMETRY_V1 → PF-G1 → PF-B1 → 0013 evaluator`

PF-G1 does not determine breakout direction and does not generate BUY/SELL.

## Required tests before approval

1. valid descending-upper + ascending-lower + forward apex → `CONVERGING`;
2. same-slope boundaries → `NOT_CONVERGING`;
3. negative upper + positive lower but intersection in the past → `NOT_CONVERGING`;
4. missing boundary → `NOT_EVALUABLE`;
5. missing availability/provenance → `NOT_EVALUABLE`;
6. upper/lower ordering invalid at evaluation → `NOT_CONVERGING`;
7. prefix replay invariance;
8. future-suffix mutation invariance;
9. availability timestamp cannot move backward;
10. no 2025 parameter selection.

## Governance gate

This proposal must not be treated as a production operator until compatibility review approves the semantics, implementation, deterministic tests, and subsequent 2016–2024 historical QA.
