# Gate 2 — Real Decision Replay

## Purpose
Run the integrated GBPUSD decision path chronologically on real project artifacts, producing one canonical event per evaluated timestamp and preserving existing semantics.

## Input artifacts
- MARKET_STATE_READER_V1
- MULTI_TIMEFRAME_READER_V1
- NISON_CANDLE_CONFIRMATION_V1
- HISTORICAL_OUTCOME_MEMORY_V1
- Existing Decision Brain / Three-Book contracts remain authoritative for decision semantics.

## Current Gate 1 result
- 401 integrated GBPUSD events produced for 2016 artifact replay.
- 120 EXECUTABLE, 56 CANDIDATE, 225 NO_TRADE.
- BUY: 70; SELL: 106.
- Evidence aligned to the event timestamp.

## Gate 2 acceptance criteria
1. Chronological ordering is deterministic.
2. One event identity per timestamp/setup.
3. No future-data access.
4. Existing book-rule semantics unchanged.
5. 2025 remains OOS and is not tuned.
6. Risk/trade-plan output is explicit for every executable event.
7. Replay artifacts are reproducible and recorded.

## Next action
Run the full chronological replay over the available GBPUSD development window, then summarize executable-trade performance using the frozen candidate execution assumptions without changing them.
