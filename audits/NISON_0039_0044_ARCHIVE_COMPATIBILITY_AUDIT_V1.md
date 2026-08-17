# Nison 0039–0044 Archive Compatibility Audit V1

Status: VERIFIED SOURCE / COMPATIBILITY PARTIAL / NO FREEZE

## Source archive verification
- 3-book integration archive: `AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip`
- SHA-256: `31ad1d22a2d9ed3c897fece30da4da5934955114302226b20177cac0a1a45509`
- Trading rules archive: `AI_Trading_Assistant_TRADING_RULES_V2.zip`
- SHA-256: `da6a7cb79d6134bd9afd19a167a647caf1bd9becb3534e49154aba298e6d2424`

## Verified Nison source roots
0039 -> `06_Multiple_Technical_Techniques/06_Multiple_Technical_Techniques`
0040 -> `06_Multiple_Technical_Techniques/13_Candlestick_Clusters:`
0041 -> `06_Multiple_Technical_Techniques/14_Trend_Lines:`
0042 -> `06_Multiple_Technical_Techniques/15_Support_Resistance:`
0043 -> `06_Multiple_Technical_Techniques/16_False_Breakouts:`
0044 -> `06_Multiple_Technical_Techniques/17_Polarity_Principle:`

## Source-derived compatibility findings

### 0040 Candlestick Clusters
Source defines a cluster as two or more bullish/bearish candlestick signals in the same price area. It explicitly says clusters identify zones, not exact prices, and require trend, previous price action, support/resistance and market context. No deterministic price-width or scoring operator is authorized by this audit.

### 0041 Trend Lines
Source requires trendline construction from important swing points, with upward lines through higher lows and downward lines through lower highs; repeated successful tests increase significance; candlestick confirmation is used around trendline tests and breaks. Existing project Murphy candidate rules MURPHY_0006/0007 describe two points as tentative and a third successful touch/reaction as confirmation, but those candidates are still INCOMPLETE_NEEDS_RULE_DEFINITION. Therefore this is compatibility evidence, not a frozen canonical evaluator.

### 0042 Support / Resistance
Source treats support/resistance as zones/areas, strengthened by repeated successful tests and candlestick confirmation. Existing MURPHY_0008/0009 are READY_FOR_BACKTEST role-reversal candidates, but remain candidate rules rather than a production-frozen horizontal-zone primitive. Nison 0042 therefore remains NOT_EVALUABLE for deterministic zone-width semantics.

### 0043 False Breakouts
Source defines false breakouts as temporary violations of significant support/resistance followed by return inside the prior range; Upthrust and Spring are explicit examples and candlestick confirmation is required. MURPHY_0010 is a READY_FOR_BACKTEST trendline-break confirmation candidate, but it does not by itself supply the full Nison false-breakout return-inside-range contract. No automatic transfer is authorized.

### 0044 Polarity Principle
Source requires a broken important support/resistance level, subsequent successful retest, and candlestick confirmation; polarity is a zone rather than an exact price. MURPHY_0008/0009 provide closely related role-reversal evidence (broken support/resistance followed by a later rally/pullback), but Nison adds explicit successful-retest and candlestick-confirmation requirements. Reuse is therefore partial and must be wrapped without semantic expansion.

### 0039 Multiple Technical Techniques
Source is a confluence/confirmation framework. It must remain evidence-only. The source's confidence model must not be converted into a Decision Brain score without a separate approved contract.

## Governance verdict
- No duplicate geometry/level/breakout engines created.
- No invented thresholds, tolerances, lookbacks, or scores.
- Nison remains confirmation/evidence only and cannot generate direction.
- 2025 remains OOS and is excluded from tuning, calibration, operator selection and optimization.
- 0039–0044 are now SOURCE-VERIFIED and COMPATIBILITY-MAPPED, but are not production-frozen.

## Next executable gate
Run deterministic tests against the actual canonical primitive artifacts once their implementation locations are verified in the workspace. Then run availability/no-lookahead checks, clause-level wrappers, and fresh 2016–2024 QA. Do not use 2025 for tuning.
