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