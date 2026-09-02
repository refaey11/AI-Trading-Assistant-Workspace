# AI Trading Assistant — Decision Brain
## Project Checkpoint / Handoff — 2026-09-02

PURPOSE
This checkpoint records the verified project state, integration findings, governed sources, decisions, failures, and next actions so work is not lost between chats. It is diagnostic/handoff state only; it does not authorize profitability claims or OOS tuning.

============================================================
1. PROJECT IDENTITY — NON-NEGOTIABLE
============================================================
- Project: AI Trading Assistant — Decision Brain.
- Goal: governed Decision Brain, not a dumb indicator.
- Existing knowledge/components must be audited and integrated, not rebuilt from scratch.
- Murphy = directional market context.
- Nison = candlestick confirmation/contradiction; never independent direction.
- Similarity / Historical Context / Historical Outcome / Context-Aware Retrieval = historical evidence only; never sole direction generator and never tuning engine.
- TIZ = process/psychology context only.
- Risk = hard execution gate.
- 2025 = locked OOS; never use 2025 for calibration/tuning.
- No official profitability claim until governed runtime, provenance, leakage, funnel, risk, cost/slippage and execution checks pass.

============================================================
2. GITHUB CURRENT DEVELOPMENT STATE
============================================================
Repository: refaey11/AI-Trading-Assistant-Workspace
Main current known commit: eae7d7f590bff410b280d21d7ad4dad379d34b12
Development branch: current-stack-dev-backtest-2016-2024-v3
Diagnostic branch: diagnostic/mtf-gate-observable-2026-09-02
Diagnostic head at checkpoint time: 46e96a23930e882c1972ec37a75d612b7696427f
Diagnostic branch must not be blindly merged into main.

Open diagnostic / related PR context:
- PR #86 diagnostic/mtf-gate-observable-2026-09-02 -> current-stack-dev-backtest-2016-2024-v3; draft/open; diagnostic only.
- Other open PRs exist for opportunity funnel, Nison decision integrity, and Murphy reconciliation; do not merge blindly.

Canonical Risk Engine fix on main:
- RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py
- CURRENT_CANONICAL_MIN_RR = 2.0
- RR_TOLERANCE = 1e-10
- main commit eae7d7... contains the canonical fix.

V5.4 replay risk contract:
- BASE risk 0.005
- AFTER_TWO_LOSSES 0.0025
- MAX 0.015
- SL = 0.75 ATR
- TP = 2.0R
- rr_target was corrected from 1.5*ATR to TP_R*stop_distance.
- fix commit: 87b50f...
- static test: 8d5b2b5...

============================================================
3. CANONICAL MTF SOURCE — SIX TIMEFRAMES
============================================================
Canonical six TFs: M5, M15, M30, H1, H4, D1.
Canonical Dropbox archive:
- /MTF_ALIGNMENT_GBPUSD_V1.zip
- Dropbox id known from prior verification: id:u18dZfxRtWwAAAAAAAAAGw
- size approximately 80MB
- purpose: Market Intelligence / Market Reading, not strategy/indicator.

Evidence pack:
- audits/evidence/MTF_ALIGNMENT_GBPUSD_V1_EVIDENCE_2026-08-21.md
- GBPUSD, base M5, complete_2016_2026.
- 106 columns with M5_/M15_/M30_/H1_/H4_/D1_ prefixes.
- aggregate fields include mtf_trend_score plus bullish/bearish/neutral counts/context.
- anti-leakage: higher-TF features only after source candle close.
- official gate previously recorded as PASS / EXISTING EVIDENCED INPUT ARTIFACT.

Old local archive /mnt/data/07/AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1.zip is research-only H4/H1 and is NOT canonical. M15 must never be fabricated from H1.

MTF runtime join:
- RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py
- requires mtf_trend_score and six *_trend_regime fields.
- UTC timestamps, duplicates rejected, numeric/non-NaN required.
- merge_asof backward with exact matches allowed.
- missing source-backed MTF rejected.
- future input rejected.
- defaults_used=false, direction_generated=false, risk_generated=false.

Governance:
- M5 execution confirmation
- M15 short-term structure/confirmation
- M30 local structure/pullback
- H1 primary intraday
- H4 higher context
- D1 major context
- W1 macro context exists conceptually but is outside the six-field canonical event contract.
- MTF never generates BUY/SELL by itself.
- missing volume is not zero.
- no guessed numeric encodings, zero-fill, translation, imputation or scaling.
- all values must be source-backed and as-of causal.

Latest MTF smoke workflow:
- workflow run 33577238368 (run #9)
- commit 46e96a...
- conclusion: SUCCESS
- MTF source gate: PASS.
- Raw gaps were only leading warm-up gaps, not mid-series data holes.

============================================================
4. MTF PROVENANCE BLOCKER / WIRING DECISIONS
============================================================
BACKTEST/MTF_PROVENANCE_BLOCKER_2026-09-02.md states:
- old MTF reader is research-only H4/H1.
- old categorical->numeric mapping was unproven and is forbidden as canonical.
- producer contract must be exact: field order, semantics, categorical encoding, missing/imputation, scaling, lineage, as-of.
- compatible inputs may use only selection/rename; incompatible input means MTF->Brain NOT_EVALUABLE.
- official 2016-2024 profitability cannot be claimed before provenance closes.

Commit ea272cf... changed V5.4 MTF wiring to use producer values verbatim:
- annual source files unique/year
- required MTF fields numeric
- producer_values_used_verbatim=true
- categorical_translation_applied=false
- imputation_applied=false
- scaling_applied=false

BACKTEST/mtf_source_contract_gate_v1.py is fail-closed on the six-TF contract and allows only a leading warm-up prefix; missing required values after the first fully complete six-TF row are rejected.

============================================================
5. GATE 3C — CANONICAL E2E CONTRACT
============================================================
Gate order:
H1 -> Market State -> Dynamic MTF/context -> Murphy 34 -> Nison 44 -> Historical Context Memory -> Historical Outcome Memory -> Similarity V2 -> Context-Aware Retrieval V2 -> TIZ process gate -> Risk/Execution gate -> Knowledge/Decision handoff -> recovered Decision Brain V1 -> frozen execution/backtest contract.

No gate is allowed to invent evidence.
No historical memory is allowed to generate direction.
No Nison rule is allowed to generate direction independently.
No TIZ signal is allowed to generate direction.
Risk cannot be overridden.
2025/future data is forbidden.

============================================================
6. CURRENT GATE 3C FAILURE — EXACT STATE
============================================================
Observable workflow:
- .github/workflows/gate3c-e2e-observe-2026-09-02.yml
- event tested: 2016-04-20T09:00:00Z
- latest diagnostic run: 33577238405 (run #2)
- job: 100083790745
- conclusion: FAILURE

Passed before failure:
- event window validation
- governed source acquisition
- source slices ready
- MTF source acquisition/gating was not the failing component.

Failure stage:
- Build event slices and canonical bundle.
- Risk evidence bridge failed before the real single-event E2E was executed.

Exact failure:
ValueError:
/mnt/.../murphy/MURPHY_2016_2024_FULL_EVIDENCE.csv:
expected exactly one directional PASS row at
2016-04-20T09:00:00+00:00,
observed=0

This comes from OOS_2025/build_single_event_risk_evidence_v1.py -> _one_directional_murphy_row().

Interpretation:
THIS IS A BRIDGE/SCHEMA MISMATCH, NOT AN MTF FAILURE.
The Murphy source is a 34-rule fan-in stream. It is not guaranteed to have one directional PASS row at every timestamp. The bridge's assumption of exactly one directional PASS row is invalid for the canonical fan-in contract.

============================================================
7. IMPORTANT MURPHY SOURCE FINDING
============================================================
Canonical Dropbox Murphy archive found and inspected:
- /New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip
- size 314,490 bytes (307.12 KB)
- server modified 2026-08-28T01:17:55Z
- contains MURPHY_2016_2024_FULL_EVIDENCE.csv.

Observed source schema from extracted content:
- timestamp
- status
- direction
- source_rule_id
- pass_rule_id
- source_event_count

Example early rows show composite source_rule_id values such as MURPHY_0025|MURPHY_0026, confirming fan-in semantics.

The canonical builder already handles this model correctly:
- tools/gate3c_build_single_event_bundle_v1.py
- it selects the Murphy CSV by timestamp/source_rule_id
- preserves ALL event rows
- splits composite source_rule_id values
- validates against the 34-rule governed ID set
- passes full murphy.rows into Gate 3C.

The real E2E runner also expects the fan-in:
- RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py
- restores event timestamp at envelope level only for the lossless fan-in API
- calls OOS_2025/governed_rule_fan_in_v1.py
- does not require one Murphy directional row.

Therefore the risk evidence bridge is the inconsistent component.

============================================================
8. EXISTING DECISION BRAIN DIRECTION BOUNDARY
============================================================
Full Brain bridge:
- RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py
- loads recovered Decision Brain V1 without changing it.

Governance handoff:
- compatibility/decision_brain_v1_handoff_adapter.py
- calls recovered brain.assess(row_copy, similarity=None)
- Murphy evidence is carried as knowledge_alignment/murphy_evidence.
- Nison/TIZ do not generate direction.
- historical memory is sanitized and remains evidence-only.

Three-book evaluator:
- evaluation/three_book_decision_evaluator_v1.py
- checks Murphy status/direction against the Decision Brain directional_bias.
- requires risk_pass and stop_loss.
- rejects Nison contradiction.
- final BUY/SELL is derived from the existing brain directional_bias, not from memory/Nison/TIZ.

This means the bridge should NOT fabricate direction from the Murphy fan-in. It should preserve source-backed fan-in semantics and let the existing Brain/Three-Book boundary consume them.

============================================================
9. RISK / EXECUTION CONTRACT
============================================================
Current frozen candidate risk profile:
- stop = 0.75 ATR
- target = 2R
- risk budget contract remains governed/frozen.

Canonical Risk Engine minimum RR is 2.0.
Risk evidence must be authoritative.
No internal runner shortcut using 0.75 ATR / 2R with costs=false is accepted as a substitute for the canonical Risk Engine.

============================================================
10. PREVIOUS PROJECT STATE — DO NOT MISREAD
============================================================
Dropbox file /AI_Trading_Assistant_PROJECT_STATE_2026-08-31.md reported a previous bounded Gate 3C success around event 2024-12-31T16:00:00Z, including a successful Brain->Risk->Trade Plan E2E result.
That is historical and must NOT be confused with the current 2026-09-02 diagnostic state.
The current diagnostic branch is testing a different real single-event path and currently fails at the Murphy->Risk evidence bridge before Brain execution.

Earlier historical issues already encountered and resolved/diagnosed:
- Dropbox 401/409 acquisition issues.
- single-event H1/timestamp mismatch.
- unbounded discovery launcher canceled after ~20 minutes; bounded discovery then succeeded.
- legacy/simplified backtest launchers identified as diagnostic-only and not official profitability evidence.

============================================================
11. RULE-WIRING GOVERNANCE
============================================================
OOS_2025/audit_final_78_rule_wiring_v1.py documents the 78-rule governed envelope:
- Murphy 34
- Nison 44
- all rule IDs must be allowlisted.
- no synthetic rule IDs.
- Murphy rules must remain source-backed and provenance-preserving.
- missing/deferred rules remain NOT_EVALUABLE; no synthetic substitute.
- official P&L remains blocked until the required 34-rule Murphy evidence fan-in and per-rule provenance are fully wired and the runtime scope is active/dispatched.

============================================================
12. IMMEDIATE NEXT ACTION — NO STRATEGY CHANGE
============================================================
1) Fix ONLY the Murphy->Risk evidence bridge on diagnostic branch.
2) Preserve the 34-rule fan-in losslessly.
3) Do not select an arbitrary "first" Murphy PASS row.
4) Do not create BUY/SELL from source_rule_id, pass_rule_id, counts, or composite row order.
5) If the event has no source-backed directional pass compatible with the frozen risk contract, the bridge must fail closed as NOT_EVALUABLE / risk blocked rather than invent direction.
6) Prefer existing governed fan-in/adapters already in repository over inventing a new decision layer.
7) Rerun Gate 3C observable workflow.
8) Verify build -> real single-event E2E -> contract audit -> artifact.
9) Only after a genuine single-event E2E PASS/NO_TRADE with intact governance should the 2016-2024 development backtest be reconsidered.

============================================================
13. DO NOT DO THESE THINGS
============================================================
- Do not redesign the trading strategy because of this failure.
- Do not add breakout/trend/volume/price-action logic as a reaction to this bridge error.
- Do not change Murphy rules.
- Do not tune against the failing event.
- Do not use 2025 for tuning.
- Do not fill missing MTF values.
- Do not convert categorical MTF values using guessed mappings.
- Do not let Memory/Similarity choose direction.
- Do not treat historical metrics from simplified runners as official.

============================================================
14. CURRENT BOTTOM LINE
============================================================
MTF source gate: PASS.
Source acquisition: PASS.
Canonical fan-in builder: already understands Murphy 34-rule rows.
Risk evidence bridge: FAILING because it incorrectly expects one directional Murphy PASS row.
Real Brain E2E: NOT YET EXECUTED on the latest diagnostic run because the builder stopped first.
2016-2024 official profitability: BLOCKED.
Strategy redesign: NOT WARRANTED.

CHECKPOINT CREATED: 2026-09-02
