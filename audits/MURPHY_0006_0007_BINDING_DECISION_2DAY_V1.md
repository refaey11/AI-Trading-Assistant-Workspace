# Murphy 0006–0007 Binding Decision — 2-Day Time Filter V1

Date: 2026-08-13
Status: EXPLICIT PROJECT BINDING PROPOSAL — TEST BEFORE FREEZE

## Decision proposed
Bind the Murphy Chapter 4 **2 consecutive daily closes beyond the trendline** time-filter semantics as the `no_break` policy for MURPHY_0006 and MURPHY_0007.

## Important provenance distinction
This is a PROJECT OPERATIONAL BINDING based on Murphy Chapter 4 source semantics. It is not represented as a verbatim statement that the original 0006/0007 records explicitly selected this filter.

## Why this policy
- It is directly source-backed by the reviewed Chapter 4 artifacts.
- It avoids inventing a touch-distance threshold, ATR, pip threshold, reaction magnitude, or arbitrary lookback.
- It is deterministic and available from daily OHLC data.
- It is compatible with the existing Geometry/Adapter architecture.
- It preserves 2025 as OOS.

## Proposed evaluator behavior
For each candidate confirmation:
1. Build the trendline from the existing two confirmed same-type pivots.
2. Require the next confirmed same-type candidate after line availability.
3. Retain existing line/range interaction as touch evidence.
4. Require the existing subsequent opposite-type directional reaction candidate as reaction evidence.
5. For `no_break`, scan completed D1 closes after the candidate and before confirmation for two consecutive closes beyond the trendline in the break direction.
6. If two consecutive daily closes beyond the line occur before the successful confirmation event, the candidate fails the no-break condition.
7. Confirmation timestamp must be after the successful reaction evidence and after the relevant no-break evidence is knowable from completed data; never use line-availability timestamp alone.

## Gate
This binding is PROPOSAL/TEST status. It must pass unit tests and 2016–2024 QA before being frozen as production logic.

## Non-goals
- No 3% threshold binding.
- No 1% short-term threshold binding.
- No new ATR/pip/touch tolerance.
- No new reaction magnitude threshold.
- No 2025 tuning.
- No rebuild of Pivot V2 or Geometry V1.
