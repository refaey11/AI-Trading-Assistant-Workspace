# Murphy 0008 — Singleton Pivot + PF-B1 Contract Test Results V1

Status: EXPERIMENTAL TEST PASS — NOT PRODUCTION FROZEN
Date: 2026-08-15

## Execution basis
- Pivot input: PIVOT_SEQUENCE_V2 GBPUSD D1, confirmed LOW pivots.
- OHLC execution input: GBPUSD D1 OHLC columns from the reconstructed Workspace DMI_ADX_V1 output covering 2016-01-03 through 2024-12-31.
- Scope: 2016–2024 only.
- 2025: excluded.
- Operator: confirmed Pivot LOW price is the event Support boundary; no clustering/tolerance.
- Break operator: two consecutive completed D1 closes strictly below the same Support boundary.

## Event replay
- Confirmed LOW pivots in 2016–2024: 344
- Events reaching two consecutive closes below their Support boundary: 324
- Events without such a two-close sequence: 20

## Contract tests
| Test | Result |
|---|---|
| Availability precedes first break bar | PASS |
| First close is a candidate only | PASS |
| Second consecutive close confirms break | PASS |
| Same Support boundary retained | PASS |
| No-lookahead chronology | PASS |
| Retest observation starts strictly after confirmation | PASS |
| Missing support maps to NOT_EVALUABLE | PASS (contract assertion) |

## Retest diagnostic (non-performance evidence)
- Of 324 confirmed-break events, 314 later bars reached or exceeded the Support price (96.91%).
- Of those first-touch events, 156 first-touch bars closed below Support.
- These are structural diagnostics only; they are NOT win rate, profitability, or trading performance.

## Important provenance limitation
This run validates the deterministic contract against the available reconstructed Workspace artifacts. The original pivot manifest references `D1/GBPUSD_D1_STRUCTURE.csv`; that raw source file was not present as a standalone file in the reconstructed archive. Therefore this document is NOT the final authoritative 2016–2024 production QA sign-off. A final production QA run must be independently reproduced from the project's authoritative OHLC source and frozen PF-B1/PF-H1 contracts.

## Freeze status
PASS for the experimental contract test suite.
NOT production frozen. Governance approval, authoritative-data replay, provenance/evidence backup, and final freeze gates remain required.
