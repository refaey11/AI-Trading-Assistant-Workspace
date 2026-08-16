# Nison 0039–0044 Shared Primitive Execution Gate V1

Status: EXECUTION GATE — NO FREEZE

## Decision
Do not create new engines for Nison. Reuse existing canonical components where verified; otherwise fail closed.

## Gate mapping
- 0039 Multiple Technical Techniques: evidence aggregation only; no score/minimum-count invented.
- 0040 Candlestick Clusters: reuse zone/evidence primitives when available; cluster count/tolerance remains blocked if not canonical.
- 0041 Trend Lines: reuse canonical trendline geometry; touch/break semantics must be explicitly available before evaluation.
- 0042 Support/Resistance: reuse canonical level/zone primitives; zone width/retest tolerance cannot be invented.
- 0043 False Breakouts: reuse canonical breakout evidence only; return-inside/confirmation chain must be causal and source-compatible.
- 0044 Polarity: reuse level/break/retest evidence chain; no standalone polarity engine.

## Test requirements before closure
1. deterministic positive/negative cases for each primitive;
2. timestamp-causal ordering;
3. no-lookahead checks;
4. provenance preserved into Nison evidence;
5. Nison adapter cannot emit direction;
6. 2025 excluded from operator selection/tuning/QA.

## Current verdict
0039–0044 remain NOT_EVALUABLE until the canonical primitive implementations and tests are directly verified. This gate prevents accidental invention and duplicate engines.
