# Nison 2025 CI Source Acquisition Blocker — 2026-08-25

## Verified state
- Nison frozen runtime contains 44 rule IDs.
- Historical/2025 Nison producer already exists and is year-parameterized.
- A prior verified 2025 production produced 6,225 H1 timestamps, 44 rule IDs, and 273,900 evidence rows.
- NISON_0031 adapter correction widened exposed history from 3 completed candles to the frozen 5-candle contract; regression test exists.

## Current blocker
The CircleCI production job acquires the authoritative `GBPUSD_H1_2016_2025_MASTER.zip` through either:
1. `NISON_2025_SOURCE_URL`, or
2. `DROPBOX_ACCESS_TOKEN` plus the Dropbox path `/GBPUSD_H1_2016_2025_MASTER.zip`.

The job then acquires Market State context through `DROPBOX_ACCESS_TOKEN` unless a committed/local context file is present. This is source acquisition infrastructure, not Nison strategy logic.

## Required sequence
1. Historical QA on 2016-2024 using the existing `run_nison_historical_production_v1.py` and the same authoritative source.
2. Re-run the frozen Nison runtime compatibility tests, including the NISON_0031 five-candle regression test.
3. Re-run fresh 2025 Nison production.
4. Verify 6,225 x 44 = 273,900 evidence rows and all 44 rule IDs.
5. Run explicit 78-rule coverage.
6. Only after full provenance/coverage gates pass may official 2025 P&L run.

## Governance
- No 2025 tuning or threshold selection.
- No invented formation/session/methodology evidence.
- Missing Nison upstream facts remain `NOT_EVALUABLE`.
- Murphy remains directional authority; Nison remains confirmation/context only.

## Provenance
- Historical Nison runner: `OOS_2025/run_nison_historical_production_v1.py`.
- 2025 producer: `OOS_2025/run_nison_2025_full_production_v1.py`.
- 2025 verifier contract: `OOS_2025/verify_nison_2025_full_production_v1.py`.
- CI source acquisition is intentionally fail-closed when the source secret is absent.
