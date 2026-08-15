# Rule Acceptance Gate V1

Date: 2026-08-16
Status: PROJECT GOVERNANCE POLICY — PROPOSAL

## Purpose
Prevent one ambiguous rule from blocking the entire Decision Brain while preventing weak rules from entering production as if they were validated.

## Rule states
### FROZEN
A rule may be used as production Decision Brain evidence only when its source meaning, contract, evaluator, tests, historical replay, availability/no-lookahead, and governance requirements are evidenced.

### CANDIDATE
The rule is retained and may be researched or used in non-production diagnostics, but it cannot independently trigger a production decision. Typical causes: unresolved operationalization, incomplete historical validation, or source ambiguity.

### BLOCKED / NOT_EVALUABLE
The rule cannot currently be evaluated without an unsupported assumption, missing data, or unresolved contract. It is isolated from production and does not block unrelated rules.

### FAIL
A defined rule was tested and violated an explicit acceptance criterion. It must be repaired or rejected; it is not silently downgraded to pass.

## Governance principle
A rule-level failure or block does not block unrelated rules or modules. Only an integration-level dependency that is required by the Decision Brain architecture can block the corresponding integration gate.

## No forced completion
The project does NOT require all registered rules to become FROZEN. It requires every rule used in production to have an explicit evidence state and provenance.

## Production boundary
Only FROZEN rules may contribute production-grade evidence. CANDIDATE and BLOCKED rules must remain visibly tagged and cannot independently create an entry decision.

## 0030–0032 disposition
After the current replay and policy work:
- 0030–0032 remain on their proposal branch until their remaining governance gates are complete.
- If a remaining gate cannot be satisfied without inventing source methodology, the affected rule(s) become CANDIDATE or BLOCKED and the project proceeds to the next rule batch.

## Batch operating rule
For each batch: compatibility audit → evaluator → focused tests → historical QA → no-lookahead/availability → sensitivity where applicable → governance classification → move on.

Do not repeatedly reopen already-closed gates unless new evidence invalidates them.
