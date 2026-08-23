# Murphy 0021 Fresh 2025 — CI Green Checkpoint

Date: 2026-08-23

## Verified CI state
- Branch: `oos-2025-murphy-0021-fresh-v1`
- Fresh Murphy 0021 producer: CircleCI Run 5063 — SUCCESS
- Nison 2025 full production: CircleCI Run 5061 — SUCCESS
- 78-rule 2025 coverage job: CircleCI Run 5062 — SUCCESS
- Runtime / Decision Brain / Risk / TIZ / Memory checks on the same commit: SUCCESS

## Controlled fixes applied before the green run
1. Added repository root to Python import path for the producer runtime.
2. Corrected the authoritative M1 source filename used by the CircleCI acquisition step.
3. Refreshed the CircleCI Dropbox credential after the prior 401 Unauthorized failure.
4. Rewired Murphy 0021 volume context to the canonical project path: authoritative M1 volume aggregated to H1, then current H1 volume versus previous completed H1 volume.
5. Missing canonical M1-derived volume context remains `NOT_EVALUABLE`; no raw H1 substitution, proxy, or invented threshold is used.
6. Preserved prior completed H1 history so the first 2025 H1 row can use the immediately preceding completed bar for `previous_close` when available.

## Governance invariants
- No new Murphy threshold was introduced.
- No futures-OI proxy was introduced for spot FX.
- No 2025 tuning, calibration, operator selection, or threshold selection was performed.
- This is evidence/producer validation, not a standalone profitability or live-trading authorization.

## Fresh-artifact boundary
The latest accessible verification proves the producer and CI are green. Exact PASS/FAIL/NOT_EVALUABLE counts from the CircleCI Run 5063 Murphy manifest are not reproduced here because the CircleCI artifact itself is not accessible through the GitHub connector. Do not reuse the older 2025 smoke-stream counts as if they were the fresh 5063 result.

## Next gate
Proceed to the shared Murphy breakout dependency audit (PF-B1) before implementing another breakout-dependent Murphy rule. Do not invent a decisive-break threshold. If the approved deterministic breakout contract cannot be established, keep the affected rule `NOT_EVALUABLE`.
