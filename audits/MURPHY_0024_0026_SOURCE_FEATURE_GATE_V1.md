# Murphy 0024–0026 Source / Feature Gate V1

Date: 2026-08-12

## Authoritative rule records recovered

The uploaded `TRADING_RULES_V2/MASTER_TRADING_RULES_V2.json` contains the exact registry records for all three rules.

### MURPHY_0024
- Chapter 9, Moving Average Rules.
- Setup: `Moving-average trend filter`.
- Source condition: use a moving average to smooth price fluctuations and identify the underlying trend.
- Decision: moving averages are trend-following tools, not standalone certainty signals.
- Status in registry: `INCOMPLETE_NEEDS_RULE_DEFINITION`.
- Missing field: confirmation.
- No MA period, exact price relation, crossover rule, timeframe role, or standalone entry trigger is defined in the authoritative rule record.

### MURPHY_0025
- Chapter 9, 4-Week Rule.
- Setup: `Four-week breakout`.
- Condition: price reaches a new four-week high.
- Confirmation: the four-week high acts as a buy / short-covering signal.
- Direction: BULLISH.
- Status in registry: `READY_FOR_BACKTEST`.
- No additional threshold is needed beyond the documented four-week period.

### MURPHY_0026
- Chapter 9, 4-Week Rule.
- Setup: `Four-week breakdown`.
- Condition: price reaches a new four-week low.
- Confirmation: the four-week low acts as a sell / short-entry signal.
- Direction: BEARISH.
- Status in registry: `READY_FOR_BACKTEST`.
- No additional threshold is needed beyond the documented four-week period.

## Source-material compatibility

The preserved John Murphy Chapter 9 source states:
- a moving average smooths price data and is trend-following rather than predictive;
- a single-MA buy signal is a close breaking/closing above the MA, and a sell signal is a close breaking/falling below it;
- the four-week rule is a new 4-week high for buy/short-covering and a new 4-week low for sell/short entry;
- four weeks corresponds to 20 trading days in the supplied project source.

## Gate decisions

### 0024
**Source semantics: PARTIALLY RESOLVED.**
The project source supports MA trend filtering but the rule record intentionally omits confirmation and exact operator parameters. Therefore it remains `INCOMPLETE_NEEDS_RULE_DEFINITION` and must not receive an invented MA period, timeframe, crossover, or filter threshold.

### 0025
**Source semantics: RESOLVED.**
The exact operator is the documented new four-week high. Existing Four-Week Lookback infrastructure should be reused. This moves the rule from a generic `NOT_YET_EVALUABLE` queue to **SOURCE / FEATURE COMPATIBLE — EVALUATOR / TEST / HISTORICAL QA PENDING**.

### 0026
**Source semantics: RESOLVED.**
The exact operator is the documented new four-week low. Existing Four-Week Lookback infrastructure should be reused. This moves the rule to **SOURCE / FEATURE COMPATIBLE — EVALUATOR / TEST / HISTORICAL QA PENDING**.

## Controls

- No new threshold or proxy is introduced.
- No new fixed timeframe is invented.
- Existing Four-Week Lookback is reused; do not rebuild it.
- 2025 remains OOS and is not used for tuning or implementation selection.
- Existing Moving Average infrastructure is reused where compatible; 0024 remains blocked on its missing source-defined confirmation/operator fields.

## Next action

Build/validate evaluators for 0025 and 0026 using the existing Four-Week Lookback contract, then unit test and run 2016–2024 historical QA. Keep 0024 blocked until its missing confirmation/operator contract is recovered from authoritative project source.