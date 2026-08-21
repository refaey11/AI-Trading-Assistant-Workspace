# Decision Brain Recovery Audit — 2026-08-21

## Resume checkpoint
This audit resumes from the authoritative handoff checkpoint: **Decision Brain Recovery & Compatibility Audit**.

## Recovery result
The original Decision Brain implementation was recovered from Dropbox:
- `/decision_brain.py`
- `/DECISION_BRAIN_V1_SPEC.json`

The recovered implementation is a V1 evidence aggregator and explicitly describes itself as a market-state assessment component, not a trading signal generator.

## Recovered implementation inputs
### Current market evidence
- `mtf_trend_score`
- M5/M15/M30/H1/H4/D1 trend-regime inputs
- volume availability and per-timeframe volume regimes when available

### Historical evidence
The legacy implementation accepts an optional similarity payload. The legacy code expects `predicted_return` when similarity is supplied.

## Recovered outputs
- `market_state`
- `directional_bias`
- `confidence`
- evidence trace
- contradictions
- `no_trade_reasons`

The V1 spec additionally describes a future/calibrated `scenario_distribution` and human-readable explanation trace, but those are not emitted by the recovered `decision_brain.py` function as currently recovered. This is an input/output contract mismatch to be classified during compatibility work rather than silently filled.

## Historical integration state recovered
Existing project records already established:
- Run 065: similarity compatibility gate completed; similarity is optional historical evidence only.
- Run 066: separate compatibility adapter passed; legacy Decision Brain code was not overwritten.
- The adapter removes directional similarity dependency and preserves no-future-data and 2025 OOS rules.
- Run 066 next gate is Outcome Memory calibration before calibrated bull/base/bear scenario probabilities.

## Preliminary compatibility findings
### Compatible in principle
- Evidence aggregation role
- No automatic BUY/SELL execution
- Similarity as evidence, not sole authority, when using the existing compatibility adapter
- No-trade / uncertainty output path

### Requires compatibility review
1. The legacy code contains internal numeric thresholds and confidence logic. These are legacy implementation behavior and must not be promoted into new authoritative project-wide constants without governance/testing.
2. Legacy similarity input expects `predicted_return`; the newer evidence contract does not provide this directly. Use the existing separate adapter path; do not reintroduce directional similarity dependency.
3. Knowledge Alignment and Risk Boundary are newer validated boundaries and are not direct inputs in the recovered legacy function. Their real contracts must be mapped at the boundary before wiring.
4. The V1 spec lists outputs that the recovered runtime does not currently emit, including calibrated scenario distribution and explanation. Do not fabricate them.

## Current classification
**RECOVERED — AUDIT IN PROGRESS**

The Decision Brain is no longer missing. The next step is a concrete contract-by-contract compatibility audit against:
- Knowledge Alignment (validated 6/6)
- Risk Boundary (validated 8/8)
- current market/context evidence
- historical outcome memory / similarity evidence

## Governance preserved
- Murphy: technical context/market structure
- Nison: confirmation/contradiction only
- Trading in the Zone: deferred/process-only; not reopened by this audit
- Similarity: historical evidence only; never sole direction authority
- Risk: hard gate
- 2025: OOS only; never tuning/calibration/selection

## No rebuild decision
Do not rewrite `decision_brain.py` at this stage. Recover → audit → classify → adapter only if required.
