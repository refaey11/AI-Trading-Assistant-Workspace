# MT5 Forex-Only Raw Capture V1.2

## Purpose and safety boundary

This separate Expert Advisor exports the latest **closed** bars for M5, M15,
M30, H1, H4, and D1. It scans symbols currently visible in Market Watch.
It remains data-capture only: no trade requests, position management,
indicators, feature formulas, BUY/SELL logic, or risk sizing.

## V1.2 forex classification (two independent gates)

With `CaptureForexOnly=true` (default), a symbol is accepted only when:

1. MT5 reports `SYMBOL_CALC_MODE_FOREX` or
   `SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE`; and
2. MT5 reports distinct base and profit currencies, and both codes appear
   in the versioned three-letter currency allowlist embedded in the EA.

The allowlist covers ISO 4217 currency codes and explicitly includes broker-used
`CNH`, plus legacy `HRK` and `RUR`. Precious-metal codes (for example XAU,
XAG) and crypto/other instrument codes (for example BTC, ETH, XRP) are not
allowlisted. Symbol-name suffixes are not used for classification.

This is a conservative fail-closed filter. A legitimate broker FX symbol whose
base/profit code is not in the allowlist will be skipped. Do not add a code
without checking the broker's MT5 symbol specification and confirming it is a
currency, not a CFD/metal/crypto token.

## Important behavior

- Only symbols currently visible in Market Watch are scanned. The EA does not
  automatically enable every broker symbol.
- Missing history or symbols are reported, not silently inferred.
- Output uses a new filename, `mt5_raw_capture_fx_v1_2.csv`, so V1 and V1.1
  files remain untouched.
- CSV retains the existing 20-column raw-bar contract. The capture version is
  `1.3.0`; no timestamp offset conversion is applied.

## Installation and test

1. Keep the V1 and V1.1 EAs and their CSV files untouched.
2. Place `MT5_Forex_Only_Raw_Capture_V1_2.mq5` in `MQL5/Experts`.
3. Compile in MetaEditor. Record the exact compiler result; do not proceed if
   there are errors or warnings.
4. Attach V1.2 to a Demo chart, leave `CaptureForexOnly=true`, and enable
   Algo Trading only for this data-capture EA.
5. Confirm the Experts log says V1.2 started and explicitly mentions the
   FX calculation mode plus base/profit currency-code filter.
6. Let it run for several minutes, then inspect the new
   `mt5_raw_capture_fx_v1_2.csv` in MT5 Common Files.
7. Confirm the output contains only broker-confirmed currency pairs. Check
   several ordinary and exotic pairs, and confirm that metals/crypto visible
   in Market Watch do not appear.
8. Compare the resulting symbols against the broker's intended FX universe.
   The filter's success on one sample is not proof of complete broker coverage.

## Data validation and age

The V1.1 sample file supplied for this audit had 3,568 rows and 222 distinct
symbols. Its 20-column schema and basic raw-bar checks passed, with no missing
cells, unsupported timeframes, unfinished bars, invalid OHLC geometry,
negative volume/spread values, or duplicate symbol/timeframe/bar-time keys.
However, the sample contained crypto and metal instruments, so it is not
accepted as Forex-only data.

The sample also contained old bar timestamps (oldest: 2022-12-29 UTC; newest:
2026-11-18 02:25 UTC). This is a data-freshness observation, not a reason to
rewrite timestamps or silently discard history. Inspect per-symbol/per-timeframe
freshness and broker history availability before downstream use.

## Explicit limitations and gates

- MetaEditor compilation and terminal behavior must be verified on the user's
  Exness Demo terminal.
- Broker symbol classification, Market Watch coverage, and historical
  completeness remain to be verified on the target terminal.
- This is not a feature producer and generates no trend regimes or MTF score.
- Do not use 2025 OOS for tuning, calibration, or feature selection.
- No merge to main and no live orders are part of this work.
