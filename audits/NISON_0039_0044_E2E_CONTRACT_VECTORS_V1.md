# Nison 0039–0044 E2E Contract Vectors V1

Status: CONTRACT-LEVEL TESTS ONLY / NOT HISTORICAL QA

Local execution result: 7/7 PASS.

## Positive vectors
- 0039: multiple technical evidence items remain direction-neutral.
- 0040: cluster evidence remains direction-neutral.
- 0041: TRENDLINE_TOUCH timestamp precedes CANDLE_CONFIRM.
- 0042: LEVEL_TEST timestamp precedes CANDLE_CONFIRM.
- 0043: BREAKOUT -> RETURN_INSIDE -> CANDLE_CONFIRM is strictly causal.
- 0044: LEVEL_BREAK -> RETEST -> CANDLE_CONFIRM is strictly causal.

## Negative vector
- 0043 with CANDLE_CONFIRM timestamp earlier than BREAKOUT/RETURN_INSIDE is rejected.

## Gate interpretation
These vectors verify the adapter contract and causal ordering only. They do not prove that the upstream canonical geometry, support/resistance, breakout, or retest engines exist or are production-ready. Historical QA remains gated on verified upstream artifacts and must use 2016–2024 only. 2025 remains OOS and is excluded from tuning, calibration, optimization, and operator selection.
