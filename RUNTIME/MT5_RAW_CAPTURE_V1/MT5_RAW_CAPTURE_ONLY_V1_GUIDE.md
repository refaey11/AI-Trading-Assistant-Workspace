# MT5 Raw Capture Only V1

## Purpose and safety boundary

This Expert Advisor exports the latest **closed** bars for six timeframes:
M5, M15, M30, H1, H4, and D1. It scans symbols currently visible in Market Watch.

It is data-capture only. It contains no trade request functions, no position management,
no indicators, no feature formulas, no BUY/SELL logic, and no risk sizing.

## Timestamp provenance

- `bar_time_mt5_utc` is the UTC timestamp returned by the MT5 `MqlRates.time`
  field. The MT5 Python integration documentation states that terminal bar/tick
  timestamps are stored in UTC. This field is not a broker-server wall-clock string.
- `terminal_time_server` is `TimeTradeServer()`, an estimated current server time
  calculated by the client terminal and dependent on the computer's time settings.
- `terminal_time_current_server` is `TimeCurrent()`, the last known server quote time.
- `host_gmt_estimate_utc` is `TimeGMT()`, calculated using the local computer's
  clock and timezone settings. It is an observation, not an independently verified
  UTC clock.
- `host_local_time_observed` is `TimeLocal()`.
- `observed_server_minus_host_gmt_seconds` is a contemporaneous diagnostic only.
  It is not a historical timezone/DST rule and must never be applied retrospectively.

The EA does not convert bar timestamps to a broker timezone or infer the broker's
historical timezone/DST policy. Keep the original MT5 UTC bar timestamp and the
separate clock observations.

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

- Verify broker server identity and symbol naming/suffixes.
- Compare UTC bar times against the MT5 terminal/history for each timeframe.
- Check that all six timeframe streams appear for every intended FX pair.
- Check gaps, duplicate rows, volume availability, spread, and OHLC geometry.
- Verify the host computer clock is synchronized. Treat TimeGMT as a host-derived
  estimate until independently checked.
- Observe server/GMT differences over time and across DST transitions; do not infer
  a timezone until the evidence supports a documented policy.
- Keep 2025 OOS sealed. Do not tune, calibrate, or validate formulas on 2025.
- Do not derive `trend_regime` or `mtf_trend_score` until their original semantics
  are recovered or a separately approved, versioned replacement contract exists.

## Current limitation

This EA source is committed for review; it has not been compiled in MetaEditor or run
against an MT5 terminal in this environment. It does not prove broker connectivity,
history completeness, symbol coverage, host clock accuracy, or timezone correctness.
