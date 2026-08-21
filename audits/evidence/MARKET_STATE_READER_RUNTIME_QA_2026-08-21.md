# Market State Reader V1 — Runtime QA Evidence

**Date:** 2026-08-21
**Status:** PARTIAL — structural/runtime checks PASS; volume lineage remains OPEN; AS-OF semantics not proven from output alone.

## Directly inspected source files
- `AI_Trading_Assistant_MARKET_STATE_READER_V1.zip`
- `CONTRACT.json`
- `README.md`
- `STATE_READER_COVERAGE.csv`
- Five historical output CSV files: EURUSD, GBPUSD, USDJPY, USDCAD, XAUUSD

## Contract evidence
`CONTRACT.json` states:
- status: `MARKET_READING_ONLY`
- `not_a_strategy: true`
- principle: describes market context before any decision
- fields include trend, structure_event, support/resistance location, volume_state, volatility_state, candlestick evidence, market_interpretation
- next layer: knowledge retrieval + contextual reasoning

This confirms the module boundary is descriptive market reading, not BUY/SELL generation.

## Runtime integrity checks performed
For every one of the five output CSVs:
- timestamps are strictly non-decreasing
- no duplicate timestamps were found
- coverage runs from January 2016 through December 2025

The historical files therefore provide a complete runtime artifact for structural QA. For current validation, 2016–2024 is the approved QA/development window and 2025 remains reserved for final OOS evaluation.

## Exact row counts and runtime coverage
- EURUSD: 61,435 rows
- GBPUSD: 61,417 rows
- USDJPY: 61,416 rows
- USDCAD: 61,420 rows
- XAUUSD: 58,504 rows

## Warm-up / missing behavior observed
Across the outputs:
- `volume_ratio` has early missing/warm-up values
- support/resistance distance fields have early missing/warm-up values
- this is consistent with the output beginning before all rolling/context calculations are fully available

This behavior is observed and recorded; it is not by itself classified as failure.

## Important correction to earlier audit statements
A prior statement that all five historical outputs had `volume = 0` was incorrect.

Direct re-check shows:
- GBPUSD: all volume values are zero in the inspected output
- USDJPY: all volume values are zero
- USDCAD: all volume values are zero
- XAUUSD: all volume values are zero
- EURUSD: 31,100 rows have non-zero volume

Therefore, the volume problem is not uniform across all five outputs. Any future fix must be based on per-pair lineage evidence, not a blanket assumption.

## What this QA proves
PASS:
1. Module contract exists and is market-reading-only.
2. Five historical runtime outputs exist.
3. Timestamp order is valid in all five inspected outputs.
4. No duplicate timestamps were found.
5. Output coverage spans the historical period required for later QA.
6. 2025 can be cleanly excluded from current validation work.

## What this QA does NOT prove
OPEN:
1. AS-OF / completed-bar / no-lookahead semantics cannot be proven from static output CSVs alone.
2. Exact upstream input lineage is not fully reconstructed.
3. Volume semantics are inconsistent across outputs and require pair-specific lineage audit.
4. `volume_available` is not present in the inspected Market State contract, so unavailable-vs-zero semantics remain unresolved.

## Gate decision
`MARKET_STATE_READER_V1 = PARTIAL`

Do not freeze the module as fully validated yet.

## Resume point
Next action is **AS-OF / no-lookahead evidence audit**, preferably by inspecting the actual generation logic or a reproducible input-to-output pipeline. This must be done before a final PASS.

Volume lineage is a parallel documented gap and must not be silently treated as solved.
