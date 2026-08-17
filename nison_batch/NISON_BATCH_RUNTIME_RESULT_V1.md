# Nison Batch Runtime Result V1

Date: 2026-08-17
Branch: nison-batch-v1
Dataset: GBPUSD D1, 2016-2024, 2,544 rows; 2025 excluded.

## Verified structural replay results
| Rule | Structural candidates | Canonical state |
|---|---:|---|
| 0001 Bullish Engulfing | 206 | NOT_EVALUABLE pending source-defined qualitative/context gates |
| 0002 Bearish Engulfing | 197 | NOT_EVALUABLE pending source-defined qualitative/context gates |
| 0015 Tweezers Top | 1 exact-high candidate | NOT_EVALUABLE pending required context/confirmation |
| 0016 Tweezers Bottom | 3 exact-low candidates | NOT_EVALUABLE pending required context/confirmation |
| 0019 Bullish Counterattack | 0 | NO_MATCH (structural replay; confirmation not inferred) |
| 0020 Bearish Counterattack | 0 | NO_MATCH (structural replay; confirmation not inferred) |
| 0034 Separating Lines | 0 exact same-open candidates | NO_MATCH for exact structural contract |

## Governance
- Structural candidate count is not a PASS/FREEZE claim.
- Qualitative source language is not converted into invented thresholds.
- Nison remains confirmation-only and emits neutral direction.
- 2025 remains OOS and is excluded from tuning.
- Existing 0035-0038 replay/evaluator evidence must be reused rather than rebuilt.

## Remaining execution
Continue the same batch runtime over the remaining compiled formation contracts. Promote only rules whose complete source, context, confirmation, invalidation, availability and no-lookahead gates pass historical QA.