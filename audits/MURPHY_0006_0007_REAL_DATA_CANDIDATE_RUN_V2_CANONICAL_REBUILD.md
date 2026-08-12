# Murphy 0006–0007 — Canonical Real-Data Candidate Rebuild V2

Date: 2026-08-13
Status: CANDIDATE EVIDENCE ONLY — NOT PRODUCTION CONFIRMATION

## Why this rebuild was required

The prior GitHub candidate-evidence CSV was malformed/partial and could not be treated as a canonical dataset. It has been removed rather than preserved as evidence.

The underlying 241-file `GBPUSD_RULE_EVALUATOR_V2` workspace transfer was reconstructed from the uploaded split parts. The four `.bcut` files contain a 153-byte metadata prefix followed by raw chunk data; those metadata prefixes were stripped before concatenating the three workspace parts.

Reconstructed archive verification:
- entries: 241
- canonical D1 geometry file: present
- canonical D1 PIVOT_SEQUENCE_V2 file: present
- canonical D1 OHLC/DMI file: present

## Canonical inputs

1. `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv`
   - 808 rows
   - confirmed pivots
   - availability timestamp after confirmation

2. `TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv`
   - 806 rows
   - 12 columns
   - line geometry + availability only

3. `DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv`
   - 2,544 D1 bars
   - contains OHLC plus DMI/ADX fields
   - only OHLC fields are used for this candidate evidence run

## Existing runner reused

`/scripts/run_murphy_0006_0007_real_data_candidates.py`

No new trendline geometry or pivot detector was created.

The runner's existing mapping is:
- `LOW + UP` -> `MURPHY_0006`
- `HIGH + DOWN` -> `MURPHY_0007`

Candidate selection is source-data based:
- same pivot family as the line
- pivot timestamp after the second anchor
- pivot availability not earlier than line availability
- first eligible subsequent pivot is recorded as the third-touch candidate
- D1 range intersection is recorded as raw evidence
- first eligible opposite pivot after the candidate is recorded as a reaction candidate
- no-break is explicitly `OBSERVATION_ONLY`
- evidence status is explicitly `CANDIDATE_ONLY`

## Reproducible result

| Rule | Candidate lines | D1 range/line intersections | Reaction candidates | Directionally consistent reactions | Exact zero-distance touches |
|---|---:|---:|---:|---:|---:|
| MURPHY_0006 | 197 | 32 | 197 | 193 | 0 |
| MURPHY_0007 | 206 | 30 | 206 | 203 | 0 |
| **Total** | **403** | **62** | **403** | **396** | **0** |

Generated candidate CSV SHA-256:
`5169513a7cc48ad4204186ceb65a9b0032bb05e8b24a580ce43aea07271442e4`

Generated rows: 403.

## Interpretation

These numbers are NOT confirmation rates and NOT rule performance.

They establish only that canonical D1/Pivot/Geometry inputs can produce a reproducible candidate-evidence population for 0006/0007.

The runner does not introduce a touch tolerance, ATR threshold, percentage threshold, fixed lookback, or 3%-for-2-days rule.

The existing project contract requires production confirmation to remain blocked/not-evaluable until an approved deterministic no-break/confirmation operator is available.

2025 was not used.

## Cleanup / provenance correction

The malformed prior candidate CSV was deleted from the branch. This audit is the authoritative record of the corrected run; the full CSV should be regenerated from the canonical workspace using the existing runner rather than committed as a manually copied artifact.
