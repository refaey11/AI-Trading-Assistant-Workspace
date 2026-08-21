# Knowledge Alignment Adapter → Active Decision Brain Compatibility Audit — 2026-08-21

## Provenance
Canonical adapter recovered from the complete milestone backup:

`AI_TRADING_ASSISTANT_MILESTONE_BACKUP_79RULE_RISK/local/knowledge_alignment_adapter.py`

Recovered adapter identity:
- RUN 074 — Knowledge Alignment Adapter
- purpose stated in source: evidence alignment only; no source-rule duplication; no final trade decision.

The exact recovered implementation was found consistently in multiple copies of the complete milestone backup.

## Recovered adapter contract
Input groups:
1. `market_bundle`
2. `murphy_records`
3. `nison_records`
4. `zone_gate`
5. optional `similarity_records`

Primary outputs:
- `alignment_state`
- `candidate_direction`
- `contradiction_gate`
- `process_gate`
- `book_evidence_status`
- `final_trade_decision: None`
- `next_layer: risk_engine_then_existing_decision_brain`

Possible alignment states include:
- PROCESS_BLOCKED
- INSUFFICIENT_BOOK_EVIDENCE
- NEEDS_REVIEW
- NISON_CONTRADICTION
- ALIGNED
- MURPHY_ONLY

## Active Decision Brain contract
Active `decision_brain.py` exposes `assess(row, similarity=None)` and returns `MarketAssessment` with:
- `market_state`
- `directional_bias`
- `confidence`
- `evidence`
- `contradictions`
- `no_trade_reasons`

Its source explicitly states that V1 is an evidence aggregator and not a trading signal generator.

## Compatibility findings

### 1. Responsibility boundary
COMPATIBLE.

The recovered adapter does not create a final trade decision and the active Brain does not generate a trading signal. Restoring the adapter as a separate upstream governance/alignment layer preserves both boundaries.

### 2. Direction semantics
PARTIALLY COMPATIBLE / EXPLICIT MAPPING REQUIRED.

The recovered adapter can emit `candidate_direction` as bullish, bearish, or none. The active Brain can emit `directional_bias` as bullish, bearish, neutral, or conflicted. These are related but not identical concepts and must not be silently equated.

### 3. Process and contradiction governance
SEPARATE INPUTS REQUIRED.

The active Brain does not consume or output `process_gate`, `alignment_state`, or `contradiction_gate`. The recovered adapter owns those governance fields. They must remain explicit in the handoff envelope rather than being synthesized inside `decision_brain.py`.

### 4. Similarity memory
COMPATIBLE AS NON-DIRECTIONAL EVIDENCE.

Both contracts accept similarity-related information, but the recovered adapter counts supplied similarity records while the active Brain uses similarity as evidence. No rule authorizes similarity to become the sole decision maker.

### 5. Market context
ADAPTER EXPECTS STRUCTURED BUNDLE; ACTIVE BRAIN EXPECTS ROW FEATURES.

A small compatibility layer may be required to preserve both input shapes. This is a data-shape concern, not authorization to add directional logic.

## Critical sequencing observation
The recovered adapter literally labels its next layer as `risk_engine_then_existing_decision_brain`. The active architecture must therefore be verified against this recovered sequencing before any runtime restoration claims are made. This audit does not silently reorder the recovered pipeline.

## Conclusion
STATUS: COMPATIBLE IN RESPONSIBILITY BOUNDARY, NOT DROP-IN COMPATIBLE AS A SINGLE FUNCTION CALL.

Required before restoration/integration:
1. preserve recovered adapter source unchanged as canonical provenance;
2. define an explicit handoff envelope for adapter outputs and active Brain inputs;
3. verify the recovered `risk_engine_then_existing_decision_brain` sequencing against the canonical boundary tests;
4. do not synthesize stop, ATR, take-profit, risk-budget, or candidate-availability fields inside the Brain;
5. only then execute the recovered 8-case boundary contract against the active chain.

## No unauthorized changes
- No adapter code added to the active runtime.
- No Decision Brain rule changed.
- No Risk Engine rule changed.
- No candidate generator created.
- 2025 remains locked Out-of-Sample and was not used for tuning.
