# Murphy 0003–0004 Handoff Backup — 2026-08-13

## Status
**PRODUCTION FROZEN**

## Frozen rule semantics
- MURPHY_0003: current reaction peak > prior reaction peak AND current reaction trough > prior reaction trough.
- MURPHY_0004: current reaction peak < prior reaction peak AND current reaction trough < prior reaction trough.

## Availability / lookahead contract
- Source: PIVOT_SEQUENCE_V2_OUTPUT.
- Confirmed pivots require confirmation after 2 bars.
- Only evidence with availability_timestamp <= evaluation_availability_timestamp may participate.
- Future pivots are excluded.
- Missing required evidence returns NOT_EVALUABLE.
- Evaluation period: 2016–2024.
- 2025 excluded.

## Validation evidence
- Workflow: Murphy 0003-0004 V2 Validation.
- Run: #5.
- Run ID: 31452549681.
- Result: SUCCESS.
- Validation artifact: murphy-0003-0004-v2-validation-workspace-v1.

## Final historical results
| Timeframe | Evaluatable events | 0003 PASS | 0004 PASS |
|---|---:|---:|---:|
| D1 | 341 | 101 | 118 |
| H1 | 7,728 | 2,257 | 2,056 |
| H4 | 1,923 | 584 | 592 |
| M15 | 29,388 | 8,373 | 8,362 |
| M30 | 14,928 | 4,304 | 4,156 |
| M5 | 84,266 | 24,447 | 23,940 |

## Freeze basis
- Availability alignment contract accepted.
- Exact evaluator implementation verified.
- Unit tests passed.
- Historical 2016–2024 validation passed.
- 2025 not used.
- No thresholds or pivot-generation parameters were tuned from 2025 or from evaluation outputs.

## Existing canonical files
- audits/MURPHY_0003_0004_EVALUATOR_V2/MURPHY_0003_0004_AVAILABILITY_ALIGNMENT_CONTRACT_V1.json
- audits/MURPHY_0003_0004_EVALUATOR_V2/murphy_0003_0004_evaluator_v2.py
- audits/MURPHY_0003_0004_EVALUATOR_V2/test_murphy_0003_0004_evaluator_v2.py
- audits/MURPHY_0003_0004_EVALUATOR_V2/MURPHY_0003_0004_FREEZE_RECORD_V1.md

## Continuation rule
Do not reopen or retune 0003–0004 unless a new compatibility/provenance issue is discovered. Continue Murphy work with the next unfrozen rule(s). 0006–0007 are being handled separately in another workstream.
