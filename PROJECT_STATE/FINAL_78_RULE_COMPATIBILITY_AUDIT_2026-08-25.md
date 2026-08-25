# Final 78-Rule Compatibility Audit — 2026-08-25

## Scope
Audit the current 2025 Final Decision Event Stream against the frozen Decision Brain Rule Allowlist before any profitability rerun.

## Frozen governance
The frozen allowlist declares 78 verified runtime rules: 44 Nison + 34 Murphy. It is deny-by-default; unknown or non-allowlisted rule IDs must be rejected. MURPHY_0008 is explicitly blocked. No change to the allowlist is authorized by this audit.

## Actual Final Event Stream observed
Input: `FINAL_2025_DECISION_EVENTS.csv` from the successful CircleCI final-evaluation artifact.

- Events: 6,225
- EXECUTABLE: 0
- NO_TRADE: 6,225
- Final trade file: empty (1 byte)
- Reason on all events: `RULE_ALLOWLIST_REJECT`
- Actual Murphy source rule IDs: `MURPHY_0021`, `MURPHY_0022`, `MURPHY_0023`
- Actual Nison source rule ID: synthetic sentinel `NISON_NONE`

## Root cause
The frozen allowlist itself is correct and contains MURPHY_0021/0022/0023 and all 44 Nison rules. The final event producer was passing `NISON_NONE` as a source rule ID when no directionally usable Nison row existed. `NISON_NONE` is not an allowlisted rule ID, so the deny-by-default evaluator correctly returned `RULE_ALLOWLIST_REJECT` for every timestamp.

The full Nison evidence contains all 44 rule IDs, but every observed direction value in the uploaded 2025 evidence is `UNKNOWN`; therefore the candidate builder could not select a directional Nison rule and emitted the synthetic sentinel.

## Murphy coverage note
The final candidate stream currently carries only Murphy 0021/0022/0023 into the decision event, not all 34 Murphy runtime rules. This is an evidence-wiring limitation of the current final OOS path and must not be described as all 34 Murphy rules being active in the final decision stream.

## Corrective action
Patch only provenance/wiring: omit the synthetic `NISON_NONE` sentinel from `source_rule_ids`. Preserve the actual aggregate Nison evidence and allow the frozen allowlist to validate only real, allowlisted rule IDs. No trading rule, threshold, direction logic, OOS data, or risk protocol is changed.

Commit: `e8092c3dd5f3c4ae1b5855973a17e3847fe4c90f`

## Next gate
Rerun the same 2025 OOS pipeline. Then verify:
1. `RULE_ALLOWLIST_REJECT` disappears for provenance-only reasons.
2. Final events contain only real allowlisted rule IDs.
3. Murphy/Nison/TIZ/Risk semantics remain unchanged.
4. Only after an executable event stream exists, calculate and record official 2025 P&L metrics.

2025 remains evaluation-only; no tuning or threshold selection is permitted.