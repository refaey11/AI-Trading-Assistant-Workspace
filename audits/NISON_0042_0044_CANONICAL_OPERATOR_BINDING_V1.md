# Nison 0042–0044 Canonical Operator Binding V1

Date: 2026-08-17
Status: OPERATIONAL CONTRACT CLOSED / E2E PENDING

## Source archive verified
NISON_GITHUB_SOURCE_SYNC_V1 contains the canonical Nison chapters:
- 15_Support_Resistance
- 16_False_Breakouts
- 17_Polarity_Principle

## Rule 0042 — Support / Resistance
Canonical evidence:
- support/resistance is a price area/zone, not an exact price;
- identify major S/R before looking for candlestick confirmation;
- bullish confirmation at support: Hammer, Morning Star, Bullish Engulfing;
- bearish confirmation at resistance: Shooting Star, Evening Star, Bearish Engulfing, Dark Cloud Cover;
- repeated successful tests strengthen the zone.

Required upstream input:
- authoritative S/R zone evidence;
- completed candle evidence;
- canonical Nison candle confirmation;
- availability timestamp.

No zone-width, ATR, pip, percentage, or lookback is invented here.

## Rule 0043 — False Breakouts
Canonical patterns:
- Upthrust = price penetrates prior resistance, then closes back below that resistance, followed by bearish candlestick confirmation;
- Spring = price penetrates prior support, then closes back above that support, followed by bullish candlestick confirmation.

Bearish confirmations: Shooting Star, Bearish Engulfing, Hanging Man.
Bullish confirmations: Hammer, Bullish Engulfing, Morning Star.

Required upstream input:
- authoritative prior support/resistance boundary/zone;
- penetration event;
- return/close back inside the broken boundary;
- canonical Nison confirmation candle;
- availability timestamp.

No penetration-distance threshold is invented. No fixed lookback is invented.

## Rule 0044 — Polarity Principle
Canonical evidence:
- old resistance becomes support only after buyers successfully defend a retest;
- old support becomes resistance only after sellers successfully reject a retest;
- bullish confirmations: Hammer, Morning Star, Bullish Engulfing;
- bearish confirmations: Shooting Star, Evening Star, Bearish Engulfing, Dark Cloud Cover;
- polarity is a zone, not an exact price;
- multiple historical reactions increase confidence.

Required upstream input:
- prior S/R zone;
- confirmed break of that zone;
- successful retest/rejection evidence;
- canonical Nison confirmation candle;
- availability timestamp.

No arbitrary retest tolerance, zone width, lookback, or number-of-tests threshold is invented.

## Shared governance
- Nison remains confirmation/evidence only and cannot create direction independently.
- Existing upstream producers must be reused; no duplicate S/R/breakout/retest engine is created here.
- Missing upstream evidence => NOT_EVALUABLE, never PASS.
- Chronology and availability must be preserved.
- 2025 remains OOS and is excluded from tuning/operator selection.

## Current integration result
Source binding = PASS.
Operator contract = PASS.
Canonical Nison confirmation mapping = PASS.
Runtime upstream producer binding = PENDING.
Historical E2E 2016–2024 = PENDING.
Production freeze = NOT YET.
