# MT5 Raw Capture V1.3 — raw clock, no UTC inference

## Why V1.3 exists
The legacy producer serializes MqlRates.time with a Z suffix. The reviewed EA does not itself perform a broker timezone/DST conversion or attach per-bar timezone evidence. A suffix alone is not proof of UTC provenance.

V1.3 is a separate, versioned producer. It does not modify V1/V1.1/V1.2 files or historical CSVs.

## What it emits
- bar_time_epoch_seconds_raw: numeric MqlRates.time preserved without formatting or conversion.
- bar_time_source_clock=MT5_MQLRATES_DATETIME_RAW.
- bar_time_utc_status=UNVERIFIED.
- Current terminal server time, last quote server time, host GMT estimate, and host local time as separate wall-clock observations.
- Broker server identity, terminal/source identity, capture version, closed-bar flag, OHLC, volumes, and spread.
- Six native timeframes: M5, M15, M30, H1, H4, D1.

## Explicit non-claims
V1.3 does not claim that the raw epoch value is verified UTC, derive a historical broker offset, infer DST, or create bar-close timestamps. The contemporaneous server-minus-host diagnostic is not a historical timezone rule. Host TimeGMT() is not promoted to an authoritative clock.

## Downstream safety
The V1.3 Python contract rejects UTC fields and any status other than UNVERIFIED. Its CSV adapter preserves the raw epoch value and does not convert it to datetime. These rows are capture/audit evidence only; they are not eligible for UTC MTF joins.

The existing Clock Provenance Gate V1 remains the separate admission gate. UTC alignment requires independently sourced, documented per-bar timezone policy and evidence. No policy, offset, or evidence is fabricated by this producer.

## Installation and output
Compile MT5_Raw_Capture_Only_V1_3.mq5 in MetaEditor and attach it to one MT5 chart. Enable desired symbols in Market Watch. Output is mt5_raw_capture_v1_3.csv in the MT5 Common Files area. It captures the latest closed bar per visible symbol and each of the six timeframes.

## Validation limits
GitHub Actions can run Python contract and CSV tests, but cannot compile MQL5 or prove behavior inside a live MT5 terminal. MetaEditor compilation and Demo-terminal capture/inspection remain mandatory. This producer does not place trades.

## Data governance
Do not tune or calibrate on 2025 OOS. Do not change Murphy/Nison/TIZ/Similarity/Risk semantics. Do not start MTF joins or feature calculations from V1.3 rows while clock status is UNVERIFIED.
