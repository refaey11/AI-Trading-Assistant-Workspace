# MURPHY_0033 — Canonical Freeze Record V1

Status: PRODUCTION-FROZEN-CANDIDATE

## Scope
This record freezes the source-bounded Murphy 0033 implementation candidate after source reconciliation, deterministic tests, prefix replay, and historical QA.

## Rule
- Rule ID: MURPHY_0033
- Name: Candlestick context filter
- Direction: NEUTRAL / contextual evidence only
- Source: Murphy, Chapter 12, Filtered Candle Patterns
- Concept attribution: Greg Morris (1991), as explicitly stated in the reconciled source record.

## Frozen contract
- Reversal candle patterns only.
- Short-term trend context required.
- Worked source profile: Stochastics %D.
- Presignal zones: %D < 20 or %D > 80.
- No independent BUY/SELL generation.
- Missing required inputs => NOT_EVALUABLE.

## QA evidence
- Deterministic unit tests: 7/7 PASS.
- Prefix/no-lookahead tests: 2/2 PASS.
- Historical QA scope: 2016–2024 only.
- Historical rows examined: 273,387.
- Confirmed contextual cases: 7,255.
- Availability: PASS.
- Provenance: PASS.
- 2025: reserved OOS; no tuning.

## Important boundary
Historical QA validates deterministic execution and replay integrity. It does not claim profitability, expectancy, or trading performance.

## Freeze decision
The rule is eligible for canonical production registration based on the completed gates above. Any future change to the source contract, operator, trend mapping, or Nison integration requires a new version and a fresh compatibility/QA review.
