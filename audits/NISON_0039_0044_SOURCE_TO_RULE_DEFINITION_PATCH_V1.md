# Nison 0039–0044 Source-to-Rule Definition Patch V1

Status: SOURCE-GROUNDED CANDIDATE DEFINITIONS — NOT FROZEN

Purpose: convert the verified Nison source material into explicit evaluator requirements without inventing thresholds, lookbacks, scoring, or trading parameters.

## 0039 — Multiple Technical Techniques
Source-backed requirements:
- multiple confirmations / technical confluence;
- never rely on one indicator;
- candlesticks confirm Western analysis;
- support/resistance gain strength through confluence;
- output remains NEUTRAL evidence.
Evaluator contract still missing: canonical confluence aggregation semantics and any project-approved independence rule. No minimum count or score is invented here.

## 0040 — Candlestick Clusters
Source-backed requirements:
- two or more bullish or bearish candlestick signals in the same price area;
- independent signals around the same level strengthen the zone;
- clusters are zones, not exact prices;
- evaluate previous candles, current pattern, nearby support/resistance, trend and market context;
- clusters provide confirmation and do not replace trend analysis.
Evaluator contract still missing: canonical price-area/zone identity and independence handling. The source explicitly supports the two-or-more concept; no numeric price tolerance is invented.

## 0041 — Trend Lines
Source-backed requirements:
- at least two significant swing points;
- uptrend line connects rising lows;
- downtrend line connects falling highs;
- successful tests increase significance;
- candlestick confirmation is required for a trend-line reaction;
- a broken trend line is a warning; candlestick confirmation is required before treating it as genuine/false.
Evaluator contract still missing: canonical swing-point, line-touch, break and confirmation operators. No lookback/tolerance is invented.

## 0042 — Support / Resistance
Source-backed requirements:
- support/resistance are price areas/zones;
- multiple successful tests increase importance;
- bullish candlesticks strengthen support;
- bearish candlesticks strengthen resistance;
- combine with trend;
- confirming candlestick evidence matters more than price alone.
Evaluator contract still missing: canonical zone identity, successful-test/rejection semantics and confirmation linkage. No zone width is invented.

## 0043 — False Breakouts
Source-backed requirements:
- significant support/resistance is temporarily broken;
- false breakout returns inside the previous trading range;
- Upthrust = false breakout above resistance;
- Spring = false breakdown below support;
- Upthrust valid bearish signal after close back below prior resistance;
- Spring valid bullish signal after close back above prior support;
- candlestick confirmation is required;
- evaluate with support, resistance, trend and market context;
- protective stop references the extreme high/low of the setup.
Evaluator contract still missing: canonical level identity, breakout event, return-inside event and causal confirmation operators. The source uses qualitative timing/penetration language; no numerical threshold is invented.

## 0044 — Polarity Principle
Source-backed requirements:
- broken resistance can become future support;
- broken support can become future resistance;
- do not assume polarity immediately after breakout;
- require successful retest/defense or rejection;
- require candlestick confirmation at the retest;
- polarity is a zone, not an exact price;
- combine with trend.
Evaluator contract still missing: canonical level identity, break, retest success/failure and confirmation operators. No retest tolerance or time window is invented.

## Governance
- Nison remains evidence/confirmation only; no standalone direction generation.
- 2025 remains OOS and cannot be used for tuning, calibration, optimization, operator selection, or QA.
- These are candidate evaluator requirements, not production-frozen trading rules.
- Historical QA is not claimed by this document.
