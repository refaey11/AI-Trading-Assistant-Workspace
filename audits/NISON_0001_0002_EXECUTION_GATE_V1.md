# Nison 0001–0002 Execution Gate V1

Status: IMPLEMENTED HARD-GEOMETRY GATE — HISTORICAL QA NOT YET GRANTED

## Scope
NISON_0001 Bullish Engulfing and NISON_0002 Bearish Engulfing are evaluated only on source-stated hard formation geometry:
- candle polarity
- two-candle ordering
- complete real-body containment

Excluded from this gate:
- trend/context
- support/resistance
- volume
- strong candle / strength
- confirmation candle
- invented thresholds, tolerances, lookbacks, scoring

## Tests
The branch now contains deterministic tests for:
- valid bullish engulfing geometry
- invalid bullish polarity
- valid bearish engulfing geometry
- incomplete bearish body engulfment
- evidence availability at evaluation timestamp
- rejection of future availability / look-ahead

## Governance
- Nison remains confirmation-only.
- This hard-geometry gate does not create market direction.
- 2025 remains OOS and is not used for tuning or selection.
- No production freeze is granted by unit tests alone.

## Next gate
Run the CI tests, then integrate the hard-geometry result with the existing Nison evidence adapter. Historical QA may only start after the complete evaluator contract (including required confirmation/context clauses) is explicitly closed. Unresolved qualitative clauses remain NOT_EVALUABLE.
