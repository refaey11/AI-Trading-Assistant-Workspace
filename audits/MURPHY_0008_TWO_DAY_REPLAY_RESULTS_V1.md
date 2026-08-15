# Murphy 0008 — Two-Day Replay Results V1

Status: EXPERIMENTAL / NOT FROZEN
Scope: GBPUSD D1, 2016-01-03 through 2024-12-31. No 2025 data.

## Inputs
- D1 OHLC: `DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv` (OHLC fields used only; indicator columns not used).
- Support candidates: `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv`.
- Pivot contract: two confirming bars; support availability controlled by `availability_timestamp`.

## Operator under test
Two successive completed D1 closes below the pivot-derived support boundary.
- First close below support = candidate.
- Second consecutive close below support = confirmation.
- First break bar must occur strictly after support availability.
- Retest observation begins strictly after confirmation.

## Reproducible results
- Confirmed LOW support candidates in 2016–2024: 344
- Candidates reaching two successive D1 closes below support: 324
- Candidates without such a break: 20
- Confirmed breaks with later diagnostic retest: 308 / 324 = 95.06%

Diagnostic retest definition used for this experiment only: a later D1 bar with High >= the broken support and Close <= that support. This is not a frozen production role-reversal contract and is not a profitability measure.

## Temporal QA
- Support availability precedes first break bar for all 324 confirmations: PASS
- Confirmation bar is strictly after first break bar: PASS
- Retest bars are strictly after confirmation: PASS
- 2025 pivot events in input: 0
- 2025 D1 bars in input: 0

## Interpretation
The candidate two-day operator is deterministic and replayable on the current 2016–2024 project data. The replay does not establish trading profitability and does not by itself freeze PF-B1 or Rule 0008. It is evidence for implementation/QA only.

## Next gate
Use this artifact for PF-B1 governance/validation. Do not tune the operator from these results. Production freeze remains blocked until the documented governance, PF-H1 compatibility, 0008 evaluator, and final evidence/freeze gates are satisfied.
