# MT5 Raw Capture Only V1

## Purpose and safety boundary

This Expert Advisor exports the latest **closed** bars for the six approved source timeframes:
M5, M15, M30, H1, H4, and D1. It scans symbols currently visible in Market Watch.

It is data-capture only. It contains no trade request functions, no position management,
no indicators, no feature formulas, no BUY/SELL logic, and no risk sizing.

## Time policy — intentionally unresolved

- `bar_time_server` is copied from the MT5 bar timestamp and written as raw server-clock text.
- `terminal_time_server`, `terminal_gmt_observed_utc`, and
  `terminal_local_time_observed` are clock observations made during capture.
- `observed_server_minus_gmt_seconds` is only a contemporaneous observed difference.
  It is not a historical timezone rule and must not be applied retrospectively.
- The EA does not convert historical bar times to UTC and does not claim that the
  broker's timezone or DST policy has been identified.
- The UTC-labelled capture observation relies on the terminal host's GMT clock being
  correctly configured. Preserve the raw server clock even if this observation is suspect.

## Installation

1. In MT5, open **File → Open Data Folder**.
2. Open `MQL5/Experts` and place `MT5_Raw_Capture_Only_V1.mq5` there.
3. Open MetaEditor, compile the file, and attach the EA to one chart.
4. Enable the symbols you want captured in Market Watch. The EA scans Market Watch,
   not every symbol offered by the broker.
5. Keep the terminal connected and allow history to load for all six timeframes.
6. The output is written to the MT5 Common Files area as
   `mt5_raw_capture_v1.csv`. The EA appends a row only when a new closed bar is seen
   for a symbol/timeframe pair. A restart can replay the latest closed bar; downstream
   ingestion must remain idempotent.

## Validation before feature production

- Verify the broker server identity and symbol naming/suffixes.
- Compare raw bar times against the MT5 chart for each timeframe.
- Check that all six timeframe streams appear for every intended FX pair.
- Check gaps, duplicate rows, volume availability, spread, and OHLC geometry.
- Observe server/GMT differences across time and DST transitions; do not infer a
  timezone until the evidence supports a documented policy.
- Keep 2025 OOS sealed. Do not tune, calibrate, or validate formulas on 2025.
- Do not derive `trend_regime` or `mtf_trend_score` until their original semantics
  are recovered or a separately approved, versioned replacement contract exists.

## Current limitation

This EA source is committed for review; it has not been compiled in MetaEditor or run
against a live MT5 terminal in this environment. It does not prove broker connectivity,
history completeness, or timezone correctness.
