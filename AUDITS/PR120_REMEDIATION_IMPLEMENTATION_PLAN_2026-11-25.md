# PR #120 Remediation Implementation Plan — 2026-11-25

## Status
Planning specification only. This document does not change runtime behavior and does not authorize merging PR #119/#120, live trading, MT5 connectivity, or automated orders.

## Baseline and constraints
- PR #119 reviewed head: `289b99cbf3567fd65b4fa7d507be24f2c50f07a3`.
- PR #120 reviewed head: `d1df29b0d3526378402e47959a55a73b13bd1889`.
- These heads are divergent; PR #120 must not be described as stacked on the latest #119.
- Keep both PRs draft/open until the gates below pass.
- GitHub only. Do not use Dropbox, Dropbox-dependent Actions, or CircleCI source acquisition.
- Do not access 2025/2026 market-data payloads. 2025 is locked OOS and must not be used for tuning, calibration, feature selection, threshold selection, or development.
- No merge/rebase/cherry-pick to main. No broker connection, MT5 order, or live execution.
- Preserve canonical Risk minimum 3R and stop-distance constraints. Evaluation-only 2R is not canonical production authorization.
- Similarity remains memory/evidence only and must be passed as `None` to directional assessment paths.

## Approved authority model to enforce
1. **Murphy:** sole source of market direction. Direction must be traceable to an approved Murphy rule, pass status, and source provenance.
2. **Nison:** confirmation/contradiction only. It cannot originate or reverse direction.
3. **MTF and Volume:** contextual/validation evidence only. Neither may independently create, flip, strengthen, or suppress the final directional bias unless a separately approved contract explicitly permits a non-directional gate.
4. **Similarity:** historical memory/evidence only. No predicted-return-to-direction conversion and no confidence/direction influence.
5. **Risk:** hard gate; canonical 3R minimum, approved stop range, finite values, and drawdown breaker remain mandatory.
6. **Trading in the Zone (TIZ):** optional audit/process metadata only under the 2026-11-12 resolution. Missing, failed, NOT_READY, or NOT_EVALUABLE TIZ must not block, allow, or modify direction, confidence, risk, size, or signal eligibility. Do not synthesize READY.
7. **2025 OOS:** locked and excluded from all development/tuning workflows.

## Integration strategy
Do not retarget or rebase PR #120 directly. First complete isolated remediation work, then:
1. Re-read the latest approved #119 head and verify it is still the intended integration base.
2. Create a new integration branch from that exact approved #119 SHA (not from main).
3. Port/reconcile only reviewed #120 runtime changes onto that branch; resolve API/import changes explicitly.
4. Run compatibility and adversarial tests on the combined head.
5. Open a new draft PR only after exact-head tests and workflow triggers are inspected.
6. Keep original #119/#120 draft PRs untouched until the new branch is reviewed.

## Remediation work packages

### WP1 — Remove TIZ from authorization
Target: `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py` and its tests.
- Make TIZ evidence optional and non-authoritative metadata.
- Remove TIZ from required evidence-envelope loops and blocking predicates.
- Preserve any supplied TIZ payload as audit metadata without interpreting it as a permission gate.
- Missing/failed/NOT_READY/NOT_EVALUABLE TIZ must yield the same authorization result as absent TIZ, all else equal.
- Do not manufacture a READY state or replace the old gate with a different TIZ-derived gate.

Acceptance tests:
- TIZ absent vs READY vs NOT_READY vs failed vs malformed metadata: direction, confidence, risk result, and eligibility remain identical, with only metadata/audit output differing.
- Explicitly assert that TIZ cannot authorize a blocked trade or block an otherwise eligible signal.

### WP2 — Make Murphy the only directional authority
Target: live runtime assembly and the Brain/evaluator boundary.
- Establish one canonical Murphy direction object with approved rule ID, PASS status, direction, source/producer provenance, and event-time linkage.
- Derive the final BUY/SELL direction from that Murphy object only.
- Do not ask recovered Brain V1 to infer a competing direction from raw MTF regime/score or volume fields.
- Keep MTF/volume as context and diagnostics. They may be surfaced as supporting/conflicting context, but cannot create, flip, or change directional confidence.
- Nison may confirm or contradict the Murphy direction; it cannot originate or reverse it.
- Enforce Murphy authority at the runtime bridge itself, not only in Gate3C's upstream caller.

Acceptance tests:
- Hold Murphy fixed while varying MTF trend score/regimes across bullish, bearish, neutral, missing, malformed, and extreme values: final direction and directional confidence do not change.
- Hold Murphy fixed while varying volume across positive, negative, zero, missing, and malformed values: final direction and directional confidence do not change.
- Change Murphy direction while holding MTF/volume fixed: direction follows Murphy or fails closed if Murphy provenance is invalid.
- Missing Murphy, non-PASS Murphy, unknown rule, absent provenance, and Murphy/Risk direction mismatch must fail closed.
- Nison confirmation may annotate strength only within its approved contract; contradiction must follow the explicit Nison conflict policy and never reverse direction.

### WP3 — Enforce no-trade reasons
- Define the authoritative taxonomy and severity of each Brain `no_trade_reason`.
- Do not silently ignore a reason that the Brain marks as a hard no-trade condition.
- Separate informational warnings from hard blockers in a versioned contract.
- Until that taxonomy is approved, fail closed on any non-empty hard-block reason set; do not infer that every informational note is a hard block.

Acceptance tests:
- Each hard-block reason independently prevents SIGNAL_READY.
- Informational-only reasons do not change eligibility, but are preserved in the audit output.
- Unknown reason codes fail closed.

### WP4 — Authenticate source envelopes and MTF lineage
- Treat `authoritative: true` and non-empty source/producer strings as assertions, not authentication.
- Require a governed producer/source registry and immutable source identity or verifiable manifest/hash, producer version/config fingerprint, symbol, timeframe, event-time semantics, and availability-time semantics.
- Validate field-level MTF encoding/scaling/missing-value policy for all seven Brain MTF fields before any production eligibility.
- Preserve the existing artifact-family closure finding, but do not misstate it as proof of exact field semantics or clock authentication.
- Volume-to-Brain six-timeframe lineage remains OPEN / NOT EVALUABLE until a committed producer and adapter mapping are demonstrated.

Acceptance tests:
- Forged authoritative flags, unknown producer IDs, mismatched hashes, altered config fingerprints, wrong symbol/timeframe, and incomplete field manifests all fail closed.
- Exact verified manifest and producer identity pass structural/authentication checks without reading any 2025/2026 data.

### WP5 — Event freshness and clock semantics
- Define a maximum event age and source-age policy in an approved contract.
- Validate source availability time, event time, candle close time, timezone/clock provenance, and allowed skew.
- Reject stale 2026 events as well as future events outside approved skew.
- Do not infer candle identity from raw epoch timestamps or composite keys. Preserve the existing source-bar identity decision: native immutable upstream ID preferred; fallback only after explicit evidence and approval.

Acceptance tests:
- Fresh, stale, future, out-of-order, duplicated, and clock-skewed events.
- Missing or unauthenticated clock/candle-close semantics fail closed for production eligibility.

### WP6 — Preserve risk and execution boundaries
- Keep canonical minimum RR at 3R and stop distance within the approved 0.5–4 ATR range.
- Keep evaluation-only 2R isolated and explicitly non-production.
- Verify drawdown breaker and finite-value checks at the canonical authorization boundary.
- Keep runtime output SIGNAL_ONLY, `orders_enabled=false`, and no broker volume/MT5 execution until a separate authorization and Demo E2E program is approved.

Acceptance tests:
- 3R valid case may pass risk; 2R and 1.5R canonical cases fail.
- Evaluation-only candidate tests remain isolated and cannot authorize production.
- Risk fail, non-evaluable risk, invalid SL/TP, and drawdown breaker prevent SIGNAL_READY.
- No code path emits an order or enables broker execution.

## GitHub-only data and CI policy
- Retire/disable Dropbox-dependent source-acquisition workflows from any proposed integration path; do not execute them.
- Do not run CircleCI source acquisition or any workflow that references Dropbox tokens/archives.
- Before any new workflow dispatch, inspect its triggers and every invoked script for Dropbox, CircleCI, broad archive downloads, or 2025/2026 selectors.
- Source manifests must identify only approved 2016–2024 inputs and be immutable/reviewable in GitHub. Check repository size, licensing, privacy, and access controls before committing any payload. Do not place large/raw market data in GitHub without a separate explicit approval.
- Prefer contract/unit tests using synthetic fixtures that cannot load external market data. Any historical validation must use an independently verified 2016–2024-only source path.

## Test and review order
1. Unit tests for each WP in isolation.
2. Authority adversarial tests (Murphy vs MTF/volume/Nison/Similarity).
3. TIZ non-blocking compatibility tests.
4. Source-envelope authentication and freshness tests.
5. Canonical 3R and drawdown tests.
6. Combined runtime integration tests on the exact new integration SHA.
7. Inspect every workflow trigger and job command before allowing Actions to run.
8. Verify each required job's run SHA, conclusion, and logs; a PR description or green unrelated workflow is not evidence.
9. Independent code review of the final diff and all caller paths before changing PR status.

## Stop conditions
Stop and report NOT READY if any of the following remains:
- TIZ can block/allow or change direction/confidence/risk/eligibility.
- MTF, volume, Nison, or Similarity can generate/alter final direction.
- Murphy direction lacks governed rule/source provenance.
- Any hard no-trade reason is ignored or its semantics are unknown.
- Source identity, MTF field semantics, volume lineage, clock provenance, or event freshness is unauthenticated.
- Canonical 3R can be bypassed by a production-eligible path.
- Any workflow requires Dropbox, CircleCI acquisition, or can reach 2025/2026 data.
- Exact combined-head tests are missing or fail.

## Current disposition
PR #119: DRAFT / NOT MERGE-READY (MTF acquisition failed HTTP 401; Dropbox dependency conflicts with GitHub-only policy).
PR #120: DRAFT / NOT MERGE-READY (TIZ blocking and non-Murphy directional inference are hard contract violations).
Combined integration: NOT READY. This plan is a reviewable implementation blueprint, not evidence that remediation has been implemented or tested.
