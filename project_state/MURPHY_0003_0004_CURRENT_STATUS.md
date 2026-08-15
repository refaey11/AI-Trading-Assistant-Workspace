# Murphy 0003–0004 — Current Project State

Date: 2026-08-15
Status: PRODUCTION FROZEN

This file is the current-state pointer for 0003/0004. Older candidate/provenance-blocker notes are historical and must not override the verified freeze record on `main`.

## Verified basis
- V2 availability-aligned evaluator.
- Canonical Pivot Sequence V2.
- Confirmed pivots available only after the required 2-bar confirmation.
- No future-pivot participation.
- Missing required evidence returns NOT_EVALUABLE.
- Unit tests present and cover positive, negative, and missing-input cases.
- Historical validation workflow Run #5 / ID 31452549681: SUCCESS.
- Validation period: 2016–2024.
- 2025 data included: NO.

## Frozen semantics
0003: current reaction peak > prior reaction peak AND current reaction trough > prior reaction trough.

0004: current reaction peak < prior reaction peak AND current reaction trough < prior reaction trough.

## Final validation counts
D1: 341 evaluatable; 101 PASS for 0003; 118 PASS for 0004.
H1: 7,728 evaluatable; 2,257 PASS for 0003; 2,056 PASS for 0004.
H4: 1,923 evaluatable; 584 PASS for 0003; 592 PASS for 0004.
M15: 29,388 evaluatable; 8,373 PASS for 0003; 8,362 PASS for 0004.
M30: 14,928 evaluatable; 4,304 PASS for 0003; 4,156 PASS for 0004.
M5: 84,266 evaluatable; 24,447 PASS for 0003; 23,940 PASS for 0004.

## Governance
No thresholds or pivot-generation parameters were tuned from 2025 or from evaluation outputs.

Canonical freeze record:
audits/MURPHY_0003_0004_EVALUATOR_V2/MURPHY_0003_0004_FREEZE_RECORD_V1.md
