# Decision Brain Architecture / Risk / TIZ Audit — 2026-11-25

## Status
AUDIT ONLY — no runtime changes, no PR merge, no production/trading approval.
Scope is GitHub repository inspection only. No Dropbox access. No 2025/2026 market-data payloads accessed.

## Repository branch authority and drift
- The active development line referenced by PR #119 is `current-stack-dev-backtest-2016-2024-v3`.
- PR #119 is draft/open and targets that development branch, not `main`.
- The canonical Risk Engine on the development base branch uses `CURRENT_CANONICAL_MIN_RR = 3.0`.
- PR #119 head retains 3R and adds fail-closed numeric validation plus stop/target orientation validation.
- The repository default `main` currently contains `CURRENT_CANONICAL_MIN_RR = 2.0` in the same canonical Risk Engine path. This is branch drift and must not be silently treated as the active development contract. Do not cherry-pick or merge without a branch reconciliation plan.

## Risk contract finding
There are two intentionally separate contracts:
1. Canonical Risk Integration: minimum 3R, enforced by `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py` on the development line.
2. Frozen candidate/evaluation protocol: 0.75 ATR stop and 2R target, used by V5.4 / Gate 3C evaluation paths. It is not canonical production authorization.

PR #106 was merged into the development line and documents this separation. Its regression tests require canonical 3R to pass, canonical 2R and 1.5R to fail, while the candidate evaluation 2R profile remains accepted.

PR #119 adds important canonical Risk hardening:
- rejects non-finite equity, entry, risk budget, SL/TP/ATR, RR and position-size values;
- rejects SL and TP on the same side of entry;
- accepts valid long/short bracket geometry;
- retains the canonical 3R boundary;
- checks development execution levels against the canonical Risk result.

Latest observed PR #119 head: `289b99cbf3567fd65b4fa7d507be24f2c50f07a3`.
Observed GitHub Actions for that SHA:
- Risk Contract Separation Tests: success.
- TIZ Metadata-Only Compatibility: success.
- Current Stack V5.4 workflow: success (the job step is named "Run governed V5.4 replay"; this is not, by itself, proof of profitability or production readiness).
- MTF Source Gate Smoke: failed at "Download exact MTF archive"; validation and contract-gate steps were skipped. No annual source validation was completed by that run.

## TIZ authority conflict — unresolved architectural decision
The current checked-in policy `03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json` says:
- status: `SUPERSEDED_BY_PROJECT_DECISION_2026-11-12`;
- role: `optional_metadata_only`;
- decision_authority: false;
- TIZ cannot block/allow a trade, affect confidence, risk, SL/TP, or execution eligibility;
- missing/failed TIZ evidence is non-blocking metadata.

The current bridge and compatibility tests implement that metadata-only boundary. The PR #119 audit also states that the separate TIZ producer spec is `CANDIDATE_NOT_AUTHORITATIVE`, with 0/7 rules authoritative and 7 deferred.

This conflicts with the project's Master Map requirement that Trading in the Zone is a psychology/process gate and cannot generate direction. Do not resolve this by quietly changing code or by inventing psychological thresholds.

### Recommended resolution
- Preserve TIZ as non-directional: it must never create, reverse, confirm, or score market direction.
- Reconcile the 2026-11-12 metadata-only decision against the Master Map in a formally reviewed architecture decision.
- Before enabling TIZ as a hard process gate, audit the existing book-derived knowledge and define/approve the seven deferred rules with explicit evidence, states, provenance, and tests.
- Until that is complete, label TIZ as `NOT_IMPLEMENTED / NOT_EVALUABLE` in the architecture and do not claim the full intended Decision Brain process gate is implemented. Any execution path that requires the intended process gate must remain ineligible until the approved gate exists. Do not fabricate a TIZ PASS.

## MTF / provenance blocker
PR #119's latest MTF source workflow failed before archive inspection because the exact archive download step failed. The annual source validation and fail-closed contract gate were skipped. Therefore:
- no verified annual 2016–2024 MTF source validation is established by that run;
- exact producer/serialization semantics, broker timezone/DST provenance, candle-close rules, and source lineage remain unresolved;
- no live six-timeframe producer or source authentication is established.

Do not rerun legacy Dropbox-dependent workflows. The GitHub Release directory-only inspection remains a separate metadata-only investigation and has not yet been validated after its parser fix.

## Acceptance gates
1. **Risk contract:** retain canonical 3R vs candidate 2R separation; run the complete contract suite; inspect every caller to ensure candidate 2R cannot leak into canonical eligibility.
2. **TIZ architecture:** formally reconcile the metadata-only decision with the Master Map; audit the seven deferred rules from existing knowledge; approve exact semantics before coding.
3. **MTF source:** prove source identity, exact schema/serialization, timezone and candle-close semantics, continuity and six-TF conformance without accessing locked 2025/2026 data.
4. **Integration:** compatibility audit across Murphy, Nison, Similarity, TIZ, Risk and the runtime bridge; no component may take another component's authority.
5. **E2E:** source-backed pre-2025 events, then deterministic 2016–2024 samples; no live execution and no auto BUY/SELL in V1.

## Explicit non-actions
- `main` untouched.
- No PR merged or retargeted.
- No runtime or strategy code modified.
- No Dropbox access or legacy Dropbox workflow intentionally run.
- No 2025/2026 market-data payload read.
- No live order, broker action, or profitability claim.
