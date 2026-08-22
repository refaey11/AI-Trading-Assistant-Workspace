# GBPUSD 2025 Market State Producer Recovery Gate

**Date:** 2026-08-23
**Status:** OPEN / PRODUCER RECOVERY REQUIRED

## Finding
The fresh GBPUSD 2025 H1/H4 source preparation is complete, but the existing Market State runtime path does **not** expose a raw-OHLC producer in the inspected project artifacts.

## Evidence inspected
1. `AI_Trading_Assistant_MARKET_STATE_READER_V1.zip`
   - Contract + historical output CSVs + coverage/readings artifacts.
   - No executable producer implementation present in the archive.
2. `AI_Trading_Assistant_MARKET_READER_V1.zip`
   - Architecture/schema/roadmap artifacts.
   - No executable producer implementation present in the archive.
3. GitHub `compatibility/market_state_contract_adapter_v1.py`
   - Explicitly described as an adapter for **existing source-derived Market State rows**.
   - It normalizes required fields and fails closed; it does not recreate Market State calculations.
4. GitHub `market_pipeline/run_073/market_pipeline_evidence_adapter.py`
   - Consumes precomputed `state_row`, `mtf_row`, and `scenario_row`.
   - It is an evidence normalization layer, not a raw-OHLC producer.

## Important implication
The 2025 H1/H4 files must **not** be passed directly into the downstream evidence adapter as though they were Market State rows. That would skip the required producer boundary and silently invent semantics.

## Contract boundary preserved
- No new Market State calculations introduced here.
- No BUY/SELL decision generated.
- 2025 remains `OOS_READ_ONLY` / protected from tuning.
- Missing producer evidence remains fail-closed.

## Next action
Recover/identify the authoritative existing producer from the Rule Evaluator workspace or another source-backed archive, then perform a compatibility audit against the frozen Market State contract before any wiring change.

## Existing runtime evidence
The Market State contract adapter is intentionally downstream of source-derived state rows and cannot substitute for the missing producer.
