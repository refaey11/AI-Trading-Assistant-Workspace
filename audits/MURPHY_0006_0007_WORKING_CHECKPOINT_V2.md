# Murphy 0006/0007 — Working Checkpoint V2

Date: 2026-08-13
Status: CHECKPOINTED / READY TO CONTINUE

## Completed state
- PIVOT_SEQUENCE_V2 reused and compatibility checked.
- TRENDLINE_GEOMETRY_V1 reused and compatibility checked.
- Existing Murphy evaluator located and preserved:
  `audits/MURPHY_0006_0007_TRENDLINE_SOURCE_CONTRACT_V1.py`
- Existing evaluator requires upstream `third_touch`, `reaction_bounce`, `no_break`, and confirmation availability.
- Evidence Adapter / Confirmation Evidence Layer / Dataset Builder / QA / CI work is recorded.
- Corrected 2016–2024 historical candidate population remains 347 rows: 166 for 0006 and 181 for 0007.
- Candidate evidence is explicitly `CANDIDATE_ONLY`.

## Deep source findings
Murphy Chapter 4 supports the qualitative chain:
- two points define a tentative trendline;
- third successful test/touch confirms validity;
- price reacts/rebounds from the line;
- a meaningful break is distinguished from a temporary/intraday penetration;
- closing beyond the trendline is more important than mere intraday penetration;
- general price/time filters such as 3% and two consecutive closes are discussed, but these are not proven as an automatic 0006/0007-specific contract.

Project knowledge also documents candlestick-based confirmation around trendlines, but this does not create a source-locked numeric touch/reaction operator for 0006/0007.

## Actual current problem
The missing logic is upstream evidence generation between `TRENDLINE_GEOMETRY_V1` and the existing Murphy evaluator.

Required predicates:
1. `third_touch`
2. `reaction_bounce`
3. `no_break`

Current data can provide raw candidate observations such as line/range intersection, subsequent opposite-pivot candidate, and chronology/availability, but these must not be promoted to the three predicates without an approved operator contract.

## Explicit non-actions
- Do not replace/rebuild Pivot V2 or Geometry V1.
- Do not create a replacement Murphy evaluator.
- Do not invent ATR/pip/%/lookback thresholds.
- Do not automatically bind 3%/2-day filters to 0006/0007.
- Do not use the stale V2 historical artifact containing 2025/2026 rows.
- Do not tune on 2025.

## Next exact step
Perform field-by-field reconciliation of the actual TRENDLINE_GEOMETRY_V1 output/schema and related source contracts against `third_touch`, `reaction_bounce`, and `no_break`. Determine whether equivalent authoritative fields already exist. If yes, implement only the smallest adapter and tests. If no, record the exact missing contract and retain `NOT_EVALUABLE`.
