# Decision Brain Architecture / Risk / TIZ Audit — 2026-11-25

## Status
AUDIT ONLY — no runtime changes, no PR merge, no production/trading approval.
Scope is GitHub repository inspection only. No Dropbox access. No 2025/2026 market-data payloads accessed.

## Repository branch authority and drift
- The active development line referenced by PR #119 is `current-stack-dev-backtest-2016-2024-v3`.
- PR #119 is draft/open and targets that development branch, not `main`.
- The canonical Risk Engine on the development base branch uses `CURRENT_CANONICAL_MIN_RR = 3.0`.
- PR #119 head retains 3R and adds fail-closed numeric validation plus stop/target orientation validation.
- The repository default `main` currently contains `CURRENT_CANONICAL_MIN_RR = 2.0` in the same canonical Risk Engine path.
- GitHub compare reports `main` and the development branch are diverged: development is 355 commits ahead and 131 behind, with merge base `4fcaa7e4567396cbb2734736efb79fbf08d631dc`. This is substantial branch drift, not a safe one-commit backport. Do not merge, rebase, cherry-pick, or use `main` as the development source without a separate branch-reconciliation plan.

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

## TIZ authority conflict — current repository decision is explicit
The development branch contains `docs/TIZ_DECISION_AUTHORITY_CHANGE_2026-11-12.md`. It explicitly says the project owner removed TIZ from the Decision Brain decision path because no authoritative reliable TIZ runtime producer had been established. It makes TIZ optional metadata only. This is an intentional checked-in project decision, not an accidental code omission.

The policy `03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json` and compatibility tests enforce:
- role: `optional_metadata_only`;
- decision_authority: false;
- TIZ cannot block/allow a trade, affect confidence, risk, SL/TP, or execution eligibility;
- missing/failed TIZ evidence is non-blocking metadata.

The earlier producer-gate specification `TRADING_IN_THE_ZONE/TIZ_RUNTIME_BOUNDARY_PRODUCER_GATE_V1.md` records seven candidate rules:
- PSY_0001 PREDEFINE_RISK — blocked;
- PSY_0002 ACCEPT_RISK — candidate only;
- PSY_0003 INDEPENDENT_OUTCOMES — process-only;
- PSY_0004 NO_CERTAINTY — blocked;
- PSY_0005 CUT_LOSS_RULE — blocked;
- PSY_0006 SYSTEMATIC_PROFIT — blocked;
- PSY_0007 RULE_DISCIPLINE — candidate only.
It explicitly says no authoritative producer exists and no rule should be frozen without evidence/provenance and deterministic semantics.

This checked-in decision conflicts with the user's earlier Master Map description of TIZ as a psychology/process gate. The current repository state follows the 2026-11-12 decision. Do not silently reverse it. If the project owner's latest intent is to restore TIZ as a hard process gate, that requires a new superseding architecture decision and completion of the seven-rule producer/provenance contract. TIZ must remain direction-neutral under either policy.

## Recommended resolution
- For the current code line, preserve the explicit 2026-11-12 metadata-only decision until the project owner supersedes it.
- Do not claim the original Master Map's TIZ process gate is implemented.
- If reinstatement is authorized, first audit existing TIZ knowledge, then approve each rule's evidence, state semantics, availability, timestamp, provenance, and tests. No invented psychological thresholds and no fabricated PASS.
- Until an authoritative producer exists, any future process-gate implementation must remain NOT_IMPLEMENTED / NOT_EVALUABLE; do not promote it to execution authority.

## MTF / provenance blocker
PR #119's latest MTF source workflow failed before archive inspection because the exact archive download step failed. The annual source validation and fail-closed contract gate were skipped. Therefore:
- no verified annual 2016–2024 MTF source validation is established by that run;
- exact producer/serialization semantics, broker timezone/DST provenance, candle-close rules, and source lineage remain unresolved;
- no live six-timeframe producer or source authentication is established.

Do not rerun legacy Dropbox-dependent workflows. The GitHub Release directory-only inspection remains a separate metadata-only investigation and has not yet been validated after its parser fix.

## Acceptance gates
1. **Risk contract:** retain canonical 3R vs candidate 2R separation; run the complete contract suite; inspect every caller to ensure candidate 2R cannot leak into canonical eligibility.
2. **TIZ authority:** preserve the 2026-11-12 decision unless explicitly superseded; if superseded, audit and approve the seven-rule producer contract before coding.
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
