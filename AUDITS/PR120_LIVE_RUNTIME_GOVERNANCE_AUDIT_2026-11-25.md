# PR #120 Live Decision Runtime Governance Audit — 2026-11-25

## Scope and method
Read-only, GitHub-only inspection of PR #120 branch `feature/live-decision-runtime-v1`:
- `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/test_live_decision_runtime_v1.py`
- `RUNTIME/TIZ_PROCESS_GATE_V1/tiz_process_gate_v1.py`
- `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`
- `evaluation/three_book_decision_evaluator_v1.py`
- `03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json`
- `.github/workflows/live-decision-runtime-v1.yml`

This is a static code audit, not a run or certification. No tests/workflows were run. No market-data payloads were accessed. No 2025 OOS or 2026 market data was read. No runtime/source files were changed. No PR was merged, no branch was rebased, and main was not modified.

## 1. Canonical 3R gate: implemented in this path
The live runtime imports `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py::evaluate_risk`, which enforces `CURRENT_CANONICAL_MIN_RR = 3.0`, 0.5–4 ATR stop bounds, and drawdown breaker. The live runtime returns BLOCKED when the Risk result fails. Its tests include a 2R rejection and the valid fixture expects exactly 3R.

This supports the narrow statement that PR #120's inspected live runtime calls the canonical 3R Risk implementation. It does not prove live market feed, broker integration, profitability, or production readiness.

## 2. Direction authority is not Murphy-exclusive
The runtime:
1. derives `assessment.directional_bias` by calling recovered Brain V1 on `normalized_row`;
2. Brain V1 creates bullish/bearish evidence from `mtf_trend_score` and six `*_trend_regime` values (and can include volume evidence);
3. the Three-Book evaluator chooses final BUY/SELL from Brain `directional_bias`;
4. Murphy is checked for PASS and for conflict with Brain, and final output is checked against Murphy direction.

There is no proof in this path that Brain's directional bias was generated exclusively from Murphy-governed direction. Agreement is not derivation. The runtime's Murphy rule IDs/pass-rule provenance checks do not bind the actual Brain directional features to Murphy's approved direction source.

This is a governance blocker under the project invariant that Murphy owns directional authority and MTF must not independently become a second direction generator. The seven MTF field producer semantics remain separately unresolved.

## 3. TIZ implementation conflicts with the effective project boundary
The inspected `03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json` says:
- TIZ role is `optional_metadata_only`;
- it cannot block/allow trade;
- missing/failed TIZ must not block runtime.

But PR #120:
- requires a TIZ evidence mapping in its required evidence loop;
- requires it to pass an authoritative source envelope;
- calls `evaluate_tiz_gate`;
- returns BLOCKED unless TIZ process state is READY;
- includes a test that explicitly expects a TIZ process failure to block.

This directly contradicts the effective 2026-11-12 project decision. Do not merge as-is. Resolution must be metadata-only; do not manufacture READY/PASS.

## 4. Brain no-trade reasons are not enforced by the live adapter
Recovered Brain V1 adds no-trade reasons when volume is unavailable, among other cases. PR #120 serializes `assessment.no_trade_reasons` into its audit payload, but the runtime does not gate on that list before calling the evaluator. The evaluator does not inspect Brain's `no_trade_reasons`; it only checks directional bias, Murphy conflict, Risk pass, and Nison contradiction.

Therefore a Brain assessment may carry a no-trade reason while the live adapter still produces SIGNAL_READY if the other checks pass. Whether each reason should be a hard gate requires a governed contract review; silently ignoring the reasons is not justified.

## 5. Source envelope is asserted, not authenticated
`_require_source_envelope` checks boolean `authoritative is True`, non-empty source/producer strings, and `available_at <= query_as_of`. The inspected function does not authenticate producer identity against a registry, validate signatures/hashes, or bind producer version/config/source lineage to an approved contract. The MTF row-to-envelope equality check proves copied values match, not that the producer or feature semantics are authenticated.

This is particularly material because the canonical six-timeframe producer formula, source clock/timezone, candle-close semantics, and missing-value policy remain unresolved in the project audits. The PR description itself lists this as a hard integration gap. The PR must remain signal-only and not be treated as source-authenticated production.

## 6. Event freshness gap
The runtime rejects decision timestamps more than five minutes in the future and rejects years <= 2025, but the inspected code does not impose a maximum age for a 2026 event. A timestamp days old can pass the year/future checks if all source `available_at` values are no later than that timestamp. This is not sufficient for a live-event freshness contract. Define an explicit maximum event age and source freshness policy before live use.

## 7. Execution boundary
The runtime explicitly returns `SIGNAL_ONLY`, `orders_enabled=False`, and `broker_volume=None`. The PR body also states MT5 order adapter is not connected. This is an important safety boundary and must remain intact. No broker lot sizing or order lifecycle was verified here.

## 8. Workflow and test evidence
The PR description claims the dedicated Live Decision Runtime V1 Actions workflow passed on its current head, and separately reports CircleCI failures. This audit did not independently retrieve a workflow run tied to a verified PR head SHA and did not rerun tests. The workflow is triggered by PR/push path filters and runs the live runtime test file plus canonical risk reconciliation tests. Treat the claimed PASS as a PR-description claim until the exact run/head SHA and job logs are independently verified.

## Required remediation before approval
1. Remove TIZ from blocking/authorization logic; retain optional metadata only, per the effective 2026-11-12 decision.
2. Establish Murphy as the exclusive directional authority. MTF may provide governed technical context only after its producer semantics and Murphy mapping are authenticated; it must not independently generate a competing final direction.
3. Define and enforce which Brain no-trade reasons are hard gates; do not discard them silently.
4. Authenticate MTF/Murphy/Nison/Risk producer identity and provenance, not merely self-asserted booleans and strings.
5. Add explicit maximum event age and source freshness rules.
6. Preserve canonical 3R hard gate and SIGNAL_ONLY/no-orders boundary.
7. Add adversarial tests for: TIZ missing/FAIL remains non-blocking metadata; MTF/Brain direction cannot override Murphy; Brain no-trade reasons; unregistered producer; stale event; canonical 2R rejection.
8. Resolve the MTF producer/clock/field semantics blocker before treating any signal as production-eligible.

## Status
- Canonical 3R call in PR #120 live runtime: PRESENT by static inspection.
- 2R rejection test: PRESENT, not run in this audit.
- Murphy-exclusive direction: NOT PROVEN.
- TIZ metadata-only compliance: FAILS static inspection.
- Brain no-trade reason enforcement: NOT PRESENT.
- Producer authentication: NOT PROVEN.
- Live event freshness bound: NOT PRESENT.
- MT5 orders: DISABLED / NOT CONNECTED.
- Production readiness: NOT ESTABLISHED.
