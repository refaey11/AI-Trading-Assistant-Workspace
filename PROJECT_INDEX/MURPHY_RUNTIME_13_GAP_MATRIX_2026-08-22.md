# Murphy Runtime Gap Matrix — 2026-08-22

## Scope
The 13 Murphy rules that are frozen/closed but are not yet proven as Runtime Integrated. This audit distinguishes frozen knowledge from executable runtime wiring.

## Runtime proof standard
A rule is counted as Runtime only when the current workspace provides evidence of:
1. evaluator/adapter source;
2. runtime entry-point/registry wiring for the rule; and
3. executable tests/integration evidence.
Presence of a frozen artifact, workflow, or historical QA alone is not sufficient.

## Current confirmed Runtime baseline
22 rules are currently recorded as Runtime Implemented in the live state. See `PROJECT_STATE/CURRENT_STATE_INDEX_2026-08-22.md`.

## 13-rule matrix
| Rule | Frozen | Evaluator/Adapter | Runtime Entry/Registry | Tests/Integration | Runtime verdict | Immediate gap |
|---|---|---|---|---|---|---|
| 0006 | YES | Evidence/workflow assets present; no verified current evaluator payload in live tree | NOT_PROVEN | Deterministic workflow exists | PARTIAL / NOT_PROVEN | Recover readable evaluator/adapter payload and prove unified runtime wiring |
| 0007 | YES | Evidence/workflow assets present; no verified current evaluator payload in live tree | NOT_PROVEN | Deterministic workflow exists | PARTIAL / NOT_PROVEN | Same as 0006 |
| 0008 | YES | Not proven as readable evaluator | NOT_PROVEN | Historical QA exists | BLOCKED | Approved decisive-break operational definition / PF-B1 binding, then evaluator + runtime |
| 0025 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Historical/freeze evidence exists | NOT_PROVEN | Recover canonical evaluator/adapter and runtime wiring |
| 0026 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Historical/freeze evidence exists | NOT_PROVEN | Same as 0025 |
| 0030 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Freeze evidence exists | NOT_PROVEN | Recover readable evaluator and entry-point proof |
| 0031 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Freeze evidence exists | NOT_PROVEN | Same as 0030 |
| 0032 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Freeze evidence exists | NOT_PROVEN | Same as 0030 |
| 0033 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Local freeze/replay evidence exists | NOT_PROVEN | Recover evaluator/adapter and repository runtime wiring |
| 0047 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Closure evidence exists; occurrence-count discrepancy is preserved | NOT_PROVEN | Recover evaluator and resolve/record archival discrepancy before runtime promotion |
| 0048 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Closure evidence exists | NOT_PROVEN | Recover evaluator/entry point/tests |
| 0049 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Closure evidence exists | NOT_PROVEN | Recover evaluator/entry point/tests |
| 0051 | YES | No verified evaluator entry in current evaluator inventory | NOT_PROVEN | Process-gate closure/test evidence exists | NOT_PROVEN | Recover evaluator/entry point; validate process-gate runtime behavior |

## Key evidence
- Current runtime audit lists verified evaluator source inventory for 0003/0004, 0021/0023, 0027/0029, and 0050, and explicitly warns that evaluator inventory alone is not sufficient to mark runtime PASS. `AUDITS/MURPHY_RUNTIME_BATCH_EXECUTION_STATUS_V1.md`.
- 0006/0007 have dedicated deterministic GitHub Actions workflows, but that is deterministic audit evidence, not proof of unified runtime routing.
- 0008 is explicitly blocked pending an approved operational definition for `decisively broken`.
- 0018/0019 are excluded from this gap list because their current workspace contains evaluator, runtime entry-point, and tests.
- 0029 is excluded from this gap list because its runtime adapter and tests are present and its current historical replay matches the existing 2016-2024 status.

## Decision
Keep the official Runtime count at **22/35**. Do not promote any of these 13 rules based solely on frozen status, historical QA, or CI workflow presence.

## Highest-leverage next targets
1. 0006/0007 — closest to Runtime because deterministic workflows and evidence adapters exist.
2. 0008 — blocked by one explicit semantic/operator contract.
3. 0030–0033 — recover readable evaluator/entry-point payloads in a batch.
4. 0047–0049 and 0051 — recover the closure-era evaluator/runtime artifacts as one batch.
