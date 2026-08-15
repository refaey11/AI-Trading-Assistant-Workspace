# Murphy 0008 — Support Identity Audit V1

Status: AUDIT COMPLETE / GOVERNANCE GAP REMAINS
Date: 2026-08-15
Branch: audit/murphy-0008-pf-b1-v1

## Objective
Determine whether the existing project support_20 / support_50 / support_100 primitives can resolve the multiple-support-candidate problem for Murphy 0008 without inventing a new level-selection rule.

## Evidence found in Workspace
The Trading Rules / compatibility artifacts explicitly list support_20, support_50, and support_100 as existing Support/Resistance primitives. For MURPHY_0008 the registry records:
- required feature: support level + break_structure_down;
- status: PARTIAL;
- note: support_20/50/100 and break_structure_down exist, while the meaning of "decisively" still requires an approved definition.

The same compatibility mapping describes the support primitives as existing, but also says exact period/level selection must follow the rule wording.

## What was NOT found
The inspected Workspace/GitHub artifacts did not expose a verified deterministic definition for:
- how support_20 is calculated;
- how support_50 is calculated;
- how support_100 is calculated;
- which of the three is authoritative for MURPHY_0008;
- how to choose among multiple simultaneously valid support candidates;
- whether these are rolling-window extrema, pivot-derived levels, or another construction;
- their availability timestamps / lookahead contract for 0008.

GitHub repository code search also did not return an implementation artifact defining these fields. The local Workspace split contains the registry references, but the semantic implementation contract for the three named fields was not recovered from the inspected artifacts.

## Compatibility decision
The names support_20 / support_50 / support_100 prove that Support/Resistance primitives are part of the project vocabulary and compatibility mapping. They do NOT, by themselves, authorize selecting one for 0008 or define its level-selection semantics.

Therefore:
- Do not choose support_20 because it is the shortest period.
- Do not choose support_50 because it is a middle period.
- Do not choose support_100 because it is the longest period.
- Do not combine them by min/max/nearest/majority without an approved contract.
- Do not tune the selection against historical outcomes.

## Relationship to the current PF-H1 proposal
The prior 0008 no-cluster proposal uses a confirmed reaction trough from canonical PIVOT_SEQUENCE_V2 as a support-boundary candidate. That is a separate operationalization candidate and should not be silently replaced by support_20/50/100 merely because those names appear in the registry.

The new finding is that the project already has named S/R primitives, so PF-H1 cannot be declared universally "missing." Instead, the unresolved issue is the authoritative identity/selection contract for 0008.

## Decision
Support identity is now a separate governance gap:

1. Existing S/R primitive vocabulary: CONFIRMED.
2. Existing 0008 compatibility mapping: CONFIRMED.
3. Deterministic implementation semantics for support_20/50/100: NOT VERIFIED.
4. Authoritative 0008 support selection: NOT APPROVED.
5. New clustering/tolerance engine: NOT justified.

## Required next evidence
Before choosing a support identity for production 0008, recover one of:
- the implementation/schema that defines support_20/50/100;
- a contract/manifest describing their construction and availability;
- an existing evaluator that explicitly binds 0008 to one of these primitives.

If the source artifact cannot be recovered, retain the PIVOT_SEQUENCE_V2 reaction-trough candidate as a clearly labeled operationalization candidate, but do not freeze it as the canonical 0008 support identity without governance approval.

2025 remains OOS and is excluded from selection/tuning.
