# Murphy 0008 PF-B1 Candidate — Deterministic Fixture Pack V1

Status: TEST FIXTURES / GOVERNANCE REVIEW — NOT PRODUCTION FROZEN
Date: 2026-08-15
Branch: audit/murphy-0008-pf-b1-v1

## Purpose
Test the smallest current PF-B1 operational candidate without silently promoting it to a Murphy production rule.

## Candidate under test
Input: confirmed support boundary from PF-H1 / PIVOT_SEQUENCE_V2.

Candidate decisive-break evidence:
- a raw downside crossing of the support boundary is observed on completed data;
- a subsequently confirmed LOW/pivot structure is formed below the boundary;
- the decisive-confirmation timestamp is the first timestamp at which that downstream pivot evidence is actually available;
- if the downstream confirmation is not available, decisive status is NOT_EVALUABLE.

This is a PROJECT OPERATIONALIZATION CANDIDATE, not a literal Murphy quote and not a frozen contract.

## Fixtures

### F01 — No break
Support = 100.00.
Completed closes remain >= 100.00.
Expected:
- raw_break = false
- decisive_confirmation = NOT_CONFIRMED / no event

### F02 — Intrabar penetration only
Support = 100.00.
A candle low prints below 100.00 but closes back above 100.00; no confirmed downstream LOW exists.
Expected:
- raw_break may be recorded only if the raw-break definition accepts completed-bar low penetration;
- decisive_confirmation = NOT_EVALUABLE until downstream confirmation exists;
- do not call the intrabar poke decisive by itself.

### F03 — Raw downside break, confirmation pending
Support = 100.00.
A completed candle closes below 100.00.
A downstream LOW has not yet reached its PIVOT_SEQUENCE_V2 availability timestamp.
Expected:
- raw_break_timestamp = break candle timestamp;
- decisive_confirmation = NOT_EVALUABLE;
- no retroactive confirmation.

### F04 — Candidate decisive confirmation becomes available
Support = 100.00.
Raw downside break occurs first.
A LOW pivot below 100.00 later becomes confirmed under the existing PIVOT_SEQUENCE_V2 availability contract.
Expected:
- raw_break_timestamp < decisive_confirmation_timestamp;
- decisive_confirmation_timestamp = pivot availability timestamp;
- status = candidate CONFIRMED only within this experimental fixture.

### F05 — Lookahead guard
Construct data where the future bars would eventually confirm a LOW below support, but inspect the series before the pivot availability timestamp.
Expected:
- no decisive confirmation before the availability timestamp;
- the future-confirmed pivot cannot be used early.

### F06 — Boundary unavailable
No confirmed support boundary is available.
Expected:
- PF-H1 boundary = NOT_EVALUABLE;
- PF-B1 decisive confirmation = NOT_EVALUABLE;
- no fabricated boundary.

### F07 — Confirmation not below boundary
Raw break occurs, but the later confirmed LOW is at or above the support boundary.
Expected:
- candidate decisive confirmation = NOT_CONFIRMED;
- do not infer decisive downside continuation from unrelated evidence.

### F08 — Chronology violation
Downstream pivot evidence is timestamped before the raw break.
Expected:
- fixture invalid / reject;
- decisive confirmation cannot precede the raw break event.

### F09 — Retest before decisive confirmation
Price returns toward the broken support before the candidate downstream pivot becomes available.
Expected:
- retest evidence remains separate;
- it must not be used to manufacture an earlier decisive confirmation.

### F10 — Missing/ambiguous evidence
Required timestamps or pivot availability are missing/ambiguous.
Expected:
- NOT_EVALUABLE;
- no fallback threshold.

## Invariants
1. No future information may be used before its availability timestamp.
2. Raw break and decisive confirmation are distinct events.
3. Decisive confirmation cannot precede raw break.
4. No 1%, 3%, two-day, ATR, pip, arbitrary tolerance, or arbitrary lookback is introduced by these fixtures.
5. 2025 is excluded from policy selection and tuning.
6. Historical Memory is evidence-only and cannot define the operator.
7. A failed fixture means the candidate remains unapproved; it does not justify tuning the candidate to historical outcomes.

## Acceptance gate
Passing these fixtures only establishes deterministic behavior of the candidate. It does NOT establish Murphy fidelity or production approval.

Next required gates:
- source/governance review;
- deterministic implementation tests;
- 2016–2024 QA;
- no-lookahead audit;
- production-freeze review.
