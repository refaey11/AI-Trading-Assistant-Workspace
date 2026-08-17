# Nison Runtime Bridge Execution V1
Date: 2026-08-17
Branch: nison-batch-v1

## Runtime access resolved
The project workspace archive was staged locally and the existing D1 OHLC data was extracted from the workspace artifact:
`DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv`

The extracted runtime dataset contains:
- 2,544 rows
- 2016-01-03 through 2024-12-31
- timestamp, open, high, low, close
- source_timeframe=D1
- no 2025 rows

## Real structural batch execution
Using source-locked structural relations only (no invented qualitative thresholds), the following formation layers were replayed:

| Rule | Setup | Structural result | Canonical status |
|---|---|---:|---|
| 0001 | Bullish Engulfing | 206 candidates | NOT_EVALUABLE pending source-defined trend/confirmation/invalidation gates |
| 0002 | Bearish Engulfing | 197 candidates | NOT_EVALUABLE pending source-defined trend/confirmation/invalidation gates |
| 0015 | Tweezers Top | 1 exact-high candidate | NOT_EVALUABLE because source says equal or nearly equal + confirmation |
| 0016 | Tweezers Bottom | 3 exact-low candidates | NOT_EVALUABLE because source says equal or nearly equal + confirmation |
| 0019 | Bullish Counterattack Lines | 0 exact structural candidates under the source-specified gap + equal-close relation | NOT_EVALUABLE |
| 0020 | Bearish Counterattack Lines | 0 exact structural candidates under the source-specified gap + equal-close relation | NOT_EVALUABLE |
| 0034 | Separating Lines | 0 exact same-open opposite-color candidates | NOT_EVALUABLE pending confirmation/context gate |

## Integrity checks
- Dataset is monotonic by timestamp.
- Dataset is within the approved 2016–2024 historical window.
- 2025 is excluded.
- No future candle is used to identify a formation at its timestamp.
- Qualitative terms such as `long`, `near`, `nearly`, `strong`, and confirmation requirements were NOT converted into invented thresholds.

## Interpretation
These are structural candidate counts, not PASS/FREEZE counts. A candidate becomes canonical PASS only after all source-required context, confirmation, invalidation, availability, no-lookahead, and historical-QA gates are satisfied.

## Next batch
Continue the same runtime bridge over the remaining source-mappable Nison formation rules, reusing shared operators and preserving NOT_EVALUABLE where source semantics remain qualitative.