# Nison 0039–0044 Source-to-Adapter QA V2

Date: 2026-08-17
Status: ADAPTER QA PASS / UPSTREAM QA PENDING / NOT FROZEN

## Source lock
The integrated Nison registry and source package resolve 0039–0044 as:
- 0039 Multiple Technical Techniques
- 0040 Candlestick Clusters
- 0041 Trend Lines
- 0042 Support / Resistance
- 0043 False Breakouts
- 0044 Polarity Principle

All six are confirmation-role Nison rules. The earlier Murphy-risk interpretation of 0042–0044 is superseded and must not be used as Nison semantics.

## Adapter implementation
The shared Nison evidence adapter was corrected so chronology is validated in the order received. It no longer sorts evidence before checking causality.

0040 now requires caller-supplied canonical zone membership and independent signals; no numeric zone tolerance or score is introduced.

0039 remains direction-neutral evidence aggregation; no minimum count or score is introduced.

0041 requires trendline event before candlestick confirmation.
0042 requires support/resistance test before candlestick confirmation.
0043 requires Upthrust/Spring -> return-inside-range -> candlestick confirmation.
0044 requires level break -> successful retest -> candlestick confirmation.

## Local deterministic QA
11/11 assertions PASS:
1. 0039 confluence remains direction-neutral.
2. 0039 out-of-order evidence is rejected without sorting.
3. 0040 same-zone cluster evidence is accepted when caller supplies canonical zone identity.
4. 0040 missing zone identity is rejected.
5. 0041 rejects confirmation before trendline event.
6. 0041 accepts causal confirmation.
7. 0042 accepts causal level-test confirmation.
8. 0043 accepts causal Spring/return/confirmation chain.
9. 0043 rejects out-of-order return/confirmation.
10. 0044 accepts break/retest/confirmation.
11. 0044 rejects failed retest and lookahead confirmation.

## What this proves
The Nison adapter layer is now source-aligned at the contract boundary and has deterministic causal tests.

## What this does NOT prove
- It does not prove the upstream canonical S/R zone producer exists.
- It does not prove a canonical breakout/return producer exists.
- It does not prove a canonical successful-retest/polarity producer exists.
- It does not prove historical QA for 2016–2024.
- It does not grant production freeze.

## Governance
- No invented threshold, tolerance, lookback, score, confidence weight, or direction generator.
- 2025 remains OOS and excluded from tuning/selection/calibration/optimization.
- Missing upstream evidence remains NOT_EVALUABLE.
