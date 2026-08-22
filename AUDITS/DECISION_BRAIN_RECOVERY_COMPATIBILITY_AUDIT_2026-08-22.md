# Decision Brain Recovery & Compatibility Audit — 2026-08-22

## Purpose
Audit the existing Decision Brain runtime against the already-validated project boundaries without rebuilding Murphy, Nison, Knowledge Alignment, Risk, or historical-memory components.

## Evidence reviewed
- `decision_brain.py` current main runtime.
- `audits/DECISION_BRAIN_RESUME_POINT_2026-08-21.md`.
- `AUDITS/DECISION_BRAIN_INTEGRATION_AUDIT_2026-08-22.md`.
- `governance/RULE_ADAPTER_PROVENANCE_MAPPING_V1.json`.
- MTF Architecture V2 compatibility audit.

## Current Decision Brain runtime
`decision_brain.py` exposes:
- `assess(row, similarity=None)`
- `MarketAssessment(market_state, directional_bias, confidence, evidence, contradictions, no_trade_reasons)`

The runtime currently consumes:
- `mtf_trend_score`
- M5/M15/M30/H1/H4/D1 trend-regime fields
- optional volume fields
- optional `similarity.predicted_return`

It does not currently expose native inputs for:
- Murphy rule evidence / setup validity
- Nison confirmation / contradiction evidence
- Rule Adapter normalized evidence
- Knowledge Alignment result
- Risk Boundary result
- explicit TIZ process gate
- explicit MTF W1 / role / top-down trace
- explicit Dynamic-MTF selected timeframe

## Compatibility findings

### Compatible
- Existing runtime is an evidence aggregator, not a direct BUY/SELL signal generator.
- M5→D1 trend-regime evidence is consumed.
- Contradiction and no-trade fields exist.
- Similarity is passed in as optional historical evidence.

### Integration gaps
1. **Murphy boundary gap** — no native Murphy evidence contract is accepted.
2. **Nison boundary gap** — no native confirmation/contradiction contract is accepted.
3. **Knowledge Alignment gap** — no validated 6/6 Knowledge Alignment output is accepted as a boundary input.
4. **Risk gap** — no validated 8/8 Risk Boundary output is accepted as a hard gate.
5. **MTF architecture gap** — W1/role/order/Dynamic-MTF fields are not represented directly in the current output.
6. **Historical evidence governance gap** — Similarity is allowed to contribute directional strength through `predicted_return`; this must remain subordinate evidence and must not override technical/risk gates.
7. **Decision output gap** — current `MarketAssessment` is not the complete project `DECISION_SCHEMA_V1` boundary and does not yet represent the full cross-book decision contract.

## Safety / governance result
No existing source contract is reopened.
No Nison/Murphy rule logic is duplicated.
2025 remains OOS/locked.
No new book-rule thresholds are introduced by this audit.

## Current gate result
**DECISION BRAIN E2E: BLOCKED / NOT_READY**

Reason: the recovered runtime exists, but the producer boundaries into Murphy/Nison/Knowledge Alignment/Risk have not yet been concretely wired and tested.

## Correct next engineering step
Build a narrow cross-book input adapter/compatibility boundary around the existing `decision_brain.py` rather than rewriting the engine. The adapter must consume already-authoritative outputs from:

`Market/MTF → Murphy evidence → Nison evidence → Historical evidence → Knowledge Alignment → Risk`

and must enforce:
- Nison cannot create direction alone.
- Historical memory cannot override technical or hard-risk gates.
- Risk failure yields no-trade/hard reject.
- Missing/invalid evidence fails closed.
- 2025 remains read-only OOS.

Only after that adapter has deterministic tests should the full Decision Brain E2E test be attempted.
