# Murphy PF-B1 Current Compatibility Reconciliation — 2026-08-23

## Status
GOVERNANCE OPEN / NO PRODUCTION-FROZEN DECISIVE-BREAK CONTRACT PROVEN

## Why this audit was reopened
The fresh Murphy 0021 2025 producer is now green on the governed 2025 CI path. The next dependency family must therefore be selected by compatibility evidence, not by historical counts or convenience.

## Existing evidence reviewed
- `audits/MURPHY_0008_PF_B1_COMPATIBILITY_AUDIT_V1.md` — existing PF-B1 compatibility audit; status remains governance open and evaluator not started.
- `PF_B1_GOVERNANCE_PROPOSAL_V1.md` — PF-B1 is a proposal, not production frozen.
- `MURPHY_0013_0020_PRIMITIVE_CLOSURE_PROPOSAL_V1.md` — PF-B1 is the shared breakout primitive intended for 0013–0020.
- `MURPHY_0013_0020_PATTERN_DERIVED_FEATURE_CONTRACT_V1.md` — breakout confirmation is a shared downstream primitive.
- `MURPHY_0008_CHAT_HANDOFF_MASTER_V1` / `AI_TRADING_ASSISTANT_MURPHY_0008_FULL_HANDOFF_V2` — explicitly require PF-B1 governance closure before 0008 evaluator implementation.
- `MURPHY_12_FROZEN_CONTINUITY_BACKUP_V1.json` — records a historical-status conflict for 0008: a later canonical list says production frozen, while preserved source-era PF-B1 evidence still says the decisive-break contract was not approved. The conflict must be preserved and reconciled, not silently erased.
- `CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md` — 0018/0019 governance/source semantics are frozen, but runtime binding remains pending; runtime count is not promoted until executable integration is verified.

## Compatibility conclusion
No independently proven, production-frozen PF-B1 decisive-break implementation was found in the accessible current evidence.

Murphy source material supports the existence of decisive breakout/penetration filtering policy families, including price-filter and two-successive-close concepts, but the project evidence does not authorize selecting one universal numerical threshold or time rule for 0008/other breakout consumers.

Therefore:
- Do not choose 3%, 1%, 2-day, ATR, pips, lookback, or an arbitrary tolerance as a project-wide decisive-break rule.
- Do not build a bespoke 0008 breakout engine that bypasses PF-B1.
- Do not use 2025 to select or tune the breakout operator.
- If decisive-break evidence is not deterministically available under an approved contract, the downstream rule must remain `NOT_EVALUABLE`.

## Dependency map
`PF-H1 / approved support level`
→ `PF-B1 / approved decisive downside break`
→ `later rally/retest`
→ `role-reversal evidence`
→ `MURPHY_0008 adapter/evaluator`

The same shared PF-B1 dependency is relevant to the 0013–0020 continuation-pattern family where breakout confirmation is a required downstream primitive.

## Next gate
1. Reconcile the current canonical status of 0008 against the preserved PF-B1 provenance conflict.
2. Determine whether there is a newer approved governance record not represented in the older handoff/proposal snapshots.
3. If no approved deterministic breakout contract exists, produce the smallest governance decision record that explicitly keeps PF-B1 `NOT_EVALUABLE` rather than inventing a threshold.
4. Only after PF-B1 governance is resolved, audit PF-H1 and then implement the smallest missing downstream evaluator.

## OOS rule
2025 remains strictly OOS. No 2025 result or pass/fail distribution may be used to choose the breakout policy.
