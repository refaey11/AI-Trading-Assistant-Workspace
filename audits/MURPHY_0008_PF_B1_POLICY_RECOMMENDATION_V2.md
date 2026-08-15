# Murphy 0008 — PF-B1 Policy Recommendation V2

Status: CANDIDATE / NOT FROZEN
Date: 2026-08-15

## Decision
The current candidate for governance review is TIME_FILTER with two successive completed D1 closes beyond the support boundary in the downside direction.

This is NOT an approved production rule. No historical performance result is used as the reason for selecting it.

## Source boundary
Murphy supports a two-successive-closes time-filter family in the broader breakout/penetration discussion. Murphy also discusses price filters. The uploaded project handoff explicitly prohibits silently converting either example into a hard 0008 threshold.

## Operational candidate
- Support boundary must already be available.
- First completed D1 close below support = raw/candidate break.
- Second successive completed D1 close below support = decisive confirmation.
- Confirmation timestamp = completion/close of the second D1 bar.
- No confirmation is available before that close.
- Later retest evidence begins strictly after confirmation.
- If required data are unavailable, return NOT_EVALUABLE.

## Why this candidate is operationally attractive
It is deterministic, has explicit chronology, does not require an invented percentage/ATR/pip tolerance, and fits the shared PF-B1 interface.

## Non-claims
- This document does not claim Murphy says “0008 = two D1 closes.”
- This document does not claim the candidate is superior because of historical replay results.
- This document does not freeze PF-B1 or 0008.

## Required next gate
Governance must explicitly approve or reject this policy. If approved, freeze the PF-B1 contract and provenance before implementing the 0008 evaluator.