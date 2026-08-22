# Decision Brain Integration Compatibility Audit — 2026-08-22

## Result
Status: SOURCE_RECOVERED_PENDING_ADAPTER
Primary classification: ADAPTER_REQUIRED
Known conflicts: SIMILARITY_INPUT, MISSING_SECURITY_GATES, SPEC_IMPLEMENTATION_GAPS

## Recovered authoritative candidate source
Recovered from Dropbox project source:
- `/decision_brain.py`
- `/DECISION_BRAIN_V1_SPEC.json`

A provenance mirror was added to GitHub under:
- `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`
- `RECOVERED_SOURCES/DECISION_BRAIN_V1/DECISION_BRAIN_V1_SPEC.json`

The original Dropbox source files were not modified.

## What the recovered V1 actually is
The source docstring defines V1 as an evidence aggregator that produces a market-state assessment, not an automatic trading signal generator. Its output is `MarketAssessment` with market_state, directional_bias, confidence, evidence, contradictions, and no_trade_reasons.

This is therefore a recoverable Decision Brain V1 assessment layer, but not yet the final integrated Decision Brain runtime.

## Source vs implementation compatibility
### Market structure / MTF
Classification: COMPATIBLE at V1 assessment level.
- Code consumes M5/M15/M30/H1/H4/D1 trend regime values and `mtf_trend_score`.
- V1 spec also defines MTF context and market-structure modules.

### Volatility
Classification: MISSING_IMPLEMENTATION.
- V1 spec defines volatility inputs and `volatility_state`.
- Recovered `decision_brain.py` does not currently consume the volatility regime fields.

### Volume
Classification: ADAPTER_REQUIRED / SEMANTIC_GAP.
- Spec says volume is active only when `volume_available=true`.
- Code follows the availability flag, which is good.
- Code currently adds a no-trade reason whenever volume is unavailable. The spec only states unavailable is not equivalent to zero; it does not define volume-unavailable as an unconditional no-trade gate. This must not be silently promoted to a hard execution rule.

### Historical / Similarity Memory
Classification: CONFLICT / ADAPTER_REQUIRED.
- Recovered code accepts `similarity["predicted_return"]` and converts its sign into bullish/bearish evidence.
- Current project Memory Evidence Package explicitly forbids predicted return from being used as direction.
- Current Run 070 wrapper calls the legacy Decision Brain with `similarity=None` and records that similarity cannot change direction.
- Required fix: boundary adapter must pass historical evidence metadata only (retrieval status, distances, evidence ids/time range, outcome evidence), never `predicted_return` as directional input.

### Knowledge
Classification: MISSING_IMPLEMENTATION.
- V1 spec defines a knowledge module that provides contextual explanations and must not invent market data.
- Recovered code does not consume a knowledge/alignment output.

### Risk
Classification: MISSING_INTEGRATION.
- V1 spec defines risk_context and says no automatic execution in V1.
- Recovered code has no Risk Engine input or hard-gate handling.
- Current project Risk source is still research-only / not execution-ready; its research parameters must not be promoted to production constants.

### Nison
Classification: ADAPTER_REQUIRED.
- V1 source does not consume a Nison confirmation/contradiction object.
- Existing project contract requires Nison to confirm or contradict only, never generate direction alone.
- Nison handoff input/output must be added through a small adapter rather than modifying Nison semantics.

### Trading in the Zone
Classification: ADAPTER_REQUIRED / MISSING_AUTHORITATIVE_PRODUCER.
- V1 source does not consume TIZ process-gate outputs.
- Current TIZ producer search says no authoritative producer exists; candidate producers are not authoritative.
- Therefore a production TIZ gate cannot be fabricated during this integration.

### Provenance / anti-leakage
Classification: MISSING_IMPLEMENTATION.
- V1 spec requires no future data, 2025 excluded from calibration, and every conclusion citing evidence modules.
- Recovered code has no explicit timestamp guard, 2025 OOS guard, or source-provenance references in the returned assessment.
- These controls belong in the integration boundary and must be tested before runtime promotion.

### Confidence
Classification: SPEC/IMPLEMENTATION MISMATCH.
- Spec says confidence is calibrated, not a raw indicator score.
- Recovered code computes a direct bullish-vs-bearish gap and uses a V1 threshold of 0.25.
- No calibration contract was recovered in this audit. Do not tune or replace the threshold from 2025 or invent a new calibration method.

### Scenario distribution / explanation
Classification: MISSING_IMPLEMENTATION.
- Spec declares `scenario_distribution` and `explanation` outputs.
- Recovered code does not return them.

## Governance-compatible architecture to preserve
- Murphy = technical context / market structure evidence.
- Nison = confirmation / contradiction only.
- TIZ = psychology / process gate only.
- Historical / Similarity Memory = evidence only and never sole decision maker.
- Risk = hard gate when an authoritative Risk runtime contract exists.
- Decision Brain = synthesis / assessment layer.
- `ABSTAIN` / `NO_TRADE` remains valid.
- 2025 = OOS and cannot be used for tuning, calibration, optimization, or implementation selection.

## Required next adapter scope
Create the smallest integration boundary around the recovered V1 source that:
1. Validates timestamp / availability and blocks future data.
2. Enforces the 2025 development OOS lock.
3. Converts current Market Reader / Market State / Scenario outputs into the V1 row fields without inventing semantics.
4. Adapts Murphy evidence into attributed evidence objects.
5. Adapts Nison as confirmation/contradiction only.
6. Attaches TIZ/process evidence only when an authoritative producer is actually available; otherwise fail closed / `NOT_EVALUABLE`.
7. Attaches Risk as a hard gate only when authoritative Risk evidence is available; otherwise `NOT_EVALUABLE` for execution.
8. Passes historical evidence metadata without predicted-return direction leakage.
9. Preserves source module/rule provenance in every conclusion.
10. Leaves the recovered V1 source unchanged.

## Explicit non-actions
- Do not edit `decision_brain.py` directly.
- Do not create new Brain thresholds from 2025.
- Do not use Similarity predicted return as directional input.
- Do not fabricate TIZ producer semantics.
- Do not promote Risk research parameters to live execution constants.
- Do not claim the final Decision Brain is runtime-verified yet.
