# Murphy 39-Rule Batch Audit V1

Date: 2026-08-16
Status: BATCH AUDIT INITIALIZED — NO RULE SEMANTICS CHANGED

## Scope

Run one evidence-first compatibility triage across the 39 Murphy rules that are not in the current canonical frozen/closed set.

The current canonical `START_HERE_FOR_ANY_CHAT.md` states that 12/51 rules are frozen/closed and explicitly says not to reopen them. Those 12 are excluded from this queue.

## Protected / excluded frozen set

0003, 0004, 0006, 0007, 0008, 0021, 0022, 0023, 0025, 0026, 0028, 0029

## Batch queue — 39 remaining rules

0001, 0002, 0005,
0009, 0010, 0011, 0012, 0013, 0014, 0015, 0016, 0017, 0018, 0019, 0020,
0024, 0027,
0030, 0031, 0032, 0033, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0046, 0047, 0048, 0049, 0050, 0051

## Required batch workflow

For every rule independently:

`source → provenance/contract → compatibility audit → existing primitive → evaluator/adapter → deterministic tests → 2016–2024 QA → availability/no-lookahead → freeze review`

A rule with a blocker must be marked `BLOCKED` or `NOT_EVALUABLE`; it must not block processing of the other rules.

## Shared accelerators

Where compatible, reuse existing canonical infrastructure rather than rebuilding it:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- shared breakout/confirmation architecture where its contract is explicitly compatible
- existing evaluator/adapter contracts
- evidence-first repository collector/reducer

Reuse means interface/architecture compatibility only. It does not transfer rule-specific semantics from one Murphy rule to another.

## Mandatory gates

1. Never reopen the protected 12 merely to populate this batch.
2. No invented operator, threshold, tolerance, timeframe, lookback, proxy, or semantic shortcut.
3. 2025 is OOS and excluded from tuning, selection, calibration, optimization, and implementation selection.
4. Historical results are validation evidence, never a source for inventing missing semantics.
5. Missing or ambiguous evidence → `NOT_EVALUABLE`.
6. Contradictory authoritative evidence → `CONFLICT` pending governance resolution.
7. A passing deterministic test is not a production freeze by itself.

## Batch output contract

Each rule must receive one machine-readable status record with at least:
- rule_id
- canonical_status
- source_status
- provenance_status
- compatibility_status
- primitive_status
- evaluator_status
- deterministic_test_status
- historical_qa_status
- availability_no_lookahead_status
- freeze_status
- blockers
- evidence_refs
- last_verified_commit

## Initial classification policy

This file intentionally does not guess the state of any of the 39 rules. The first batch pass must collect authoritative evidence from the repository and reduce it deterministically. The output may contain `FROZEN`, `QA_PASS`, `FREEZE_CANDIDATE`, `TECHNICAL_BLOCKED`, `SOURCE_BLOCKED`, `NOT_EVALUABLE`, `CONFLICT`, or `UNVERIFIED` as supported by evidence.

## Success criterion

The batch audit succeeds when all 39 rules have an evidence-backed status and next action, without modifying any protected frozen rule and without introducing new Murphy semantics.
