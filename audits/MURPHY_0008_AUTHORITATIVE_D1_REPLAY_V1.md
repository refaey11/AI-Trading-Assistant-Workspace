# Murphy 0008 — D1 Replay V1

Status: EXPERIMENTAL / CANDIDATE EVIDENCE — NOT PRODUCTION FROZEN

## Scope
GBPUSD D1, 2016–2024 only. 2025 excluded.

## Data lineage
The reconstructed Rule Evaluator workspace contains:
- PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv
- DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv

The project evidence separately records that the D1/M1 lineage reconciliation reproduced d1_ref.csv exactly across 2,544 common 2016–2024 dates. Therefore this replay uses the lineage-validated reconstructed D1 path; it does not claim that a standalone raw `D1/GBPUSD_D1_STRUCTURE.csv` is present in the archive.

## Candidate operationalization under test
For each confirmed LOW pivot available within the 2016–2024 evaluation window:
1. pivot price is the singleton Support boundary for that event;
2. first completed D1 close strictly below Support starts a candidate break;
3. second consecutive completed D1 close strictly below the same Support confirms the candidate break;
4. retest observation begins strictly after the second close;
5. diagnostic retest = later D1 range intersects Support;
6. diagnostic role-reversal retest = later intersecting D1 bar closes strictly below Support.

This is an experimental project operationalization, not a claim that Murphy specifies these exact numeric event predicates verbatim.

## Replay result
- Confirmed LOW Support candidates available in 2016–2024: 344
- Two-successive-close confirmations: 324
- No two-close confirmation: 20
- Later range-intersection retest: 314 / 324 (96.91%)
- Later intersecting bar closing below Support: 308 / 324 (95.06%)

## Integrity checks
- Support availability precedes the first eligible break observation: PASS by construction of the eligibility gate.
- Confirmation occurs at the close of the second completed D1 bar: PASS.
- Retest search starts strictly after confirmation: PASS.
- No 2025 data used: PASS.
- No ATR, pip, percentage, clustering, tolerance, or hidden lookback: PASS.

## Interpretation
The replay demonstrates that the candidate singleton-Pivot + two-close operator is deterministic and reproducible on the lineage-validated D1 path. The retest percentages are event-frequency diagnostics only; they are not win rates, profitability, or proof of rule validity.

## Governance boundary
PF-B1 and the singleton PF-H1 path remain experimental until the project's explicit governance/freeze gates are completed. This replay must not be promoted to a production 0008 PASS or freeze decision by itself.

## Next gate
1. Preserve this replay as candidate evidence.
2. Complete final PF-B1/PF-H1 governance review.
3. Integrate the smallest evaluator into the existing shared architecture.
4. Run the formal 0008 test suite and provenance audit.
5. Freeze only after explicit approval and all gates pass.
