# MURPHY 0006/0007 — DISCOVERY LOG V1

Purpose: append-only record of material discoveries, corrections, decisions, and evidence so the project does not repeat investigations or rely on conversation memory.

## Entry 001 — D1 lineage verification
Date: 2026-08-14
Finding: The existing machine-readable fresh replay claim is supported. Calendar-date aggregation of `GBPUSD_M1_MASTER_2016_2026_V1.zip` reproduces `d1_ref.csv` exactly across 2,544 common 2016–2024 dates.
Evidence: `MURPHY_0006_0007_D1_LINEAGE_RECONCILIATION_V1.md`.
Result: D1/M1 lineage gate CLOSED/PASS for the available artifacts.

## Entry 002 — Invalid blocker corrected
Date: 2026-08-14
Finding: The earlier blocker compared Pivot V2 event price 1.43519 with D1 low 1.40792. This was a category error because a pivot event price is not the D1 bar low.
Evidence: superseded `MURPHY_0006_0007_CANONICAL_INPUT_REPLAY_BLOCKER_V1.md`.
Result: The blocker is explicitly marked SUPERSEDED.

## Entry 003 — Fresh replay evidence preserved
Date: 2026-08-14
Finding: `murphy_0006_0007_FRESH_REPLAY_2016_2024_V1.json` records `FRESH_REPLAY_PASS`, canonical Pivot V2 and Geometry V1 reuse, 2016–2024 scope, 2025 excluded, 0006=8, 0007=7, total=15, and no-lookahead/availability checks.
Result: Replay result is evidence, but production freeze remains blocked by governance/integration gates.

## Entry 004 — Freeze pack state
Date: 2026-08-14
Finding: `MURPHY_0006_0007_FINAL_FREEZE_REVIEW_PACK_V1.zip` states QA PASS but production freeze false; open gates are formal evaluator integration, governance approval, and explicit freeze manifest/decision.
Result: Do not declare Production Frozen yet.

## Entry 005 — Anti-regression rule
Date: 2026-08-14
Finding: Conversational claims are not sufficient evidence.
Decision: Every material discovery must be written to this log and/or a dedicated evidence artifact with inputs, hashes, method, result, and governance impact.

## Entry 006 — Governance review V2
Date: 2026-08-14
Finding: The current operational contract is deterministic and reproducible, but several clauses are project operationalizations rather than verbatim Murphy numeric/deterministic source text.
Evidence: `MURPHY_0006_0007_GOVERNANCE_REVIEW_V2.md`; `MURPHY_0006_0007_FORMAL_OPERATIONAL_CONTRACT_V1.md`; Murphy source/provenance artifacts.
Result: Governance approval remains OPEN. 0006/0007 remain QA PASS / NOT PRODUCTION FROZEN.

## Entry 007 — Source-lock search result
Date: 2026-08-14
Finding: Current Workspace search still exposes the original registry wording as "A third successful touch and reaction confirms the trendline" and explicitly states that exact operational meanings for successful touch, reaction, third touch, and confirmation/availability timing were not proven from an authoritative project contract.
Evidence: `PROJECT_CURRENT_STATE.md`, `AI_TRADING_ASSISTANT_PROJECT_CURRENT_STATE_2026-08-12_MURPHY_0006_0007.md`.
Result: No new authoritative deterministic contract was found in the accessible source material during this review. Do not promote the operational clauses as source text.

## Entry 008 — Full-book review boundary
Date: 2026-08-14
Finding: The supplied Murphy source package was reviewed as the broader source context. Chapter 4 is the primary source for 0006/0007 trendline semantics. Other chapters provide adjacent technical-analysis context but do not, from the accessible project artifacts reviewed, create a rule-specific 0006/0007 numeric touch/reaction/no-break contract.
Result: Do not import thresholds or semantics from unrelated chapters into 0006/0007. Keep Chapter 4 as the primary semantic authority for this gate.

## Entry 009 — Chapter 4 compatibility matrix
Date: 2026-08-14
Finding: Chapter 4 supports the qualitative structure of 0006/0007: reaction-low/high trendline families, two anchors, third successful touch, directional reaction, and no meaningful break. The existing project operator is compatible at the qualitative level. However, its deterministic clauses remain explicitly labeled project operationalization.
Important exclusion: Chapter 4's general 3% price-filter and 2-consecutive-daily-close examples are NOT rule-specific authorization for 0006/0007 and remain unbound.
Evidence: `MURPHY_0006_0007_CH4_COMPATIBILITY_MATRIX_V1.md`; `MURPHY_0006_0007_CONFIRMATION_CONTRACT_V2_DRAFT.md`; `MURPHY_0006_0007_FORMAL_OPERATIONAL_CONTRACT_V1.md`.
Result: Source compatibility is sufficient for governance review, but the production freeze decision remains OPEN. No semantic change or new threshold is authorized.

## Entry 010 — Direct Geometry V1 artifact/schema audit
Date: 2026-08-14
Method: Reconstructed the uploaded 597,678,846-byte GBPUSD Rule Evaluator V2 workspace from its split parts, stripped the `.bcut` metadata headers, validated the ZIP, and directly inspected the canonical Geometry V1 build contract, manifest, QA report, and D1 trendline output.
Findings:
- `TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json` states: input=`PIVOT_SEQUENCE_V2`; line generation=`consecutive pivots of the same type only`; slope=`exact price change / elapsed seconds`; availability=`later confirmation timestamp of the two defining pivots`; pattern classification and breakout detection are explicitly excluded; thresholds added=false; 2025 used=false; line cannot be available before both defining pivots are confirmed.
- `TRENDLINE_GEOMETRY_MANIFEST_V1.csv` includes a D1 output with 806 lines: `GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv`.
- The D1 Geometry output schema is explicitly: `line_id,line_type,point_1_timestamp,point_1_price,point_2_timestamp,point_2_price,slope_price_per_second,direction,availability_timestamp,point_1_availability,point_2_availability,source_file`.
- `TRENDLINE_GEOMETRY_QA_V1.csv` reports slope_ok, availability_ok, chronology_ok, type_ok, and no_2025 as true for the D1 output and the listed timeframe outputs.
Result: The previous wording that Geometry V1's schema was not exposed is superseded. Geometry V1 is now directly proven as an upstream geometry primitive that emits line identity, family, direction, anchors, slope, and availability. It intentionally does NOT emit third-touch/reaction/no-break fields; those belong in the separate Murphy Confirmation Layer/operator above Geometry. Therefore Geometry V1 is NOT the current blocker.
Governance impact: close the Geometry-schema blocker. Keep the operational no-break governance gate open; do not rebuild Geometry.

## Entry 011 — Explicit governance decision
Date: 2026-08-14
Finding: The project now has an explicit governance record approving the current deterministic 0006/0007 operationalization as the project's executable translation of Murphy Chapter 4 semantics.
Evidence: `MURPHY_0006_0007_GOVERNANCE_DECISION_V1.md`.
Decision: CONDITIONAL APPROVAL. Murphy remains the semantic authority; the operational contract is explicitly an implementation translation, not verbatim numeric Murphy wording. No 3%, 2-day, ATR, pip, arbitrary tolerance, hidden lookback, or 2025 tuning is authorized.
Impact: Governance approval gate is CLOSED/PASS. Remaining freeze gate is production-path integration and explicit freeze manifest.

## Entry 012 — Fresh production-path replay after operator correction
Date: 2026-08-14
Method: Executed the corrected `murphy_event_operator.py` locally against the canonical D1 Pivot V2 and Geometry V1 artifacts extracted from the full Rule Evaluator V2 workspace, with D1 rebuilt from the supplied M1 master using calendar-date OHLC aggregation. No reference result artifact was read by the replay.
Input hashes:
- Pivot V2: `bd9df3ec9fea3e180628daf9d4a079b5d030edbb4a3bd659c4a7baf9de6033f8`
- Geometry V1: `9394b594a15a9e0e33a3fda14364b9158fda13ff074a325df24997c92295b1b3`
- M1: `e0383c003fdb08e8776e68a4e8d1cc30529c0be55799295c0ffbdd52a80e1bb8`
- Rebuilt D1: `467d6a08ee59721e4a6048b7888b4d19b6da8d2fa46a89f6af47249b27cd31cb`
Result: `MURPHY_0006=8`, `MURPHY_0007=7`, `total=15` across 2016–2024. 2025 excluded. First same-family candidate is enforced; reaction is strictly after touch by event timestamp; availability is used as the no-lookahead gate.
Evidence: `MURPHY_0006_0007_PRODUCTION_PATH_VALIDATION_V1.md`.
Impact: Fresh replay gate CLOSED/PASS. This proves corrected evaluator behavior with canonical inputs; it does NOT by itself prove that the evaluator is merged into an external Decision Brain runtime. That final integration claim remains OPEN until an explicit production-path adapter/integration artifact is recorded.

## Next required discovery
Complete explicit production-path adapter/integration validation, then create the final freeze manifest and freeze decision if the integration gate passes.
