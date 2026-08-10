# Murphy 0003–0004 Evidence Reconciliation V1

## Status

**BLOCKED — DO NOT FREEZE**

The V2 workflow passes its own evaluator tests and historical scan, but its resulting exact counts do not match the existing canonical historical comparison artifact already committed in the workspace.

## Evidence A — V2 workflow run

Run: `31441977055`
Commit evaluated: `1a63ec7fd4e18f5d5bd837e9e0f050e0cecda78b`
Release: `workspace-v1`

The job passed 7 evaluator tests and produced the following historical counts:

| TF | Evaluable | 0003 PASS | 0004 PASS |
|---|---:|---:|---:|
| D1 | 341 | 101 | 118 |
| H1 | 7,728 | 2,257 | 2,056 |
| H4 | 1,923 | 584 | 592 |
| M15 | 29,388 | 8,373 | 8,362 |
| M30 | 14,928 | 4,304 | 4,156 |
| M5 | 84,266 | 24,447 | 23,940 |

## Evidence B — existing workspace comparison artifact

`MURPHY_0003_0004_HISTORICAL_COMPARISON_2016_2024.csv` contains different exact counts:

| TF | 0003 exact | 0004 exact |
|---|---:|---:|
| D1 | 15 | 15 |
| H1 | 309 | 309 |
| H4 | 102 | 102 |
| M15 | 1,135 | 1,135 |
| M30 | 548 | 548 |
| M5 | 2,806 | 2,806 |

## Finding

These are not a rounding or formatting difference. They are materially different evaluation populations/results.

The current V2 workflow computes its own counts directly from files under `workspace/PIVOT_SEQUENCE_V2_OUTPUT` after reconstructing `workspace-v1`. The existing comparison artifact is therefore not automatically authoritative for the new run, but it is an existing project artifact that must be reconciled before declaring a frozen result.

## Required next gate

1. Identify the provenance and generation method of `MURPHY_0003_0004_HISTORICAL_COMPARISON_2016_2024.csv`.
2. Identify whether its `exact` columns used a different event-selection/alignment population, especially the historical evaluation event definition.
3. Compare the two populations event-by-event on the same canonical Pivot Sequence V2 source.
4. Determine the authoritative evaluation population from the existing project contract — do not infer authority from whichever count is larger.
5. Update only documentation/QA evidence after reconciliation. Do not tune thresholds, pivot parameters, or 2025 data.

## Freeze decision

**0003–0004 remain NOT FROZEN.**

The evaluator logic itself is validated, but the evidence layer has an unresolved historical-count discrepancy. The next action is reconciliation of the two historical evaluation methods, not further tuning.
