# Murphy 0021–0023 Historical Provenance Audit V1

Date: 2026-08-13

## Scope
Reviewed the Workspace artifact:
`MURPHY_EVALUATORS_V1/MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`

and the accompanying contract/summary artifacts.

## Findings
- Evaluator contract status: `IMPLEMENTED_AND_UNIT_TESTED`.
- Contract states `2025_used: false`.
- Historical evaluation file is named for `2020_2024` but contains **9 rows dated 2025-01-01** (3 timeframes × 3 rules).
- Therefore the current historical artifact is **not cleanly limited to 2020–2024** and cannot be accepted as the final freeze artifact without remediation/re-generation or an explicit provenance explanation.

## 2025 rows observed
- H1 / 0021 / FAIL
- H1 / 0022 / NOT_EVALUABLE
- H1 / 0023 / NOT_EVALUABLE
- H4 / 0021 / FAIL
- H4 / 0022 / NOT_EVALUABLE
- H4 / 0023 / NOT_EVALUABLE
- D1 / 0021 / PASS
- D1 / 0022 / NOT_EVALUABLE
- D1 / 0023 / NOT_EVALUABLE

## 2020–2024 counts after excluding the 9 contaminated rows
| Rule | Evaluable | PASS | PASS rate |
|---|---:|---:|---:|
| 0021 | 40,799 | 20,600 | 50.4914% |
| 0022 | 39,936 | 5,509 | 13.7946% |
| 0023 | 39,936 | 5,401 | 13.5241% |

## Per-timeframe 2020–2024 counts
| TF | Rule | FAIL | NOT_EVALUABLE | PASS |
|---|---|---:|---:|---:|
| D1 | 0021 | 727 | 2 | 825 |
| D1 | 0022 | 1,094 | 271 | 189 |
| D1 | 0023 | 1,091 | 271 | 192 |
| H1 | 0021 | 16,215 | 159 | 15,011 |
| H1 | 0022 | 26,920 | 459 | 4,006 |
| H1 | 0023 | 26,939 | 459 | 3,987 |
| H4 | 0021 | 3,257 | 18 | 4,764 |
| H4 | 0022 | 6,413 | 312 | 1,314 |
| H4 | 0023 | 6,505 | 312 | 1,222 |

## Decision
**0021–0023 remain FREEZE CANDIDATES, not Production Frozen.**

The blocker is historical provenance cleanliness: the artifact labelled `2020_2024` includes 2025 rows despite the contract stating `2025_used=false`.

## Required next gate
Regenerate or deterministically filter the historical artifact to the approved 2020–2024 window, rerun the historical validation/summary, verify no 2025 rows remain, then perform the official Freeze reconciliation.

No threshold, operator, timeframe, proxy, or rule semantics were changed in this audit.