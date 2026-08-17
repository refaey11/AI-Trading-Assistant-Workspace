# Nison 44-Rule Batch — Execution Status

Date: 2026-08-17
Branch: nison-batch-v1

## Verified inputs
- Canonical File Library artifact `D1.csv` exists and exposes timestamp/OHLC plus derived D1 fields. The project records 2,544 GBPUSD D1 rows for 2016–2024 in the Nison historical work.
- Existing historical replay artifacts for Nison 0035–0038 already cover 2016–2024 and exclude 2025.

## Important execution boundary
The current GitHub branch does not contain the raw D1 bytes in its `data/` directory, and the File Library connector exposes searchable file content but not a mounted runtime path for executing the full CSV in this turn. Therefore this report does NOT claim a fresh 44-rule OHLCV replay.

## Reused historical evidence
0035–0038 have already been structurally replayed on 2,544 GBPUSD D1 rows from 2016–2024:
- 0038: 6 structural Windows (2 bullish, 4 bearish), availability violations 0; freeze candidate only.
- 0035: 1 structural Tasuki candidate; canonical PASS not claimed because the source does not provide a numeric 'about the same size' comparator and trend context is not source-locked.
- 0037: structural candidates exist; same-open/similar-body comparators remain NOT_EVALUABLE.
- 0036: Window dependency and 11-session ceiling are source-backed, but sharpness/small-body/congestion definitions remain unresolved.

## Batch governance result
- Nison remains confirmation-only.
- 2025 is OOS and was not used for tuning.
- No ATR/pip/percentage/body-size/gap threshold was invented.
- Unit tests are not treated as production freeze.
- Rules with unresolved source semantics remain NOT_EVALUABLE rather than being forced through.

## Current verdict
BATCH EXECUTION INFRASTRUCTURE: READY
HISTORICAL EXECUTION: PARTIALLY PROVEN BY EXISTING 2016–2024 ARTIFACTS
FRESH 44-RULE RAW-DATA REPLAY: BLOCKED BY RUNTIME DATA MOUNT
PRODUCTION FREEZE: NOT CLAIMED

## Next concrete action
Make the canonical D1.csv available as a runtime file to the Nison batch runner, then execute all deterministic rules in one pass and emit per-rule PASS/FAIL/NOT_EVALUABLE plus availability/no-lookahead status. Do not tune on 2025.