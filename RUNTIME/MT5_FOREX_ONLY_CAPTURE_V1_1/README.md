# MT5 Forex-Only Raw Capture V1.1

## Purpose and safety boundary

This separate Expert Advisor exports the latest **closed** bars for M5, M15,
M30, H1, H4, and D1. It scans symbols currently visible in Market Watch and,
by default, includes only symbols whose MT5 trade calculation mode is
`SYMBOL_CALC_MODE_FOREX` or `SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE`.

It is data-capture only. It contains no trade requests, position management,
indicators, feature formulas, BUY/SELL logic, or risk sizing.

## Important behavior

- `CaptureForexOnly=true` is the default. Gold, crypto, indices, shares, and
  other non-FX calculation modes are skipped.
- The filter uses the broker's MT5 symbol calculation mode, not string matching
  on symbol names. This avoids assuming that every FX symbol has the same suffix.
- The EA still scans only Market Watch. Use MT5's Symbols dialog to make the
  broker's intended FX instruments visible. The EA does not automatically
  discover or enable every broker symbol.
- If the broker classifies a desired instrument under a non-FX calculation
  mode, it will be excluded. Confirm the broker's symbol specifications before
  relying on coverage.
- Output is written to the MT5 Common Files area as
  `mt5_raw_capture_fx_v1_1.csv`. This is a new filename and does not overwrite
  the V1 capture file.

## Installation and test

1. Keep the existing V1 EA and its CSV untouched.
2. Place `MT5_Forex_Only_Raw_Capture_V1_1.mq5` in `MQL5/Experts`.
3. Compile in MetaEditor and confirm zero errors and zero warnings.
4. Attach this V1.1 EA to one Demo chart. Leave `CaptureForexOnly=true`.
5. Confirm the Experts log reports the Forex-Only V1.1 start message.
6. After several minutes, inspect `mt5_raw_capture_fx_v1_1.csv`. Confirm that
   symbols are FX instruments and that all six timeframe labels appear where
   history is available.
7. Compare the included symbol list with the broker's intended FX universe.
   Missing history or symbols must be reported, not silently inferred.

## Data and timestamp policy

The EA retains the MT5 bar timestamp and separate server/host clock observations.
It does not infer broker timezone/DST rules or apply offsets retrospectively.
The CSV schema remains compatible with the existing V1 raw-bar field contract;
the capture version is `1.2.0`.

## Explicit limitations

- MetaEditor compilation and terminal behavior must be verified by the operator.
- Broker symbol classification, Market Watch coverage, and historical completeness
  remain to be verified on the target Exness Demo terminal.
- This is not a feature producer and generates no trend regimes or MTF score.
- Do not use 2025 OOS for tuning, calibration, or feature selection.
- No merge to main and no live orders are part of this work.
