# Murphy 0008 — Event Provenance QA V1

Status: CANDIDATE QA — NOT PRODUCTION FROZEN

## Data used
- GBPUSD D1: `DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv`
- Confirmed pivots: `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv`
- Scope: 2016–2024 only
- 2025: excluded

## Frozen validation operator
For each confirmed LOW pivot:
1. Support boundary = pivot price.
2. Support must be available before the first eligible break observation.
3. First completed D1 close strictly below support = break candidate.
4. Immediately following completed D1 close strictly below the same support = decisive confirmation.
5. Retest starts strictly after confirmation.
6. Retest = later D1 range intersects the support price.
7. Role-reversal evidence = later intersecting D1 bar closes strictly below support.

## Recomputed event population
- Confirmed LOW support candidates in 2016–2024: 344
- First-break candidates: 326
- Decisive two-close confirmations: 242
- Candidate failures at immediate next close: 84
- Later range-intersection retests: 233 / 242 (96.28%)
- Later intersecting bars closing below support: 229 / 242 (94.63%)

## Chronology / availability checks
- Support availability precedes first break candidate: 242 / 242 PASS
- Candidate timestamp precedes confirmation: 242 / 242 PASS
- Confirmation timestamp follows support availability: 242 / 242 PASS
- Retest begins after confirmation: 233 / 233 PASS
- Role-reversal evidence occurs after confirmation: 229 / 229 PASS
- Confirmations in 2025: 0

## Edge-case populations
Nine confirmed events had no later D1 range intersection with the support before the end of the 2016–2024 dataset. Thirteen confirmed events had a later range intersection but no later intersecting bar closed strictly below support.

These are valid diagnostic outcomes, not evaluator failures.

## Important provenance correction
The earlier conversational count of 324 confirmations is superseded. The frozen operator requires the immediate next completed D1 close to confirm the first candidate close. Recomputing directly from the workspace data yields 242 confirmations.

## Interpretation
This QA validates event chronology and deterministic application of the frozen validation operator. The retest percentages are evidence-frequency diagnostics only. They are not win rate, profitability, or a production trading-performance claim.

## Production boundary
This file does not by itself authorize production freeze. A final freeze still requires the project's explicit provenance/evidence manifest and production governance gate.
