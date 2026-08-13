# Murphy 0025–0026 — Four-Week Lookback Compatibility Audit V1

Date: 2026-08-13
Scope: MURPHY_0025 / MURPHY_0026 only
Status: SOURCE/FEATURE COMPATIBLE — VALIDATION PENDING

## Source-backed rule semantics
The Master Knowledge Base contains the Murphy/Donchian 4-Week Rule:
- New 4-week high (20 trading days) -> Buy / cover short.
- New 4-week low -> Sell / short entry.

Therefore the project mapping is:
- MURPHY_0025 -> new 4-week high -> BULLISH
- MURPHY_0026 -> new 4-week low -> BEARISH

## Existing component
The project handoff explicitly identifies FOUR_WEEK_LOOKBACK_V1 as existing infrastructure and requires reuse rather than rebuilding it.

## Compatibility result
The source and existing feature family are compatible with 0025/0026.
No new feature is required.

## Exact unresolved operator detail
The accessible source text establishes the 20-trading-day window and directional outcome, but it does not by itself specify which OHLC field must trigger the phrase “price reaches a new 4-week high/low” (e.g. high/low versus close). The existing FOUR_WEEK_LOOKBACK_V1 implementation/contract must therefore be inspected before freezing the evaluator.

Do NOT silently choose a field or invent a threshold.

## Required next gate
1. Retrieve the canonical FOUR_WEEK_LOOKBACK_V1 implementation/contract.
2. Verify its exact trigger field and availability semantics.
3. Bind 0025/0026 to that existing feature without changing the source rule.
4. Add deterministic unit tests.
5. Run historical/provenance QA on 2016–2024.
6. Keep 2025 OOS and out of tuning/selection.
7. Freeze only after the complete pipeline passes.

## Freeze boundary
This audit does not claim evaluator completion, historical QA completion, or Production Freeze.