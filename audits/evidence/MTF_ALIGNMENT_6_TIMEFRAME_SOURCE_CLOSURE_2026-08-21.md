# MTF Alignment 6-Timeframe Source Closure — 2026-08-21

## Purpose
Close the previously open provenance gap for the six timeframe inputs expected by the active Decision Brain runtime, using the recovered `MTF_ALIGNMENT_GBPUSD_V1` artifacts as evidence.

## Evidence reviewed
Recovered artifacts include a final manifest and yearly aligned GBPUSD M5 datasets, including:

- `FINAL_MANIFEST.csv`
- `GBPUSD_M5_MTF_ALIGNMENT_2017.csv`
- `GBPUSD_M5_MTF_ALIGNMENT_2018.csv`
- `GBPUSD_M5_MTF_ALIGNMENT_2020.csv`
- `GBPUSD_M5_MTF_ALIGNMENT_2022.csv`
- `GBPUSD_M5_MTF_ALIGNMENT_2026.csv`

The source package is split across two uploaded parts and was repaired/extracted before inspection.

## What the source establishes
The recovered MTF Alignment source uses M5 as the base observation timeframe and carries aligned higher/lower-context features for the six-timeframe set:

`M5 -> M15 -> M30 -> H1 -> H4 -> D1`

The recovered aligned datasets expose timeframe-specific feature families used for market context, including trend-regime fields and other structure/context features. The source also exposes aggregate MTF fields such as:

- `mtf_trend_score`
- `mtf_bullish_count`
- `mtf_bearish_count`
- `mtf_neutral_count`
- `mtf_context`

This closes the prior statement that the provenance of the six Decision Brain timeframe inputs was unproven. The six-timeframe source is now identified as the recovered `MTF_ALIGNMENT_GBPUSD_V1` dataset family.

## Decision Brain compatibility
The active `decision_brain.py` expects:

- `mtf_trend_score`
- `M5_trend_regime`
- `M15_trend_regime`
- `M30_trend_regime`
- `H1_trend_regime`
- `H4_trend_regime`
- `D1_trend_regime`

These names align directly with the recovered MTF Alignment evidence model at the field-family level. Final runtime compatibility must still be demonstrated by executing the governed chain against actual recovered rows; this audit does not claim a completed runtime PASS.

## Anti-leakage / alignment boundary
The recovered source documents that higher-timeframe information is aligned to the M5 base only after the relevant source candle has closed. This is the provenance basis for treating the recovered MTF features as point-in-time aligned rather than freely forward-filled future context.

Runtime validation of this boundary remains part of the end-to-end test evidence; this document records source provenance and contract compatibility, not a new independent backtest result.

## Dataset coverage boundary
Recovered yearly artifacts show the MTF Alignment dataset family spanning historical years through 2026. Project governance remains:

- historical development/tuning must preserve the project split rules;
- 2025 remains protected Out-of-Sample and must not be used for tuning;
- 2026 availability does not itself authorize live execution or tuning.

## Closure status

| Item | Status |
|---|---|
| Six-timeframe source provenance | CLOSED / EVIDENCE FOUND |
| M5/M15/M30/H1/H4/D1 source family | CONFIRMED |
| Aggregate MTF context fields | CONFIRMED |
| Decision Brain field-name compatibility | SUPPORTED; runtime test pending |
| Time/Session Context as separate module | NOT CLOSED by this artifact |
| Dynamic Timeframe Context as separate module | NOT CLOSED by this artifact |
| Full End-to-End runtime PASS | NOT YET CLAIMED |

## Correction to prior audit position
Any prior note stating that the source of the six timeframe inputs was still unproven is superseded by this evidence record. The remaining open work is not discovery of the six-timeframe source; it is runtime execution/validation and separate recovery of any independent Time/Session or Dynamic Timeframe Context contracts.
