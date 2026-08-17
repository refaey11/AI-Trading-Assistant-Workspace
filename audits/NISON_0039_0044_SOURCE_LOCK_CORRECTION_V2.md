# Nison 0039–0044 Source Lock Correction V2

Date: 2026-08-17
Status: SOURCE LOCKED / NOT FROZEN

## Critical correction
CANDLE_RULE_0039–0044 are Steve Nison confirmation rules in the integrated Nison registry. They are NOT Murphy risk rules. Any earlier Murphy 0042–0044 risk-gate work must not be used as the semantic definition of these Nison rules.

The authoritative registry maps them to:
- 0039: Multiple Technical Techniques
- 0040: Candlestick Clusters
- 0041: Trend Lines
- 0042: Support / Resistance
- 0043: False Breakouts
- 0044: Polarity Principle

All six have integration_role=confirmation and direction=NEUTRAL in the source registry.

## Source-derived operational requirements

### 0039 — Multiple Technical Techniques
- use multiple confirmations / technical confluence;
- never rely on one indicator;
- candlesticks confirm Western analysis;
- support/resistance gain strength through confluence.
- No source-locked minimum count, weighting, score, or confidence formula is present; therefore this remains evidence-only rather than a numeric decision score.

### 0040 — Candlestick Clusters
- cluster = two or more bullish or bearish candlestick signals in the same price area;
- independent signals around the same level strengthen the zone;
- evaluate prior price action, current pattern, nearby support/resistance, trend, and market context;
- clusters identify zones, not exact prices;
- clusters confirm and do not replace trend analysis.
- No numeric zone width/tolerance is present; zone membership must come from an approved upstream primitive.

### 0041 — Trend Lines
- trend line uses at least two significant swing points;
- rising line connects higher lows; falling line connects lower highs;
- successful tests increase significance;
- candlestick confirmation is required at trend-line interaction;
- a broken trend line is an early warning; candlestick confirmation is required before treating the break as genuine/false.
- Existing TRENDLINE_GEOMETRY_V1 is reusable for line identity/anchors/availability; it does not by itself prove the required interaction/confirmation event.

### 0042 — Support / Resistance
- support/resistance are price areas/zones;
- bullish reversal patterns near support strengthen confirmation;
- bearish reversal patterns near resistance strengthen confirmation;
- repeated successful tests strengthen the level;
- combine with trend and context;
- confirming candle matters more than price alone.
- No numeric zone width is source-locked; do not use the earlier Murphy risk percentages.

### 0043 — False Breakouts
- significant support/resistance is temporarily broken;
- price returns inside the previous range;
- Upthrust = false breakout above resistance;
- Spring = false breakdown below support;
- Upthrust requires close back below prior resistance;
- Spring requires close back above prior support;
- candlestick confirmation is required;
- support/resistance, trend, and context remain relevant.
- The source does not supply a numeric penetration threshold or fixed 'quickly' window; these remain qualitative unless an approved compatible primitive exists.

### 0044 — Polarity Principle
- broken resistance can become future support;
- broken support can become future resistance;
- polarity is not assumed immediately after a break;
- successful retest/defense or rejection is required;
- candlestick confirmation is required at the retest;
- polarity is a zone, not an exact price;
- combine with trend.
- No retest tolerance or time window is source-locked.

## Execution architecture
Reuse existing canonical infrastructure; do not create duplicate engines:

0039 -> provenance-preserving confluence evidence
0040 -> canonical zone membership + candlestick-cluster evidence
0041 -> TRENDLINE_GEOMETRY_V1 + causal interaction + Nison candle confirmation
0042 -> canonical S/R zone/test evidence + Nison candle confirmation
0043 -> canonical level/break/return-inside-range chain + Nison candle confirmation
0044 -> canonical level/break/successful-retest chain + Nison candle confirmation

## Fail-closed rules
- Missing required upstream evidence => NOT_EVALUABLE.
- Qualitative clause without approved comparator => NOT_EVALUABLE.
- Evidence received out of causal order => FAIL/NOT_EVALUABLE; never sort events before validation.
- Nison never creates standalone direction.
- No invented threshold, tolerance, lookback, score, confidence weight, or proxy.
- 2025 remains OOS and is excluded from tuning/selection/calibration/optimization.

## Freeze status
Source semantics: PASS.
Registry mapping: PASS.
Operational contracts: defined at clause level.
Existing upstream primitive compatibility: PARTIAL and must be verified per rule.
Deterministic QA: PENDING end-to-end.
Historical QA 2016–2024: PENDING.
Production freeze: NOT FROZEN.
