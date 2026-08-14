# Murphy 0008 — PF-B1 Governance Reconciliation V1

Date: 2026-08-15
Status: GOVERNANCE RECONCILIATION COMPLETE / PF-B1 DECISIVE-BREAK APPROVAL STILL OPEN
Branch: audit/murphy-0008-pf-b1-v1

## 1. New finding from full Workspace archive inspection

The reconstructed GBPUSD Rule Evaluator V2 workspace contains an existing generic feature mapping for Rule 0008:

`support level + break_structure_down`

The exact Murphy mapping worksheet records the intended operator concept as:

`price breaks below support with the project's approved decisive-break condition`

and marks Rule 0008 as `PARTIAL`, explicitly stating that support_20/50/100 and break_structure_down exist but that `decisively` still needs an approved definition.

This is important: the project already has a generic downside-break feature, so a new bespoke breakout engine is NOT justified by the evidence found so far.

## 2. What this generic feature proves

It proves that a reusable market-structure break signal exists in the workspace architecture.

It does NOT prove that `break_structure_down` is an approved Murphy-0008 decisive-break operator.

The exact mapping remains conditional on an approved decisive-break definition. Therefore the feature can be treated as an upstream candidate/input, not as a frozen PF-B1 contract.

## 3. Source boundary

The Murphy source supports support/resistance role reversal and meaningful/decisive penetration. The source material also discusses closing behavior, price filters and time filters. However, the project evidence does not establish one project-specific numeric decisive-break threshold for 0008.

Therefore this reconciliation does NOT select:
- 3%
- two consecutive closes
- ATR
- pips
- arbitrary percentage
- arbitrary lookback
- hidden tolerance

## 4. PF-B1 compatibility decision

REUSE PATH: YES, conditionally.

The generic `break_structure_down` feature should be reused as the upstream break candidate for 0008 rather than creating a duplicate break engine.

GOVERNANCE STATUS: OPEN.

The remaining missing decision is the definition of when the generic break becomes `decisive` and therefore eligible for PF-B1 `CONFIRMED` status.

Until that definition is explicitly approved, PF-B1 must preserve:

`status = NOT_EVALUABLE` when decisive-break evidence cannot be established deterministically.

## 5. Required PF-B1 contract fields

The smallest contract still needs to bind:

1. boundary/level identity;
2. downside break direction;
3. completed-bar evidence used by the break feature;
4. decisive-break approval state;
5. breakout timestamp;
6. availability timestamp;
7. `CONFIRMED / NOT_CONFIRMED / NOT_EVALUABLE` state.

No new numeric threshold is introduced by this document.

## 6. Decision

Do NOT implement the 0008 evaluator yet.

Do NOT tune a threshold from historical data.

Do NOT use 2025.

Do reuse the existing `break_structure_down` architecture once the decisive-break governance is closed.

Next gate: approve the smallest source-faithful PF-B1 decisive-break contract, then audit PF-H1 and implement the 0008 role-reversal layer.

## 7. Evidence

- `MURPHY_0008_PF_B1_COMPATIBILITY_AUDIT_V1.md`
- `MURPHY_0008_CHAT_HANDOFF_MASTER_V1.docx`
- `MURPHY_0013_0020_PRIMITIVE_CLOSURE_PROPOSAL_V1.md`
- `MURPHY_PATTERN_PRIMITIVES_IMPLEMENTATION_SPEC_V1.md`
- `MURPHY_0006_TO_0010_EXACT_MAPPING_V1.csv` from the reconstructed GBPUSD Rule Evaluator V2 workspace
- Murphy Chapter 4 source archive: `01_John_Murphy_Technical_Analysis(6).zip`

## 8. Freeze rule

This document is a governance reconciliation only. It does not freeze PF-B1 or 0008. Production requires an approved operator, deterministic tests, availability/no-lookahead validation, historical QA, provenance, and a freeze manifest.
