# Murphy 0003–0004 Production Freeze Record V1

## Status
**PRODUCTION FROZEN**

## Freeze basis
The Murphy 0003–0004 availability alignment contract, evaluator implementation, unit tests, and 2016–2024 historical validation were reviewed against the canonical Pivot Sequence V2 source.

## Exact rule semantics
- MURPHY_0003: current reaction peak > prior reaction peak AND current reaction trough > prior reaction trough.
- MURPHY_0004: current reaction peak < prior reaction peak AND current reaction trough < prior reaction trough.

## Availability / lookahead
- Confirmed pivots require confirmation after 2 bars.
- Only evidence with availability_timestamp <= evaluation_availability_timestamp may participate.
- Future pivots are excluded.
- Missing required evidence returns NOT_EVALUABLE.

## Validation evidence
- Workflow: Murphy 0003-0004 V2 Validation
- Run: #5
- Run ID: 31452549681
- Result: SUCCESS
- Historical period: 2016–2024
- 2025 data included: NO
- Validation artifact: murphy-0003-0004-v2-validation-workspace-v1

## Final historical results
| Timeframe | Evaluatable events | 0003 PASS | 0004 PASS |
|---|---:|---:|---:|
| D1 | 341 | 101 | 118 |
| H1 | 7,728 | 2,257 | 2,056 |
| H4 | 1,923 | 584 | 592 |
| M15 | 29,388 | 8,373 | 8,362 |
| M30 | 14,928 | 4,304 | 4,156 |
| M5 | 84,266 | 24,447 | 23,940 |

## Freeze decision
All required freeze gates passed. No thresholds or pivot-generation parameters were tuned from 2025 or from the evaluation outputs.

**MURPHY_0003–0004: PRODUCTION FROZEN.**
