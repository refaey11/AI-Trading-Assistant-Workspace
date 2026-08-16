# Murphy Hybrid Rule Evaluator Architecture V1

Status: GOVERNANCE / ENGINEERING CONTRACT — NOT A RULE FREEZE
Date: 2026-08-16

## Purpose

Provide one reusable architecture for converting the remaining Murphy rules into deterministic evaluators without forcing qualitative source language into invented numeric thresholds.

The architecture is intentionally hybrid:

1. **Hard / Canonical clauses** are executed literally from an approved canonical contract.
2. **Qualitative clauses** are first classified as either measurable through an already-approved project primitive or not yet measurable.
3. A qualitative clause may become deterministic only through a source-bounded adapter to an existing approved primitive or through a separately approved contract. It must never acquire an arbitrary threshold merely to make the rule executable.
4. If a required clause cannot be evaluated without invention or unavailable evidence, the rule returns `NOT_EVALUABLE` / `BLOCKED` according to the project gate.

## Non-negotiable governance

- Do not rebuild existing canonical primitives.
- Do not copy semantics from one Murphy rule into another.
- Do not invent thresholds, tolerances, lookbacks, percentages, ATR/pip distances, or scoring weights.
- Do not use historical outcomes to define source semantics.
- 2025 is OOS and is excluded from tuning, selection, calibration, optimization, or operator choice.
- A qualitative phrase is not automatically a numeric rule.
- A rule may only advance when every required clause has an auditable evidence path.
- `NOT_EVALUABLE` is a valid terminal state when the required evidence path is absent.

## Clause taxonomy

Every rule contract is decomposed into atomic clauses with one of these types:

### HARD_CANONICAL

The source/approved contract specifies a sufficiently explicit condition. The evaluator executes it literally. No interpretation layer may change its meaning.

### QUALITATIVE_MEASURABLE

The source wording is qualitative, but the project already contains an approved primitive whose semantics are explicitly compatible. The adapter must document the mapping and may expose only the primitive's existing output. It may not introduce a new threshold.

### QUALITATIVE_UNMEASURABLE

The source wording remains qualitative and no compatible approved primitive exists. The clause is `NOT_EVALUABLE` until governance approves a source-bounded operationalization.

### EVIDENCE_ONLY

The clause records source evidence/context but does not generate a trading direction or numeric score.

## Evaluation pipeline

```text
Canonical Rule Contract
        ↓
Clause Decomposer
        ↓
┌───────────────────────┐
│ HARD_CANONICAL        │ → literal evaluator
│ QUALITATIVE_MEASURABLE│ → approved primitive adapter
│ QUALITATIVE_UNMEASURABLE│ → NOT_EVALUABLE
│ EVIDENCE_ONLY         │ → evidence record
└───────────────────────┘
        ↓
Clause Evidence Ledger
        ↓
Rule Acceptance Gate
        ↓
PASS / FAIL / NOT_EVALUABLE / BLOCKED
```

## No hidden scoring

The architecture does **not** create a fuzzy score such as "7/10 conditions met". A rule cannot pass by compensating for an unevaluable required condition with other conditions.

If the canonical rule requires a clause, that clause must pass its own gate.

## Separation of concerns

- **Rule Contract** = what Murphy requires.
- **Primitive** = how an already-approved measurable concept is represented.
- **Adapter** = the compatibility mapping between the rule clause and the primitive.
- **Evaluator** = deterministic execution of the approved contract.
- **Decision Brain** = downstream decision process; the rule evaluator itself does not become a trading strategy.
- **Historical QA** = validation after semantic/operator closure; never a source of rule definition.

## Batch factory behavior

The factory can ingest the remaining rule contracts in one batch. It should generate an audit/evaluator manifest for every rule, but it must not auto-freeze a rule merely because code generation succeeds.

For each rule:

```text
contract found?
  no → BLOCKED
  yes
   ↓
clauses decomposed?
  no → BLOCKED
  yes
   ↓
all required clauses have approved evidence paths?
  no → NOT_EVALUABLE / BLOCKED
  yes
   ↓
existing primitives reused where compatible?
  no → compatibility audit
  yes
   ↓
deterministic tests + no-lookahead tests
   ↓
QA queue
```

## Required evidence ledger fields

Each clause record must preserve:

- `rule_id`
- `clause_id`
- `clause_type`
- `canonical_text_reference`
- `operator_source`
- `primitive_id` (nullable)
- `adapter_id` (nullable)
- `measurability_status`
- `availability_status`
- `no_lookahead_status`
- `test_status`
- `decision`
- `provenance`

## Freeze gate

A rule may be marked `FROZEN` only when:

1. canonical source contract is identified;
2. every required clause has an approved operational path;
3. no invented semantic threshold exists;
4. upstream primitives are compatible and reused;
5. deterministic unit tests pass;
6. availability/no-lookahead tests pass;
7. provenance is complete;
8. historical QA is performed on the permitted in-sample period (2016–2024 for this project);
9. 2025 remains untouched as OOS;
10. governance review accepts the final record.

This architecture accelerates implementation by standardizing the mechanics while preserving rule-specific semantics.
