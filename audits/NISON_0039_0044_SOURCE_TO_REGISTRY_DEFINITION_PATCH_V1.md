# Nison 0039–0044 Source-to-Registry Definition Patch V1

Status: SOURCE-BACKED DEFINITION PATCH / NOT FROZEN

## Registry finding
The current TRADING_RULES_V2 master registry marks CANDLE_RULE_0039 through CANDLE_RULE_0044 as INCOMPLETE_NEEDS_RULE_DEFINITION, with testing status UNTESTED and missing confirmation fields. This patch does not overwrite that registry status.

## Source-backed clauses

### 0039 — Multiple Technical Techniques
Source: Nison 06_Multiple_Technical_Techniques/06_JSON.json and Trading Rules.
- use multiple confirmations;
- never rely on one indicator;
- candlesticks confirm Western analysis;
- support/resistance gain strength through confluence.
- role: evidence/confirmation; direction-neutral at this layer.

### 0040 — Candlestick Clusters
Source: Nison chapter 13.
- a cluster is more reliable than an isolated pattern;
- multiple independent candlestick signals in the same price area strengthen support/resistance;
- evaluate with trend, prior price action, support/resistance and market context;
- clusters identify price zones, not exact prices;
- repeated successful support/resistance tests with confirming candles increase significance.

### 0041 — Trend Lines
Source: Nison chapter 14.
- trend line types: up/down;
- historical interaction records include test, break and false-break;
- candlestick confirmation is required in the source workflow;
- the backtest record explicitly tracks trend-line respect and confirmation.
- Do not invent swing-count/tolerance/lookback beyond what the source or canonical primitive supplies.

### 0042 — Support / Resistance
Source: Nison chapter 15.
- identify major support/resistance before searching for candlestick patterns;
- bullish patterns at support and bearish patterns at resistance carry greater significance;
- multiple successful tests strengthen the zone;
- support/resistance are price zones, not exact prices;
- combine with trend;
- use confirming-candle extreme for stop placement.

### 0043 — False Breakouts
Source: Nison chapter 16.
- do not trade a breakout immediately;
- Upthrust is confirmed when price closes back below previous resistance;
- Spring is confirmed when price closes back above previous support;
- candlestick confirmation is required;
- consider support/resistance and trend;
- source explicitly records Spring/Upthrust, S/R, candlestick confirmation and whether price remained outside.

### 0044 — Polarity Principle
Source: Nison chapter 17.
- do not assume polarity changes immediately after breakout;
- wait for successful retest;
- old resistance becomes support only after successful defense of retest;
- old support becomes resistance only after successful rejection of retest;
- candlestick confirmation is required;
- polarity is a zone, not an exact price;
- combine with trend.

## Execution boundary
This patch supplies the missing source-grounded semantic clauses for the registry. It intentionally does NOT create numerical tolerances, lookbacks, zone widths, penetration thresholds, scoring, or minimum-count operators.

## Testing boundary
The existing Nison adapter layer has 7/7 local deterministic tests. These tests validate adapter behavior only. They do not validate the missing upstream canonical market-structure primitives or historical performance.

## Governance
- Nison remains evidence/confirmation only.
- 2025 is OOS and excluded from tuning, calibration, optimization and operator selection.
- Historical QA may begin only after canonical upstream primitives are verified end-to-end.
