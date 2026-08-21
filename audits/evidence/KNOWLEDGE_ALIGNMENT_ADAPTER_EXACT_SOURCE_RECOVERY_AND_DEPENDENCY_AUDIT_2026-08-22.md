# Knowledge Alignment Adapter — Exact Source Recovery and Dependency Audit — 2026-08-22

## Source and provenance
Exact source recovered from the canonical complete milestone backup:

`AI_TRADING_ASSISTANT_COMPLETE_MILESTONE_BACKUP_79RULE_RISK_20260821T022022Z.zip`

Internal path:
`AI_TRADING_ASSISTANT_MILESTONE_BACKUP_79RULE_RISK/local/knowledge_alignment_adapter.py`

The same canonical backup also contains:
- `KNOWLEDGE_ALIGNMENT_CONTRACT_V1.json`
- `KNOWLEDGE_ALIGNMENT_SMOKE_TEST_RUN_074.py`
- `KNOWLEDGE_ALIGNMENT_TO_RISK_ENGINE_BOUNDARY_INTEGRATION_TEST_V1.json`
- `RISK_ENGINE_SPEC_V1.json`

## Exact adapter responsibility
The recovered runtime is explicitly evidence alignment only.
It:
- normalizes direction labels;
- accepts market bundle, Murphy records, Nison records, Trading in the Zone gate, and optional similarity records;
- requires frozen Murphy evidence;
- allows only source-locked Nison pattern IDs 1–38 as authoritative pattern evidence;
- blocks on process gate FAIL;
- abstains on missing Murphy evidence;
- returns NEEDS_REVIEW when frozen Murphy records disagree;
- returns NISON_CONTRADICTION when authoritative Nison evidence directly opposes the existing Murphy direction;
- never manufactures an opposite direction from Nison;
- never emits final BUY/SELL, entry, stop, take-profit, or position size.

The recovered output includes:
- `alignment_state`
- `candidate_direction`
- `contradiction_gate`
- `process_gate`
- `book_evidence_status`
- optional `market_evidence_status`
- optional `similarity_record_count`
- `final_trade_decision: None`
- `next_layer: risk_engine_then_existing_decision_brain`

## Runtime dependencies
The adapter has no project-module imports and no external package dependencies. Its functional dependencies are input providers, not Python imports:
1. normalized market bundle;
2. existing frozen Murphy evaluator/adapter outputs;
3. existing source-locked Nison confirmation outputs;
4. existing Trading in the Zone process gate output;
5. optional historical/similarity evidence.

## Canonical smoke test evidence
The same backup contains `KNOWLEDGE_ALIGNMENT_SMOKE_TEST_RUN_074.py` covering:
- aligned evidence;
- Nison contradiction;
- unfrozen Nison evidence ignored/abstained;
- process block;
- missing Murphy evidence;
- assertion that every case leaves `final_trade_decision` as `None`.

## Recovery conclusion
The exact source content and its immediate dependency model are now recoverable with provenance. The adapter is not yet restored into the active runtime, and no integration was performed by this audit.

## Risk-runtime search inside nested backup archives
Nested ZIP archives contained in the canonical milestone backup were also scanned recursively for filenames matching Risk Engine / Risk Boundary / Position Sizing runtime patterns. No standalone executable risk runtime was located through those nested archive filenames.

This is a search result, not proof that no implementation ever existed.

## Controlled next action
Run a line-by-line field/provider compatibility audit between the recovered adapter's five functional inputs and the currently active upstream modules. In parallel, continue recovery of the Risk Boundary executable runtime from dedicated project sources.

## Governance
- No source rule was rewritten.
- No adapter behavior was changed.
- No final trade decision was added.
- No BUY/SELL/entry/SL/TP/position-size logic was created.
- 2025 remains locked OOS and was not used for tuning, calibration, threshold selection, or implementation selection.
