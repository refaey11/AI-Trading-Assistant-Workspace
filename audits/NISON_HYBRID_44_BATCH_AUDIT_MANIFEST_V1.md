# Nison Hybrid 44-Rule Batch Audit Manifest V1

Status: WORKING AUDIT MANIFEST — NOT A FREEZE RECORD
Date: 2026-08-16

## Scope

This manifest defines the audit shape for all 44 Nison rules. It intentionally does not claim that every rule is currently implemented or evaluable.

## Rule inventory

| Range | Batch treatment | Initial state |
|---|---|---|
| 0001–0025 | inventory + contract/definition audit | per current Nison registry |
| 0026 | evaluator/QA compatibility lane | READY_FOR_BACKTEST in current registry |
| 0027–0029 | inventory + contract/definition audit | per current Nison registry |
| 0030–0031 | evaluator/QA compatibility lane | READY_FOR_BACKTEST in current registry |
| 0032–0034 | inventory + contract/definition audit | per current Nison registry |
| 0035–0038 | proof batch: reuse existing evaluators/tests, then close remaining gates | READY_FOR_BACKTEST in current registry |
| 0039–0044 | inventory + contract/definition audit | per current Nison registry |

## Per-rule record

Each of the 44 rules must receive one record with:

- rule_id
- canonical source reference
- registry status
- implementation/evaluator reference
- clause inventory
- clause classification
- primitive/adapter compatibility
- evidence ledger reference
- deterministic tests
- availability evidence
- no-lookahead evidence
- historical QA 2016–2024
- 2025 isolation check
- provenance
- final decision
- blocking reason, if any

## Initial proof batch: 0035–0038

0035 Tasuki Gap:
- Existing V3 evaluator and 7/7 unit tests are present.
- Remaining semantic issue: source-locked operationalization of “about the same size”.
- Do not invent a body-size threshold.

0036 Gapping Play:
- Existing evaluator/tests are present.
- Qualitative clauses including sharp move, small real bodies, and congestion remain subject to source-bounded operationalization.
- Do not import arbitrary ADX/ATR thresholds.

0037 Side-by-Side:
- Existing evaluator/tests are present.
- “same open” and “similar body” remain semantic/compatibility gaps unless an approved comparator exists.
- Do not invent a comparator threshold.

0038 Windows:
- Existing structural evaluator and tests are present.
- Availability/replay evidence exists for the historical dataset.
- Sessionization and future-closure semantics remain explicit integration/freeze gates.
- Structural evaluator success alone is not sufficient for FROZEN.

## Decision vocabulary

FROZEN
QA_PENDING
READY_FOR_BACKTEST
PARTIAL
NOT_EVALUABLE
BLOCKED

## Batch rule

A rule's unresolved issue must not prevent independent rules from progressing. The manifest is evidence-first and fail-closed: missing evidence is recorded as a gap, not converted into a pass.
