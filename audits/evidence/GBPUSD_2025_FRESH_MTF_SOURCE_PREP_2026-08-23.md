# GBPUSD 2025 Fresh MTF Source Preparation — Checkpoint

**Date:** 2026-08-23
**Status:** COMPLETE / CHECKPOINT RECORDED

## What was completed
A source-bound adapter was executed against the uploaded GBPUSD Master 2016–2026 source to derive 2025 H1 and H4 bars.

Fresh outputs:
- H1: **6,216 bars**
- H4: **1,554 bars**

The generated bars preserve source-backed volume and use no invented volume semantics.

## Adapter boundary
`GBPUSD_2025_H1_H4_SOURCE_ADAPTER_V1.py`

The adapter:
- requires timestamp/OHLC/volume/volume_available/source_period fields;
- limits processing to 2025-01-01 through 2025-12-31;
- rejects duplicate source timestamps;
- rejects unavailable or non-positive source volume;
- resamples M1 -> H1/H4 using OHLC + summed volume;
- does not fill missing bars/gaps;
- does not add trading direction or decision logic.

## Governance
- 2025 remains protected OOS and is not used for tuning/optimization.
- No gaps are synthetically filled.
- No new directional rule is introduced.
- This checkpoint only covers fresh H1/H4 source preparation.

## Architecture note
The project already has a separate `MTF_ALIGNMENT_V1` artifact supporting M5/M15/M30/H1/H4/D1 and a Dynamic MTF binding adapter. This checkpoint does **not** replace or rebuild those components.

## Next gate
Feed the fresh 2025 source-backed timeframes into the existing Market State / Market Reader boundary and prove the runtime path without changing component semantics.
