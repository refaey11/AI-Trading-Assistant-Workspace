# 102 Rule Registry Reconciliation V1

Date: 2026-08-12

## Authoritative registry inspected

Source archive: `AI_Trading_Assistant_TRADING_RULES_V2.zip`
Artifact: `02_Trading_Rules_V2/MASTER_TRADING_RULES_V2.json`

This registry contains exactly 102 rules:
- 51 Murphy
- 44 Steve Nison
- 7 Trading in the Zone

Registry status:
- 23 `READY_FOR_BACKTEST`
- 79 `INCOMPLETE_NEEDS_RULE_DEFINITION`

Important: all 102 registry entries currently have `testing.status = UNTESTED` in the registry. Therefore READY_FOR_BACKTEST means structurally ready for the next test/evaluator stage, not tested or frozen.

## 23 rules currently READY_FOR_BACKTEST in the registry

### Murphy — 16
MURPHY_0008
MURPHY_0009
MURPHY_0010
MURPHY_0013
MURPHY_0014
MURPHY_0015
MURPHY_0016
MURPHY_0017
MURPHY_0018
MURPHY_0019
MURPHY_0020
MURPHY_0025
MURPHY_0026
MURPHY_0028
MURPHY_0029
MURPHY_0047

### Steve Nison — 7
CANDLE_RULE_0026
CANDLE_RULE_0030
CANDLE_RULE_0031
CANDLE_RULE_0035
CANDLE_RULE_0036
CANDLE_RULE_0037
CANDLE_RULE_0038

### Trading in the Zone — 0

## Registry vs existing evaluator artifacts — reconciliation required

The registry is not synchronized with all evaluator work preserved in the Workspace:

- MURPHY_0003–0004: registry says `INCOMPLETE_NEEDS_RULE_DEFINITION`, while V2 evaluator/tests exist. They remain NOT FROZEN because provenance/semantics are unresolved.
- MURPHY_0021–0023: registry says `INCOMPLETE_NEEDS_RULE_DEFINITION`, while evaluator/unit-test/historical artifacts exist. These need compatibility reconciliation before any status promotion.
- MURPHY_0027: registry says `INCOMPLETE_NEEDS_RULE_DEFINITION`; existing evaluator intentionally blocks pending exact regime operator.
- MURPHY_0028–0029: registry says `READY_FOR_BACKTEST`; existing evaluator/unit-test artifacts also exist. These are the first clean candidates for QA closure.
- MURPHY_0050: registry says `INCOMPLETE_NEEDS_RULE_DEFINITION`; structural evidence/evaluator artifact exists but current state is NOT_EVALUABLE.

This discrepancy is a **registry synchronization/lineage issue**, not permission to overwrite the source registry. Existing evaluator artifacts must be audited against their rule entries and only then can the registry/closure status be updated through the project's controlled process.

## Immediate execution priority

The project should stop cycling through unresolvable rules and work the rules that the authoritative registry already marks `READY_FOR_BACKTEST`:

1. Murphy 0008–0010, 0013–0020, 0025–0026, 0028–0029, 0047.
2. Nison CANDLE_RULE_0026, 0030, 0031, 0035–0038.

For each READY_FOR_BACKTEST rule:

**Source → exact operator/logic → existing feature compatibility → evaluator → unit tests → historical QA → freeze**

No new thresholds/operators are to be invented. Existing modules must be reused after compatibility audit.

## Deferred rules

The remaining 79 rules are not ready for test closure according to the registry because they have missing fields/definitions. They remain in the closure queue; do not fabricate confirmation, entry, invalidation, or other missing fields.

## Global controls

- 2025 remains OOS and is never used for tuning/selection.
- Decision Brain V1/V1.1 already exists; do not rebuild.
- Rule Adapter is normalization only; do not copy the 102 registry rules into the Brain.
- Murphy = technical context; Nison = confirmation; Trading in the Zone = process gate; Similarity = historical evidence; Risk = hard gate.
