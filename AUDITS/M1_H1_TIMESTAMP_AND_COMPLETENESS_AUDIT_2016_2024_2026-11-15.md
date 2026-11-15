# M1 to H1 timestamp and completeness audit (2016-2024)

**Date:** 2026-11-15  
**Scope:** GBPUSD only, development years 2016-2024. 2025 OOS and 2026 rows were excluded before all measurements.  
**Method:** read-only audit of the existing Dropbox M1 and H1 master archives. No runtime inputs were modified.

## Source coverage and integrity

| Metric | Result |
|---|---:|
| M1 rows | 3,351,523 |
| H1 rows | 55,192 |
| M1 invalid/non-numeric volume rows | 0 |
| M1 duplicate timestamps | 0 |
| M1 off-minute timestamps | 0 |
| H1 duplicate timestamps | 0 |
| Active M1 hours | 55,998 |
| Hours with 60 unique M1 minutes | 53,145 |
| Hours with fewer than 60 unique M1 minutes | 2,853 |
| Partial hours containing internal missing minutes | 2,521 |
| Partial hours contiguous from first to last observed minute | 332 |
| H1 rows with 60 unique M1 minutes | 50,731 |

The 2,853 partial hours must not all be classified as market-session edges: 2,521 contain internal missing minutes. Any completeness gate needs a source/session policy; blindly accepting all partial hours or blindly rejecting all of them would both be unjustified.

## Timestamp and OHLC alignment

All 55,192 H1 timestamps are exactly on the hour boundary and equal the start of their corresponding UTC hour; none equals the hour-end boundary.

The audit independently aggregated M1 OHLC inside each timestamp hour and compared each H1 OHLC field with absolute tolerance 1e-8:

| Comparison | Matching H1 rows |
|---|---:|
| H1 open vs same-hour M1 first open | 24,908 |
| H1 high vs same-hour M1 max high | 24,914 |
| H1 low vs same-hour M1 min low | 24,908 |
| H1 close vs same-hour M1 last close | 24,916 |
| All four OHLC fields match same-hour M1 aggregation | 24,870 |
| All four match and hour has 60 M1 minutes | 23,070 |
| All four match previous-hour M1 aggregation | 0 |

This is strong evidence for same-hour/open-time alignment on the rows that match, but it does **not** certify the entire H1 file's OHLC lineage: fewer than half of all H1 rows match all four M1-derived OHLC fields. The remaining rows may reflect source differences, data gaps, or other construction differences and require provenance before being classified.

## Proven code-path timing issue

The existing M1-to-H1 volume reconstruction in `OOS_2025/run_murphy_0021_2025_fresh_v1.py`:
1. assigns each M1 row to `timestamp.floor("h")`;
2. sums volume per hour;
3. compares that hour's volume with the previous available hourly aggregate;
4. labels the result with the hour-start timestamp.

The volume for a bucket beginning at 17:00 is not complete until the 17:59 M1 bar has closed, i.e. at the 18:00 boundary. Labeling that complete-bucket result as available at 17:00 creates a one-hour availability mismatch if the timestamp is treated as decision/as-of time.

The Gate3C path also needs a separate timestamp contract review:
- `tools/gate3c_build_single_event_bundle_v1.py` reads the H1 row at or before event time and uses its close as the Brain row's entry-price fallback.
- `OOS_2025/build_single_event_risk_evidence_v1.py` selects the exact H1 row at event timestamp and uses its close as entry when no explicit entry field exists.
- The current event bundle does not carry distinct `bar_open_time`, `bar_close_time`, and `available_at` fields.

This is a proven **timestamp-contract gap / potential look-ahead**, not yet a license to shift all event timestamps: Murphy, Market State, Nison, MTF, risk and historical evidence may have their own timestamp conventions. Those must be reconciled together before changing the runtime.

## Safe next step

Create a separate, read-only event-time compatibility audit that records each source's row timestamp, bar interval, and earliest defensible availability time for one selected 2016-2024 event. Only after that audit should we propose the smallest approved runtime contract change.

No volume thresholds, rule semantics, risk rules, book knowledge, Brain direction, or execution behavior were changed. No 2025 OOS data was used for tuning or modification.

## Gate3C source timestamp neighborhood for the selected event

A second read-only audit downloaded the actual Gate3C source set and inspected the selected event `2020-01-03T00:00:00Z`, plus the nearest prior and following timestamp for each source.

| Source | Exact rows at event | Prior row | Next row | Explicit availability metadata |
|---|---:|---|---|---|
| H1 | 1 | 2020-01-02 23:00 | 2020-01-03 01:00 | None; only `timestamp` |
| Market State | 1 | 2020-01-02 23:00 | 2020-01-03 01:00 | None; only `timestamp` |
| MTF M5 | 1 | 2020-01-02 23:55 | 2020-01-03 00:05 | None; only `timestamp` |
| Nison | 44 | 2020-01-02 23:00 | 2020-01-03 01:00 | None; only `timestamp` |
| Murphy | 2 | 2020-01-02 23:00 | 2020-01-03 01:00 | None; only `timestamp` |

H1 and Market State event OHLC values match exactly: O=1.31256, H=1.31289, L=1.31155, C=1.31207. Their volume field is 0. The separate M1 source has 60 rows in the 00:00-00:59 bucket and a summed volume of 430, but its OHLC does not match the H1/Market State event row. This demonstrates that the separate M1 archive cannot be assumed to be the same price/volume lineage as the H1/Market State source for this event.

The MTF row at 00:00 contains M5=-1, M15=-1, M30=0, H1=+1, H4=+1, D1=+1, score=+1, and context=mixed. Its prior 23:55 row has D1 missing and score=0; its next 00:05 row has the same regimes as 00:00. This is a timestamp transition worth checking against the MTF producer, but the output file contains no bar-close or availability timestamp that proves when those values became knowable.

Nison has 44 event rows. Its per-row provenance text declares `lookahead: none`, but the output still does not expose bar-close/available-at timestamps. Murphy has two event rows: the directional PASS is BEARISH from MURPHY_0021 with source IDs MURPHY_0021|MURPHY_0022|MURPHY_0023; the other row fails. Its output has no explicit availability metadata.

## Code-path compatibility finding

The candidate selector requires exact H1 and Market State timestamps and accepts the latest MTF row with timestamp <= event, provided its age is no more than five minutes. The canonical event builder uses the event's H1 and Market State slices, and the risk evidence builder uses the H1 close at the exact event timestamp as entry when no explicit entry field exists.

Therefore the system currently aligns **labels**, not proven **availability times**. The files do not carry the metadata needed to prove that H1 close, MTF M5 state, Murphy PASS, Nison fan-in, and Market State values were all available at the event timestamp. This is a real contract/provenance gap. It is not sufficient evidence to mechanically shift all sources by one hour or five minutes.

## Required next gate

Before any runtime change, locate or reconstruct from source-backed producer contracts:
1. whether H1 timestamps label bar-open or bar-close;
2. whether MTF M5 and higher-timeframe values use only completed bars as of each M5 timestamp;
3. whether Murphy and Nison event timestamps refer to the input bar's open, close, or evaluation/availability time;
4. whether Market State outputs are generated from the same completed H1 bar or use a distinct as-of convention;
5. a single event-time contract carrying `bar_open_time`, `bar_close_time`, and `available_at` per source.

No runtime change is authorized or implemented in this PR. The 2025 OOS freeze remains intact.


## Existing project MTF contract compatibility check

Dropbox also contains a separate component at `/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1/`:
- `README.md` says the reader uses available H1 master data to create H4 context aggregated from H1 and H1 local structure; M15 is intentionally not fabricated from H1 and is deferred until real M15 data exists.
- `CONTRACT.json` labels the component `RESEARCH_ONLY`, lists only H4 and H1, and says no trade decision is generated.
- `MTF_COVERAGE.csv` reports H1/H4 coverage for GBPUSD (61,417 H1 bars and 16,051 H4 bars).
- This separate reader folder also has a GBPUSD H4/H1 output CSV (8.61 MB).

This is a **distinct component** from `/MTF_ALIGNMENT_GBPUSD_V1.zip`, which Gate3C currently consumes and whose annual CSV contains M5/M15/M30/H1/H4/D1 fields. The older H1/H4 reader contract must not be incorrectly imposed on the separate alignment archive. However, the two artifacts demonstrate that the project has multiple MTF products with different declared scopes. The producer, source lineage, and contract for `MTF_ALIGNMENT_GBPUSD_V1.zip` were not found in the repository code search or Dropbox search during this audit. Its six-timeframe fields therefore remain source-backed as file content, but their derivation and bar-availability semantics are not yet verified.

No attempt was made to replace the Gate3C MTF source with the H1/H4 reader output, synthesize M15/M30/M5/D1, or merge the two contracts.
