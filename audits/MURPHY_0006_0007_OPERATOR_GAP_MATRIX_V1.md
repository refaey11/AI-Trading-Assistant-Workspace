# Murphy 0006–0007 Operator Gap Matrix V1

Date: 2026-08-13
Status: COMPATIBILITY ANALYSIS RECORDED

## Source-backed fields

| Required predicate | Existing evidence | Source support | Production-ready? |
|---|---|---|---|
| third_touch | next confirmed same-type pivot after anchor 2 and line availability; candidate timestamp/price; line price; signed/absolute distance; daily range intersection | Murphy requires a third successful test/touch and reaction | NO — candidate only |
| reaction_bounce | subsequent reaction candidate + directional consistency | Murphy requires successful reaction/rebound | NO — candidate only |
| no_break | raw D1 line/range integrity observation | Murphy distinguishes meaningful break from temporary/intraday penetration; general 3%/2-day examples exist | NO — approved 0006/0007 binding absent |
| availability | line availability timestamp; Pivot V2 availability/no-lookahead lineage | Project contracts require no lookahead and availability timing | YES as evidence/constraint |

## Important distinction

The adapter already identifies a `third_touch_candidate`; it does not claim successful touch. The existing evidence schema also records reaction candidates and directional consistency. These are observations, not confirmation predicates.

## What cannot be promoted without a new authoritative contract

- No touch tolerance can be inferred from `absolute_distance`.
- `daily_range_intersects_line` cannot by itself be promoted to `third_touch_detected`.
- `reaction_directionally_consistent` cannot by itself be promoted to `reaction_detected` because no source-approved magnitude/duration rule exists.
- `no_break_observation` cannot be promoted to `no_break_valid` because no 0006/0007-specific approved break binding exists.
- Murphy's general 3% / two-consecutive-day filters must not be automatically bound to 0006/0007.

## Decision

The smallest source-safe layer is already implemented: preserve raw candidate evidence. The remaining gap is the exact deterministic operator/contract for successful touch, successful reaction, and 0006/0007-specific no-break.

Production evaluator must remain NOT_EVALUABLE until those contracts are source-locked.

## Next authorized step

Search only for an existing authoritative operator/contract in the full project and historical evaluator workspace. If none exists, do not invent one; retain candidate evidence and document the gate.

## Constraints

- Reuse PIVOT_SEQUENCE_V2 and TRENDLINE_GEOMETRY_V1.
- No invented ATR, percentage, pip, tolerance, magnitude, duration, lookback, or timeframe.
- No 2025 tuning.
