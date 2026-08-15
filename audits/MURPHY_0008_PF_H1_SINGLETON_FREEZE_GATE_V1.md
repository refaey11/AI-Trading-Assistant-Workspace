# Murphy 0008 — PF-H1 Singleton Freeze Gate V1

Status: FROZEN FOR 0008 VALIDATION — NOT PRODUCTION FROZEN

## Decision
For the 0008 validation path, PF-H1 uses a single confirmed LOW pivot from PIVOT_SEQUENCE_V2 as the Support boundary for that event.

## Contract
- Support source: confirmed LOW pivot.
- Support price: pivot price.
- Identity: preserve the pivot/event identity as the level identity; do not merge nearby pivots.
- Availability: support must be available before the first break observation.
- Missing/unavailable support: NOT_EVALUABLE.

## Explicit exclusions
- No horizontal clustering.
- No price-equality tolerance.
- No ATR/pip/percentage tolerance.
- No hidden lookback.
- No use of future pivots to redefine a historical support boundary.
- No 2025 tuning or selection.

## Compatibility rationale
This is the smallest deterministic path supported by the existing PIVOT_SEQUENCE_V2 infrastructure and the 0008 semantic requirement for a Support boundary. It avoids inventing a new horizontal-level engine.

## Integration order
Confirmed Pivot LOW → singleton Support boundary → frozen PF-B1 two-close decisive break → later retest/role reversal → 0008 evidence.

## Status boundary
This freeze is limited to the 0008 validation path. It does not claim that singleton pivots are a universal horizontal-level definition for the broader project.

## Remaining gates
- Formal 0008 evaluator/adapter implementation.
- Deterministic test suite.
- Fresh 2016–2024 QA and provenance/evidence backup.
- Final production-freeze decision after all gates pass.
- 2025 remains OOS.
