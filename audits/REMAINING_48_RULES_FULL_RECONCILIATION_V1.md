# Remaining 48 Rules — Full Source Reconciliation V1

Date: 2026-08-12

## Purpose

This artifact processes all 48 rules that remained unprocessed after the Murphy pass and the three previously processed Nison rules. It is source-grounded in the integrated 102-rule registry. It does NOT claim all 48 are tested or frozen; it records exact registry content, missing fields, and the correct next closure action.

## Count

- Steve Nison remaining: 41
- Trading in the Zone remaining: 7
- Total: 48

## Rule closure policy

Every rule follows:
Source/registry → mapping → existing feature compatibility → Dynamic MTF where applicable → exact operator/logic → existing evaluator → unit tests → historical/provenance QA → freeze.

`READY_FOR_BACKTEST` is not a test pass and not a freeze. Rules marked `INCOMPLETE_NEEDS_RULE_DEFINITION` must have their missing fields completed from the project source before evaluation. No invented operators, thresholds, timeframes, confirmation logic, or invalidation rules are allowed.

## Steve Nison — 41 remaining

| Rule | Setup | Registry status | Missing fields | Next closure action |
|---|---|---|---|---|
| CANDLE_RULE_0001 | Bullish Engulfing | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0002 | Bearish Engulfing | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0003 | Dark Cloud Cover | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0004 | Piercing Pattern | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0005 | On Neck | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0006 | In Neck | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0007 | Thrusting | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0008 | Morning Star | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0009 | Evening Star | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0010 | Morning Doji Star | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0011 | Evening Doji Star | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0012 | Abandoned Baby | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0013 | Harami | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0014 | Harami Cross | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0015 | Tweezers Top | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0016 | Tweezers Bottom | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0017 | Upside Gap Two Crows | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0018 | Three Black Crows | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; invalidation_rule | Source completion |
| CANDLE_RULE_0019 | Bullish Counterattack Lines | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0020 | Bearish Counterattack Lines | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0021 | Three Mountains | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0022 | Three Rivers | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0023 | Three Buddha Tops | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0024 | Three Buddha Bottoms | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0025 | Dumpling Top | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0027 | Tower Top | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0028 | Tower Bottom | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0029 | Unique Three River Bottom | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0032 | Three White Soldiers | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0033 | Advance Block (Stalled Pattern) | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0034 | Separating Lines | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0035 | Tasuki Gap | READY_FOR_BACKTEST | none | Locate/reuse evaluator; unit + historical QA |
| CANDLE_RULE_0036 | Gapping Play | READY_FOR_BACKTEST | none | Locate/reuse evaluator; unit + historical QA |
| CANDLE_RULE_0037 | Side-by-Side White Lines | READY_FOR_BACKTEST | none | Locate/reuse evaluator; unit + historical QA |
| CANDLE_RULE_0038 | Windows | READY_FOR_BACKTEST | none | Locate/reuse evaluator; unit + historical QA |
| CANDLE_RULE_0039 | 06_Multiple_Technical_Techniques | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0040 | 13_Candlestick_Clusters: | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0041 | 14_Trend_Lines: | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0042 | 15_Support_Resistance: | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0043 | 16_False_Breakouts: | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |
| CANDLE_RULE_0044 | 17_Polarity_Principle: | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation | Source completion |

## Trading in the Zone — 7 remaining

| Rule | Setup | Registry status | Missing fields | Role / next closure action |
|---|---|---|---|---|
| PSY_0001 | PREDEFINE_RISK | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; entry_rule | Process-gate definition; no direction generation |
| PSY_0002 | ACCEPT_RISK | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; entry_rule | Process-gate definition; no direction generation |
| PSY_0003 | INDEPENDENT_OUTCOMES | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; entry_rule | Process-gate definition; no direction generation |
| PSY_0004 | NO_CERTAINTY | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; entry_rule | Process-gate definition; no direction generation |
| PSY_0005 | CUT_LOSS_RULE | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; entry_rule | Process-gate definition; no direction generation |
| PSY_0006 | SYSTEMATIC_PROFIT | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; entry_rule | Process-gate definition; no direction generation |
| PSY_0007 | RULE_DISCIPLINE | INCOMPLETE_NEEDS_RULE_DEFINITION | confirmation; entry_rule | Process-gate definition; no direction generation |

## Important source-grounded details for Zone rules

The integrated registry already contains the following decision logic:
- PSY_0001: risk must be predefined before entry; edge does not imply certainty.
- PSY_0002: a valid setup may still lose; predefined risk must be accepted before entry.
- PSY_0003: treat individual trade outcomes as independent; evaluate the edge over a meaningful sample.
- PSY_0004: never turn a probabilistic edge into certainty; allow NO_TRADE.
- PSY_0005: when predefined invalidation is reached, exit without changing the rule because of emotional discomfort.
- PSY_0006: profit-taking must follow a predefined method rather than improvised behavior.
- PSY_0007: do not violate tested rules because of fear, FOMO, revenge, or recent loss.

These remain process/psychology gates and cannot create directional trade signals.

## Nison architectural control

All Nison rules remain `integration_role = confirmation`. Nison may confirm or contradict a directional setup, but cannot create direction alone. The Rule Adapter and Master Handoff explicitly enforce this precedence.

## Final status of this full batch

**All 48 remaining rules are now processed into the Master Rule Closure Queue.**

This is a full source/registry reconciliation, not a claim that the 48 are all test-passed. The next implementation work is split:
1. 4 Nison `READY_FOR_BACKTEST` rules (0035–0038): evaluator/test QA first.
2. 37 Nison incomplete rules: complete missing confirmation/invalidation fields from the authoritative Nison source artifacts, then build/use evaluator only where the project already has compatible infrastructure.
3. 7 Zone rules: complete process-gate confirmation/entry-contract fields without ever generating direction.

## Global controls

- Do not rebuild Decision Brain V1/V1.1.
- Do not copy/rewrite the 102 registry rules into the Brain.
- Do not let Similarity be the sole decision maker.
- Do not let Nison create direction alone.
- Do not let Trading in the Zone generate direction.
- 2025 remains OOS and must not be used for tuning, threshold selection, feature optimization, model selection, or rule optimization.
- Do not invent thresholds/operators/timeframes. Reuse existing components after compatibility audit.
