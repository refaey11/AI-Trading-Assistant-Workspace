# Murphy 0006–0007 — Deterministic Operator Contract V1

Date: 2026-08-13
Status: SOURCE-LOCKED QUALITATIVE / DETERMINISTIC GATE BLOCKED

## Source-backed semantics

MURPHY_0006:
- reaction LOW family
- upward trendline
- two anchors form tentative line
- third test/touch
- successful reaction/rebound away from line
- line holds without meaningful break
- bullish context

MURPHY_0007:
- reaction HIGH family
- downward trendline
- two anchors form tentative line
- third test/touch
- successful reaction/rebound away from line
- line holds without meaningful break
- bearish context

## Existing lineage to reuse

PIVOT_SEQUENCE_V2 -> TRENDLINE_GEOMETRY_V1 -> MURPHY_CONFIRMATION_LAYER -> 0006/0007 evaluator

Pivot V2 provides confirmed pivot events and availability/no-lookahead. Geometry V1 provides the two-anchor line, slope, direction, and line availability.

## Deterministic status by operator

### Third touch
STATUS: NOT SOURCE-LOCKED DETERMINISTICALLY.

The source establishes that a third test/touch is required, but the project artifacts do not define a numeric or deterministic price-contact predicate. Existing Geometry V1 does not emit a third-touch field.

Do NOT infer a touch from exact price equality, arbitrary distance, ATR, percentage, pips, or a hidden lookback.

### Reaction away from line
STATUS: NOT SOURCE-LOCKED DETERMINISTICALLY.

The source establishes direction of the reaction qualitatively (away from the trendline), but the project does not define a minimum reaction magnitude, bar count, close rule, or other deterministic predicate.

### No-break / line holds
STATUS: NOT SOURCE-LOCKED FOR 0006/0007.

Murphy discusses meaningful trendline breaks and general price/time filtering, but no project artifact binds the general 3% or 2-day examples to 0006/0007. Geometry V1 explicitly excludes breakout detection.

### Availability
STATUS: SOURCE-SUPPORTED.

Use existing Pivot V2 and Geometry V1 availability contracts. No lookahead before defining pivots/line availability.

## Production decision

Because all three confirmation predicates (third touch, reaction magnitude/acceptance, no-break) lack an approved deterministic project operator, 0006/0007 MUST remain NOT_YET_EVALUABLE for production.

The existing candidate/evidence layer may emit raw observations and candidate fields, but it must not emit production PASS/FAIL for these rules.

## Explicitly prohibited

- ATR touch tolerance
- percentage touch tolerance
- pip tolerance
- arbitrary candle/bar count
- arbitrary reaction-distance threshold
- fixed lookback invented by implementation
- automatic 3% binding
- automatic 2-day binding
- tuning any of the above on 2016–2024
- using 2025 to choose an implementation

## Gate closure requirement

A future source artifact/contract must explicitly define deterministic predicates for:
1. third touch
2. successful reaction away from line
3. meaningful break / line hold

Only then may the smallest evaluator adapter be promoted from candidate evidence to PASS/FAIL.

## Current QA state

The corrected 2016–2024 candidate population contains 347 rows (0006=166, 0007=181) and has passed candidate chronology/mapping/uniqueness QA. This QA does not constitute confirmation.
