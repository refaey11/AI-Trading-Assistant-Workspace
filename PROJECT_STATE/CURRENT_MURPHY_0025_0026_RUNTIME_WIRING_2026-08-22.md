# Murphy 0025/0026 Runtime Wiring Status — 2026-08-22

## Status
RUNTIME WIRED / EXECUTION VERIFICATION PENDING

## Scope
- 0025: New 4-week high -> bullish.
- 0026: New 4-week low -> bearish.
- Four-week reference is the existing four completed ISO calendar weeks preceding the current ISO week; current week excluded.
- Missing four-week reference returns NOT_EVALUABLE.

## Existing authoritative evidence
- 10/10 deterministic rule tests.
- 55,192 H1 rows, 2016-2024.
- 0025: 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE.
- 0026: 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE.
- 8/8 historical replay checks.
- 8/8 availability/no-lookahead checks.
- 0 future-reference violations.
- 0 2025 rows.

## Runtime changes
- Added `MURPHY_EVALUATORS_V1/murphy_0025_0026_runtime_v1.py`.
- Added `MURPHY_EVALUATORS_V1/test_murphy_0025_0026_runtime_v1.py`.
- Wired both rules into `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`.

## Verification boundary
The GitHub commit has no CI/status checks recorded yet, so 0025/0026 are NOT upgraded to Runtime Implemented until the executable runtime tests are actually run and pass.

## Next action
Execute the new runtime tests and a full-path smoke test using the existing four-week lookback outputs. Do not add thresholds or rebuild the lookback engine.

2025 remains OOS.
