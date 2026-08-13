# Murphy 0006/0007 Source-Faithful Event Operator V1

Status: OPERATIONALIZATION CANDIDATE / NOT PRODUCTION FROZEN
Date: 2026-08-13

## Purpose
Document the smallest deterministic event representation that can be tested against the existing Murphy 0006/0007 source semantics and canonical Pivot/Geometry evidence without inventing numeric thresholds.

## Source-backed facts
- 0006: reaction lows, upward trendline, two points establish the tentative line, third successful touch/reaction confirms the trendline, line holds.
- 0007: reaction highs, downward trendline, two points establish the tentative line, third successful touch/reaction confirms the trendline, line holds.
- Murphy's general 3% price and 2-day time filters are break-confirmation material and are not bound here as 0006/0007 touch/reaction rules.

## Existing project facts
- PIVOT_SEQUENCE_V2: confirmed pivots with availability after the required confirming bars; no-lookahead.
- TRENDLINE_GEOMETRY_V1: canonical line family, direction, anchors, slope, and line availability.
- D1 candidate evidence: 347 total candidates; 166 for 0006; 181 for 0007; 62 official strong candidates from candidate-day D1 range intersection plus directional reaction evidence.
- Confirmation Layer contract expects third-touch, reaction, no-break, and confirmation-availability evidence.

## Deterministic operational representation under review
### 0006
1. Use an existing LOW/UP line with two defining anchors.
2. After line availability, select the next confirmed LOW pivot as the third-touch candidate.
3. Require candidate-day D1 range intersection with the line: low <= line_price <= high.
4. Select the next confirmed opposite-family HIGH pivot as the reaction event.
5. Require existing directional-reaction evidence to be true.
6. Between touch and reaction confirmation, require completed D1 lows to remain at or above the line; touch bar may intersect.
7. Confirmation availability = reaction pivot availability timestamp.

### 0007
Mirror of 0006 using HIGH/DOWN, next confirmed HIGH touch candidate, next confirmed LOW reaction event, and completed D1 highs remaining at or below the line.

## Provenance boundary
The source supports the qualitative event chain, but does not explicitly state that "next opposite-family confirmed pivot" is the literal definition of reaction, nor does it specify a numeric reaction magnitude or fixed duration. Therefore this document does not promote those representations to source-verbatim semantics.

## Current empirical result
Applying this operational representation to the official 2016-2024 strong-candidate population produces 15 provisional confirmations:
- 0006: 8
- 0007: 7

These are validation results only, not production PASS.

The existing confirmation-availability artifact records confirmation=True only where no_break_valid=True and the confirmation availability timestamp is populated. Examples include 0006 LOW::55 (2017-04-18 -> confirmation 2017-05-01), LOW::59 (2017-05-16 -> 2017-05-21), LOW::106 (2018-07-13 -> 2018-07-18), and LOW::205 (2021-02-04 -> 2021-02-12). 0007 examples include HIGH::104 (2018-07-16 -> 2018-07-22), HIGH::172 (2020-01-24 -> 2020-01-30), HIGH::236 (2021-10-11 -> 2021-10-14), HIGH::249 (2022-02-10 -> 2022-02-17), HIGH::256 (2022-04-21 -> 2022-05-02), HIGH::270 (2022-09-13 -> 2022-09-20), and HIGH::288 (2023-03-07 -> 2023-03-10).

## Prohibited
- No ATR tolerance.
- No pip tolerance.
- No percentage touch tolerance.
- No fixed lookback.
- No invented reaction magnitude/duration.
- No automatic 3% or 2-day binding.
- No 2025 use.

## Promotion gate
Do not mark 0006/0007 production-frozen until this operational representation passes formal compatibility review, deterministic unit tests, 2016-2024 historical QA, and no-lookahead audit.
