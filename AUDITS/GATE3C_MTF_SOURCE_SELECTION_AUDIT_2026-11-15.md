# Gate3C MTF Source Selection Audit — 2026-11-15

## Status
CONFIRMED SOURCE-SELECTION DEFECT — runtime fix not applied in this diagnostic PR.

## Scope
Diagnostic-only review of the existing MTF source archive and the Gate3C event builder. No source data, runtime behavior, decision semantics, or risk contracts were modified. 2025 remains protected OOS and was not used for this analysis.

## Findings

### 1. Annual source files contain only a leading incomplete-timeframe prefix
The exact Dropbox archive `/MTF_ALIGNMENT_GBPUSD_V1.zip` contains annual GBPUSD M5 MTF alignment CSVs for 2016–2026. The 2016–2024 annual files contain 671,601 rows in total.

Across the 2016–2024 annual files:
- 2,512 missing values across the required MTF fields.
- Zero nonnumeric nonblank values.
- Every missing value is confined to a contiguous prefix beginning at row offset 0 in its annual file.
- No missing values were found after the first valid value for the corresponding field.

The prefix lengths match the timeframe's initial incomplete bar exposure:
- M15: 3 M5 rows (15 minutes).
- M30: 6 M5 rows (30 minutes).
- H1: 12 M5 rows (60 minutes).
- H4: 24–48 M5 rows depending on the annual market-open boundary.
- D1: 83–288 M5 rows depending on the annual market-open boundary.

This is consistent with unavailable higher-timeframe values until the first corresponding bar is complete. It does not justify imputation, row dropping, or treating those rows as evaluable. Under the existing MTF binding contract, required missing timeframe data must remain NOT_EVALUABLE.

### 2. Gate3C currently selects the wrong annual MTF file for a 2020 event
In `tools/gate3c_build_single_event_bundle_v1.py`, `find_csv()`:
1. scans every CSV below the MTF root;
2. scores candidate filenames by the presence of `GBPUSD`, `MTF`, and `ALIGNMENT`;
3. sorts ties lexicographically by path;
4. returns the first candidate.

All annual files receive the same hint score of 3. Therefore the lexicographically first file is `GBPUSD_M5_MTF_ALIGNMENT_2016.csv`, regardless of the event year.

The builder then calls `read_rows_at(..., exact=False)`, which selects the last row at or before the event timestamp. For the verified Gate3C event `2020-01-02T01:00:00Z`, this selects the final row from the 2016 file:

- Selected file: `GBPUSD_M5_MTF_ALIGNMENT_2016.csv`
- Selected row timestamp: `2016-12-30 16:55:00+00:00`
- M5: 0
- M15: 1
- M30: 1
- H1: 0
- H4: -1
- D1: -1
- MTF score: 0

These values match the MTF values recorded in the earlier Gate3C event artifact for 2020-01-02 01:00. The previous Gate3C PASS therefore did not establish point-in-time MTF validity for that event; it consumed stale 2016 MTF evidence.

### 3. Correct annual source at the event timestamp is incomplete
The 2020 annual file contains an exact row at `2020-01-02 01:00:00+00:00`:
- M5: 1
- M15: 1
- M30: 1
- H1: 1
- H4: missing
- D1: missing
- MTF score: 1

The current Gate3C builder's required-field validation would correctly reject this row as missing H4/D1. Therefore, once the source selection is corrected, this particular event should be BLOCKED / NOT_EVALUABLE at the MTF stage, not passed using stale 2016 values.

## Required controlled fix (not included here)
A separate, reviewed runtime fix should:
1. select the annual MTF file matching the event year, or use a verified continuous source with a point-in-time timestamp join;
2. reject ambiguous/missing source candidates rather than falling back lexicographically;
3. enforce event-time/as-of freshness and retain exact source path, row timestamp, and source provenance in the event artifact;
4. preserve NOT_EVALUABLE when any required timeframe is unavailable;
5. add regression tests proving a 2020 event can never consume a 2016 annual MTF row;
6. rerun Gate3C on a valid event after the fix. Do not change the event timestamp merely to force a PASS.

## Governance
- No MTF values imputed or translated.
- No rows dropped.
- No MTF direction generation added.
- No Brain, Murphy, Nison, Similarity, TIZ, or risk semantics changed.
- No 2025 tuning, calibration, or use.
- This audit does not authorize a runtime fix or PR merge.
