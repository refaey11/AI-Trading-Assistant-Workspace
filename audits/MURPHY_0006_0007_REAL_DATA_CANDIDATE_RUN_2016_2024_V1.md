# Murphy 0006–0007 Real-Data Candidate Evidence Run V1

Date: 2026-08-12
Historical window: 2016-01-01 through 2024-12-31
2025: excluded
Status: CANDIDATE EVIDENCE ONLY

## Canonical Workspace inputs

Reconstructed from the uploaded three-part `GBPUSD_RULE_EVALUATOR_V2` Workspace archive:

- `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv` — 808 rows
- `TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv` — 806 lines
- `DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv` — 2,544 D1 bars

The Workspace audit independently lists these canonical artifacts and their sizes/paths. The Pivot lineage identifies `D1/GBPUSD_D1_STRUCTURE.csv` as the source file.

## Rule selection

- MURPHY_0006: LOW line family + UP direction
- MURPHY_0007: HIGH line family + DOWN direction

These mappings remain the project's working mapping and are not promoted to a production source lock by this run.

## Candidate construction

For each matching Geometry V1 line:
1. Use the existing two Geometry V1 anchors.
2. Require the line availability timestamp.
3. Select the first confirmed same-type Pivot V2 event after anchor 2 whose availability is not earlier than line availability.
4. Calculate the mathematical line price at the candidate timestamp using the Geometry V1 slope.
5. Join D1 OHLC for the candidate date and record whether the daily range intersects the mathematical line.
6. Select the first subsequent opposite-type confirmed pivot, available no earlier than the candidate availability, as a reaction candidate.
7. Record directional consistency as evidence only.
8. Do not apply a touch tolerance, reaction magnitude, ATR threshold, percentage threshold, hidden lookback, or production break rule.

## Results

| Rule | Candidate lines | D1 range intersects line | Reaction candidates | Directionally consistent reaction candidates | Exact zero-distance touch |
|---|---:|---:|---:|---:|---:|
| MURPHY_0006 | 197 | 32 | 196 | 193 | 0 |
| MURPHY_0007 | 206 | 30 | 206 | 203 | 0 |

## Interpretation

This is the first run against the actual canonical Workspace data rather than synthetic unit-test fixtures.

The results are **not** PASS/FAIL rule outcomes. `daily_range_intersects_line` is a geometric observation, not an approved successful-touch operator. A reaction candidate is evidence, not an approved reaction operator. No-break remains observation-only because no project-approved 0006/0007 break/no-break binding was established.

The result therefore remains `CANDIDATE_ONLY` for every row.

## Safety / provenance

- No 2025 data used.
- No tuning or threshold selection performed.
- Existing Pivot V2 and Geometry V1 outputs were reused without modification.
- Existing D1 OHLC evidence was reused only as price-bar evidence.
- No Murphy 3%/2-day general break example was automatically bound to 0006/0007.

## Next gate

1. Preserve this real-data candidate output.
2. Verify whether an approved project/source operator can convert candidate touch/reaction evidence into deterministic confirmation.
3. If not available, keep production evaluation `NOT_EVALUABLE` rather than inventing a threshold.
4. Historical QA can only begin after the exact operator gate is closed.
