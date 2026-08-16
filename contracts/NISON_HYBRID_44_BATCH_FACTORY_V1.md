# Nison Hybrid 44-Rule Batch Factory V1

Status: GOVERNANCE / ENGINEERING CONTRACT — NOT A RULE FREEZE
Date: 2026-08-16

## Purpose

Apply the project's proven hybrid rule-factory pattern to the 44 Nison candlestick rules without inventing source semantics, thresholds, tolerances, lookbacks, scoring weights, or direction logic.

Nison remains confirmation-only. A Nison evaluator may produce confirmation evidence, but it must not independently create market direction or a trading strategy.

## Source of truth

1. Nison canonical source/contracts and the existing Nison workspace artifacts are authoritative for Nison semantics.
2. The GitHub workspace supplies reusable engineering architecture, provenance, tests, contracts, and audit conventions.
3. Existing evaluators/primitives must be reused when compatible; they must not be rebuilt merely to fit the batch.
4. Historical outcomes may validate an already-closed semantic/operator contract, but may not define Nison semantics.
5. 2025 is OOS and must not be used for tuning, calibration, selection, optimization, or operator choice.

## Clause taxonomy

Every Nison rule is decomposed into atomic clauses:

- HARD_CANONICAL: execute the approved Nison contract literally.
- QUALITATIVE_MEASURABLE: use only an already-approved compatible project primitive through a documented adapter; no new threshold may be introduced.
- QUALITATIVE_UNMEASURABLE: remain NOT_EVALUABLE until an approved source-bounded operationalization exists.
- EVIDENCE_ONLY: retain source/context evidence without generating direction or a numeric score.

## Batch pipeline

44 Nison rules are ingested together and independently gated:

Canonical Rule Contract
→ Clause Decomposition
→ Clause Classification
→ Existing Primitive / Adapter Compatibility
→ Clause Evidence Ledger
→ Deterministic Evaluator
→ Availability / No-Lookahead
→ Unit Tests
→ Historical QA 2016–2024
→ Governance Gate
→ FROZEN / QA_PENDING / NOT_EVALUABLE / BLOCKED

One blocked or unevaluable rule must not stop unrelated rules in the batch.

## No hidden scoring

The factory must not convert partial clause success into a passing score. A required unevaluable clause cannot be compensated for by other clauses.

## Required manifest fields

Each rule record must preserve:

- rule_id
- canonical_source_reference
- rule_status
- clause_id
- clause_type
- canonical_text_reference
- operator_source
- primitive_id
- adapter_id
- measurability_status
- evaluator_status
- availability_status
- no_lookahead_status
- deterministic_test_status
- historical_qa_status
- provenance
- decision
- blocking_reason

## Reuse-first policy

Before implementing anything new, inspect the existing Nison workspace for:

- canonical contracts
- evaluators
- primitives
- adapters
- unit tests
- replay/QA artifacts
- availability/no-lookahead evidence

Existing compatible components are reused. Missing components are recorded as gaps rather than silently replaced with invented semantics.

## Freeze gate

A Nison rule may be marked FROZEN only when:

1. canonical source is identified;
2. every required clause has an approved operational/evidence path;
3. no invented semantic threshold exists;
4. compatible upstream primitives are reused;
5. deterministic tests pass;
6. availability/no-lookahead tests pass;
7. provenance is complete;
8. Historical QA is completed on 2016–2024 only;
9. 2025 remains untouched as OOS;
10. governance accepts the final record;
11. Nison output remains confirmation evidence and does not become independent direction.

## Initial proof batch

Rules 0035–0038 are the initial proof batch because existing evaluator/test artifacts are already present. Their existing gaps must remain explicit and must not be hidden by batch code generation.

The batch factory is an implementation accelerator and audit mechanism; it is not an auto-freeze mechanism.
