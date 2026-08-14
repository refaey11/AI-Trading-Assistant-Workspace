# Murphy 0006/0007 — Canonical Input Replay Blocker V1

Date: 2026-08-14
Status: REPLAY BLOCKED BY INPUT LINEAGE MISMATCH

## What was verified
The complete split GBPUSD_RULE_EVALUATOR_V2 workspace was reconstructed successfully from the uploaded parts. The canonical files were recovered:
- PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv
- TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv

The newly uploaded GBPUSD_M1_MASTER_2016_2026_V1.zip was also inspected successfully.

## Critical finding
The newly uploaded M1 dataset cannot currently be treated as the source dataset for the canonical D1 Pivot V2/Geometry V1 outputs without proving the D1 session/boundary/source lineage.

Concrete check:
- Canonical Pivot V2 first LOW: 2016-01-21, price 1.43519.
- Aggregating the newly uploaded M1 file by calendar date gives 2016-01-21 low = 1.40792.
- Therefore the new M1 file does not reproduce the canonical D1 bar used by the Pivot V2 artifact under the simple calendar-day aggregation.

## Consequence
Do NOT run a "fresh" 0006/0007 replay using the new M1-derived D1 bars while keeping the canonical Pivot/Geometry. That would mix two different data lineages and could create false mismatches.

## Existing evidence
The project already records 2016–2024 D1 evidence and a reconciled 0006/0007 result of 8 + 7 = 15 with 15/15 reference reconciliation. This remains QA evidence, not a production freeze.

## Exact next input required for an independent canonical replay
Recover the exact D1 source used by PIVOT_SEQUENCE_V2 (or its documented session/timezone aggregation contract), then run:
D1 source -> canonical Pivot V2 -> canonical Geometry V1 -> 0006/0007 Event Operator -> 2016–2024 QA.

The newly uploaded M1 dataset remains useful raw market data, but it is NOT silently substituted for the canonical D1 source.

## Guardrails
- Do not rebuild Pivot V2.
- Do not rebuild Geometry V1.
- Do not tune 2025.
- Do not introduce 3%, 2-day, ATR, pip, percentage, or hidden lookback thresholds.
- Do not declare production freeze from the existing 15/15 reconciliation alone.
