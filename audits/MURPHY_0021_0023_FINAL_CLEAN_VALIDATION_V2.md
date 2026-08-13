# Murphy 0021–0023 — Final Clean Historical Validation V2

Date: 2026-08-13

## Artifact identity
- File: `MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024_CLEAN_V1.csv`
- SHA-256: `2fdde90766716ca313f7d98ee30ceac98aec27ae7ce6a1c3d262b01e6383df6c`
- Rows: **122,934**
- Years: **2020–2024 only**
- 2025 rows: **0**
- Rules: `MURPHY_0021`, `MURPHY_0022`, `MURPHY_0023`
- Timeframes: `D1`, `H1`, `H4`

## Status counts

| Rule | FAIL | NOT_EVALUABLE | PASS |
|---|---:|---:|---:|
| 0021 | 20,199 | 179 | 20,600 |
| 0022 | 34,427 | 1,042 | 5,509 |
| 0023 | 34,535 | 1,042 | 5,401 |

## Contract / implementation check

The existing evaluator contract states:
- current completed close vs previous completed close;
- existing `volume_direction == UP`;
- existing CFTC futures `oi_direction == UP`;
- no added thresholds;
- no spot-FX OI proxy;
- Dynamic MTF;
- `2025_used = false`.

The evaluator implementation and unit-test file were inspected. All listed unit tests are marked `True`.

## Decision

**Historical artifact cleanliness/provenance: PASS.**

The clean artifact contains no 2025 rows and has internally consistent rule/timeframe/status coverage.

**Production Freeze: NOT YET GRANTED.**

Reason: the historical CSV records evaluator outputs, but does not contain the full input evidence required to independently re-run the evaluator from raw market/OI inputs. Therefore this validation confirms artifact integrity and provenance, not an independent recomputation of every historical decision.

Next gate: retain this clean artifact as the approved historical evidence artifact, then perform the project's official Freeze reconciliation/record against the evaluator contract and Rule Adapter integration.