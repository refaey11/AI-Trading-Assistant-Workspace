# Market State Volume Lineage & Compatibility Evidence — 2026-08-21

## Status
**OPEN GAP — SOURCE LOCATED / COMPATIBILITY AUDIT NEXT**

This is an evidence checkpoint. It does **not** claim that the Market State volume gap is fixed.

## Evidence chain

### 1. Historical Market State outputs
Reviewed files include:
- EURUSD_MARKET_STATE.csv
- GBPUSD_MARKET_STATE.csv
- USDJPY_MARKET_STATE.csv
- USDCAD_MARKET_STATE.csv
- XAUUSD_MARKET_STATE.csv

Observed historical-output condition:
- volume fields are zero / non-informative in the existing Market State outputs.
- therefore the historical output must not be interpreted as proof that real volume was unavailable upstream.

### 2. 2020–2024 volume source exists
Existing `VOLUME_CONFIRMATION_V2` artifacts provide M1-derived volume context for GBPUSD for 2020–2024.

Direct evidence observed from the existing volume artifact includes fields:
- `bar_close_timestamp`
- `volume`
- `m1_count`
- `previous_volume`
- `volume_direction`
- `volume_change_available`
- `volume_ratio_to_previous`
- `source_timeframe`

Observed source lineage:
- `M1_TitanFX_2020_2024`

Observed non-zero examples exist, including values such as `1315` and `1835`, with `m1_count=60` for H1 examples. Therefore the project contains usable upstream volume evidence for the 2020–2024 period.

### 3. Timeframe coverage
Existing volume artifacts have been identified for GBPUSD across:
- M5
- M15
- M30
- H1
- H4
- D1

Therefore the six-timeframe project architecture is compatible with the existence of real volume context for the 2020–2024 source window.

### 4. Historical unavailable period
For the earlier historical period before the M1-derived source window, volume availability must be represented as unavailable rather than silently coerced to numeric zero.

Governance rule already established in the project:

`volume unavailable != zero`

Accordingly, an unavailable source must not automatically create a market conclusion such as `CONTRACTION` solely because a missing value was represented as zero.

## Current lineage diagnosis

```text
2016–2019 (or earlier portion outside the confirmed M1 source window)
    -> volume source not confirmed as available
    -> must preserve explicit unavailable semantics

2020–2024
    -> M1_TitanFX source exists
    -> VOLUME_CONFIRMATION_V2 artifacts contain real non-zero volume context
    -> existing historical MARKET_STATE outputs still show non-informative/zero volume
    -> integration or propagation gap remains OPEN
```

## What is proven
1. Real upstream volume data exists for the confirmed 2020–2024 source window.
2. The existing historical Market State output does not faithfully demonstrate that upstream volume was absent.
3. The gap is therefore a lineage/availability/propagation question, not proof that the project lacks volume data.

## What is NOT yet proven
The following remain unverified and must not be assumed:
- exact `MARKET_STATE_READER_V1` input contract for volume
- exact timestamp semantics expected at the reader boundary
- whether direct field names are already compatible
- whether a transformation/adapter is required
- exact source of the zeroing behavior
- AS-OF/completed-bar compatibility of the volume handoff

## Required next test: Compatibility Audit
Before any code or data modification:

1. Extract the exact output contract of `VOLUME_CONFIRMATION_V2`.
2. Extract the exact input contract of `MARKET_STATE_READER_V1`.
3. Compare field names, types, semantics, timestamps, timeframe meaning, and availability behavior.
4. Verify AS-OF/completed-bar mapping.
5. Determine the smallest deterministic fix, if a mismatch is proven.
6. Run standalone GBPUSD QA on 2016–2024 only.
7. Keep 2025 excluded from tuning and iterative fitting; preserve it for final OOS evaluation.

## Resume point
**Do not rebuild the Volume module or Market State Reader. Resume at: `VOLUME_CONFIRMATION_V2 -> MARKET_STATE_READER_V1 compatibility audit`.**
