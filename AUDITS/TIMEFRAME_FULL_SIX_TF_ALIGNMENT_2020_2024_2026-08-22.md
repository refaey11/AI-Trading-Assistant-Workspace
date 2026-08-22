# Timeframe Full Six-Timeframe Alignment — 2026-08-22

## Scope
Validate the recovered GBPUSD six-timeframe source family without reopening source contracts and without using 2025 for tuning/selection.

## Source evidence
A reconstructed Rule Evaluator workspace contains the following same-family OBV datasets:
- M5: 373,465 rows
- M15: 124,764 rows
- M30: 62,513 rows
- H1: 31,385 rows
- H4: 8,039 rows
- D1: 1,554 rows

All datasets cover 2020-01-02 through 2024-12-31 and expose `bar_close_timestamp` plus the OBV evidence fields.

## Deterministic alignment test
M5 is the base observation stream. Each higher timeframe is joined using backward/as-of semantics: the latest source timestamp less than or equal to the M5 observation timestamp.

Results:
| Higher TF | Source rows | Unmatched M5 rows | Future timestamp violations |
|---|---:|---:|---:|
| M15 | 124,764 | 0 | 0 |
| M30 | 62,513 | 0 | 0 |
| H1 | 31,385 | 0 | 0 |
| H4 | 8,039 | 0 | 0 |
| D1 | 1,554 | 0 | 0 |

Source integrity checks:
- All six timestamp series monotonic increasing.
- No duplicate source timestamps in any timeframe.
- Base M5 rows: 373,465.
- 2025 rows used: 0.

## Interpretation
The recovered six-timeframe data family can be aligned to the M5 base with zero future timestamp violations and zero unmatched M5 observations over the 2020-2024 test window.

This is evidence for the six-timeframe alignment/no-lookahead boundary. It is NOT a claim that the entire Dynamic Timeframe Selection runtime is implemented or production-verified.

## Remaining gates
- Dynamic Timeframe Selection runtime producer/implementation: not yet demonstrated.
- Time/Session Context runtime contract: not yet demonstrated.
- Full end-to-end timeframe leakage proof across the actual runtime chain: not yet claimed.
- 2025 remains protected OOS.

## Governance
Do not invent timeframe selection thresholds, session boundaries, or directional logic. MTF assigns roles/evidence; Decision Brain decides. 2025 is excluded from tuning/calibration/selection.
