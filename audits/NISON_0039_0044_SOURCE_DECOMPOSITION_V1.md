# Nison 0039–0044 Source Decomposition V1

Status: SOURCE-DECOMPOSED / NOT FROZEN / NOT BACKTEST-READY

## Source basis
The integrated project package contains the Nison source material for Multiple Technical Techniques chapters/topics 06, 13, 14, 15, 16 and 17. The rule registry maps CANDLE_RULE_0039–0044 to these source roots. This document records only source-supported semantics and does not invent deterministic thresholds or operators.

## 0039 — Multiple Technical Techniques
Registry source: 06_Multiple_Technical_Techniques.
Source-supported concept: use multiple confirmations / technical confluence; do not rely on one indicator; candlesticks confirm Western analysis; support and resistance gain strength through confluence. Role: confirmation/evidence, direction NEUTRAL.
Gate: NOT_EVALUABLE until the project defines an explicit, source-compatible confluence contract without inventing a score, minimum-count threshold, or weighting.

## 0040 — Candlestick Clusters
Registry source: 13_Candlestick_Clusters.
Source-supported semantics: two or more bullish or bearish candlestick signals in the same price area; multiple independent signals around the same level strengthen the importance of the zone; clusters must be evaluated with previous candles, current pattern, nearby support/resistance, trend and market context; clusters identify zones rather than exact prices; clusters provide confirmation and do not replace trend analysis.
Gate: NOT_EVALUABLE until zone/confluence primitives and pattern-independence semantics are explicitly contracted. No invented count, price tolerance, or score.

## 0041 — Trend Lines
Registry source: 14_Trend_Lines.
Source-supported semantics: at least two important swing points; upward line connects higher lows; downward line connects lower highs; repeated successful tests increase significance; candlestick patterns confirm trend-line tests; a broken trend line is a warning and candlestick confirmation is required before treating the break as genuine/false.
Gate: NOT_EVALUABLE until the project supplies canonical swing-point, line-touch, break, and confirmation operators. No invented swing tolerance or lookback.

## 0042 — Support / Resistance
Registry source: 15_Support_Resistance.
Source-supported semantics: support/resistance are price areas; bullish reversal patterns near support and bearish reversal patterns near resistance increase confirmation; repeated successful tests strengthen the level; levels must be treated as zones rather than exact prices; combine with trend and context.
Gate: NOT_EVALUABLE until canonical zone construction and retest/rejection operators are available. No invented zone width/tolerance.

## 0043 — False Breakouts
Registry source: 16_False_Breakouts.
Source-supported semantics: false breakout temporarily breaks a significant support/resistance level and returns inside the prior range; Upthrust is false breakout above resistance; Spring is false breakdown below support; confirmation is required; Upthrust requires close back below prior resistance; Spring requires close back above prior support; context, support/resistance and trend are required; protective stop references the extreme high/low.
Gate: NOT_EVALUABLE until canonical level, breakout penetration, return-inside-range, close-confirmation and context operators are available. No invented 'quickly', penetration, or range lookback thresholds.

## 0044 — Polarity Principle
Registry source: 17_Polarity_Principle.
Source-supported semantics: broken resistance can become future support; broken support can become future resistance; important original levels and repeated tests increase significance; wait for successful retest and candlestick confirmation; polarity is a zone, not an exact price; combine with trend.
Gate: NOT_EVALUABLE until canonical break, retest, zone and confirmation operators are available. No invented retest tolerance, time window, or scoring.

## Governance
- Nison remains confirmation/evidence only and cannot generate standalone direction.
- No invented thresholds, tolerances, lookbacks, scoring, or operator selection.
- 2025 remains OOS and must not be used for tuning, calibration, optimization, or operator selection.
- Unsupported clauses remain NOT_EVALUABLE/BLOCKED.
- No freeze or historical QA claim is made by this document.

## Batch verdict
0039–0044 are now source-decomposed from the integrated project material. They are not production-ready evaluators yet. The next gate is compatibility mapping to existing canonical primitives, followed by tests and no-lookahead validation; only then can 2016–2024 historical QA be considered.
