# AI Trading Assistant — Murphy 0008 Checkpoint

Date: 2026-08-15
Branch: audit/murphy-0008-pf-b1-v1
Status: CHECKPOINT / CONTINUATION POINT — NOT PRODUCTION FROZEN

## Purpose
Preserve the exact project state reached in the current 0008 investigation so future work resumes from this point instead of restarting the audit.

## Confirmed
- Murphy Rule 0008 semantic identity is resolved: support -> decisive/significant downside break -> later rally/retest -> former support becomes resistance.
- `break_structure_down` exists as an existing project primitive and must be reused; no duplicate breakout engine is authorized.
- `PIVOT_SEQUENCE_V2` is canonical and has been verified for chronology/availability/no-lookahead behavior in the current investigation.
- PF-B1 interface is compatible as a policy-injection boundary: raw break is distinct from decisive confirmation.
- A deterministic PF-B1 candidate fixture pack exists; candidate logic passed the synthetic invariants, but this does not constitute Murphy fidelity or production approval.
- The project explicitly forbids selecting 1%, 3%, two consecutive closes, ATR, pips, arbitrary tolerance, arbitrary lookback, or historical-performance-derived thresholds as a silent 0008 default.
- 2025 remains OOS and must not be used for policy selection or tuning.

## Open governance blockers
### 1. PF-B1 decisive-break policy
No production-frozen, source-authorized deterministic policy has yet been approved for translating Murphy's "decisive/significant" downside break into a 0008 confirmation operator.

Current contract proposal: `audits/MURPHY_0008_PF_B1_POLICY_INJECTION_CONTRACT_V1.md`.
Current state: interface compatible; decisive policy OPEN.

### 2. PF-H1 / Support Identity
The project vocabulary contains `support_20`, `support_50`, and `support_100`, but their authoritative producer/calculation/availability semantics and the rule-specific selection contract for 0008 have not been verified from recovered implementation artifacts.

Do NOT select 20/50/100 by name, period length, historical performance, or convenience.
Do NOT invent a clustering/equality tolerance.
A confirmed PIVOT_SEQUENCE_V2 reaction-trough remains an operationalization candidate only, not a production-frozen canonical 0008 support identity.

## Current 0008 state
- Source semantics: RESOLVED
- Existing breakout primitive: AVAILABLE
- Pivot upstream: VERIFIED/CANONICAL
- PF-B1 interface: COMPATIBLE
- PF-B1 decisive policy: OPEN
- Support identity contract: OPEN
- 0008 evaluator: BLOCKED FOR PRODUCTION
- 2016-2024 QA: NOT YET A POLICY-SELECTION STEP; only after governance is approved
- 2025: OOS / LOCKED
- Production freeze: NOT APPROVED

## Next action
Resume with Support Identity Recovery:
1. Inspect recovered Feature Engineering V2/V1 Higher-TF artifacts and related manifests/contracts.
2. Trace `support_20`, `support_50`, `support_100` from output -> manifest/schema -> producer -> calculation -> timeframe -> availability -> consumers.
3. Compare any recovered producer against Murphy 0008 wording and existing project governance.
4. If authoritative evidence is recovered, bind 0008 explicitly.
5. If not recovered, record the exact missing artifact/contract and keep 0008 `NOT_EVALUABLE` rather than inventing a rule.

## Important continuity rule
Do not restart the project-wide audit from scratch. Do not rebuild existing knowledge. Continue from this checkpoint and preserve compatibility/provenance decisions already established.
