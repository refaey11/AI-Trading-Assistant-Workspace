# MULTI_TIMEFRAME_READER_V1 — Audit Evidence

Date: 2026-08-21
Status: PARTIAL

## Archive evidence
Archive contents include five pair-level `*_MTF_H4_H1.csv` outputs, `CONTRACT.json`, `README.md`, coverage, and latest readings.

## Contract
- Status: `RESEARCH_ONLY`
- Implemented timeframes: H4 and H1
- H4: higher-timeframe context
- H1: local market structure
- M15: explicitly not implemented because the available master datasets are H1; M15 must not be fabricated from H1
- Trade decision: not generated

## Output schema
Pair-level outputs contain:
`timestamp, close, trend, structure, volume_ratio, atr, h4_time, h4_trend, h4_structure, h4_volume_ratio, mtf_state`

Declared states in README:
- ALIGNED_BULL
- ALIGNED_BEAR
- COUNTER_TREND
- MIXED

## Runtime-output integrity checks
All five pair outputs were directly checked.

| Pair | Rows | Duplicate timestamps | Sorted | Coverage |
|---|---:|---:|---|---|
| EURUSD | 61,435 | 0 | PASS | 2016-01-03 to 2025-12-31 |
| GBPUSD | 61,417 | 0 | PASS | 2016-01-03 to 2025-12-31 |
| USDJPY | 61,416 | 0 | PASS | 2016-01-03 to 2025-12-31 |
| USDCAD | 61,420 | 0 | PASS | 2016-01-03 to 2025-12-31 |
| XAUUSD | 58,504 | 0 | PASS | 2016-01-03 to 2025-12-31 |

## Key compatibility finding
The module is explicitly a **two-timeframe implementation: H4 + H1 only**. It does not implement M15 and explicitly refuses to fabricate M15 from H1.

Therefore this module must not be represented as the final six-timeframe reader without a compatibility layer or later real-data implementation for the additional timeframes.

## AS-OF / no-lookahead finding
For every checked row, `h4_time <= timestamp`; however `h4_time + 4h > timestamp` for every row. This is consistent with `h4_time` representing an H4 bucket/start label, but the archived outputs alone do not prove whether the H4 fields were derived only from completed H4 bars or from information inside an H4 bar that was still forming.

No generator/source code is present in this archive. Therefore:
- output timestamp ordering: PASS
- future timestamp mapping: no direct future key observed
- completed-bar / AS-OF semantics: UNPROVEN
- strict no-lookahead: UNPROVEN

## OOS governance
Historical outputs extend into 2025. For project QA and any later fitting/tuning, use 2016–2024 only. Preserve 2025 as final OOS and do not tune on it.

## Final verdict
- Contract/design: PASS
- Historical output integrity: PASS
- H4/H1 context classification: PASS as archived runtime output
- Six-timeframe compatibility: PARTIAL / additional timeframes not implemented here
- AS-OF/no-lookahead provenance: UNPROVEN
- Final status: **PARTIAL — AUDITED / GAPS REGISTERED**

## Resume point
Do not rebuild this module. Keep the explicit H4/H1 scope. Continue the Market Pipeline audit with **Time / Dynamic Timeframe Context**, then perform the cross-module compatibility matrix and close only proven gaps.
