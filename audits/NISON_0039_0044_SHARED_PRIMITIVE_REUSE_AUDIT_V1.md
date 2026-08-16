# Nison 0039–0044 Shared Primitive Reuse Audit V1

Status: COMPATIBILITY AUDIT — IMPLEMENTATION GATE OPEN, NOT FROZEN

## Source-of-truth decision
Do not create a new Nison geometry/level engine. Reuse existing project primitives where their contracts are source-compatible, and keep unresolved semantics NOT_EVALUABLE.

## Reuse map

### 0039 Multiple Technical Techniques
Use existing evidence/adapter layer only. Confluence is an aggregation of independently sourced evidence; no new scoring engine. If confluence cannot be represented without a new threshold/count, return NOT_EVALUABLE.

### 0040 Candlestick Clusters
Reuse existing support/resistance/zone identity and Nison evidence adapter where compatible. Cluster membership remains evidence aggregation; no invented price-width, minimum-count, or score.

### 0041 Trend Lines
Reuse canonical TRENDLINE_GEOMETRY_V1 for line identity, anchors, direction, slope, and availability. Do not rebuild trendline geometry. Touch/break confirmation remains an upper-layer contract and cannot be inferred from geometry alone.

### 0042 Support / Resistance
Reuse existing pivot/support-resistance identity where compatible. The existing project explicitly requires a horizontal-level contract before assigning a numeric tolerance; therefore unresolved zone-width semantics remain NOT_EVALUABLE.

### 0043 False Breakouts
Reuse existing breakout evidence contract only if its decisive-break and return-inside semantics are already approved. The existing PF-B1 material is a proposal, not production-frozen; therefore 0043 remains NOT_EVALUABLE for canonical evaluation until PF-B1 is approved.

### 0044 Polarity Principle
Reuse the same level/break/retest evidence chain as 0043. No duplicate polarity engine. Broken-level role reversal is evidence only until the level-break/retest/confirmation contract is closed.

## Canonicality / no-rebuild rule
- PIVOT_SEQUENCE_V2 and TRENDLINE_GEOMETRY_V1 are protected shared components.
- Nison adapter normalizes evidence and does not decide direction.
- No new duplicate geometry, breakout, or scoring engine is authorized by this audit.

## Required next implementation gate
1. Verify exact existing primitive artifact and version.
2. Verify its deterministic test suite.
3. Verify availability/no-lookahead behavior.
4. Map Nison clause-by-clause without semantic expansion.
5. Only then implement rule evaluator wrappers.
6. Run fresh 2016–2024 QA; keep 2025 OOS.

## Verdict
The correct solution is controlled reuse, not rebuilding. 0039–0044 are structurally mapped to shared primitives, but 0041/0042 are only partially consumable and 0043/0044 remain blocked by the unfrozen breakout/retest contract. 0039/0040 remain blocked where confluence/cluster requires an unapproved count, score, or tolerance.
