# Murphy 0021–0023 Clean Historical Validation V1

Date: 2026-08-13

## Validation performed
Validated the cleaned historical artifact after deterministic removal of the 9 rows dated 2025-01-01 from the prior `2020_2024` artifact.

### Artifact checks
- Rows: 122,934
- Minimum timestamp: 2020-01-02 00:00:00
- Maximum timestamp: 2024-12-31 23:00:00
- Years present: 2020, 2021, 2022, 2023, 2024 only
- 2025 rows: 0
- Timeframes present: H1, H4, D1
- Rules present: MURPHY_0021, MURPHY_0022, MURPHY_0023

### Summary consistency
The clean summary exactly matches a group-by of the clean historical evaluation rows.

### 2020–2024 totals
| Rule | Evaluable | PASS | PASS rate |
|---|---:|---:|---:|
| 0021 | 40,799 | 20,600 | 50.4914% |
| 0022 | 39,936 | 5,509 | 13.7946% |
| 0023 | 39,936 | 5,401 | 13.5241% |

## Decision
The **historical artifact cleanliness/provenance gate is now PASS** for the cleaned artifact: no 2025 rows remain and the summary is internally consistent.

This does NOT by itself constitute Production Freeze. The next required gate is a canonical evaluator rerun/CI validation using this clean 2020–2024 artifact, followed by the official Freeze record if that rerun passes.

No rule logic, thresholds, timeframe definitions, or proxies were changed.