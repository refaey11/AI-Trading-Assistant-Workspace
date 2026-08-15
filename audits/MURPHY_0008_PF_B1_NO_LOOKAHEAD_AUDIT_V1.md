# Murphy 0008 — PF-B1 No-Lookahead Audit V1

Status: EXPERIMENTAL / NOT FROZEN
Policy under test: TIME_FILTER — two successive completed D1 closes below support.
Scope: 2016-01-01 through 2024-12-31 only. 2025 excluded.

## Required event ordering
1. Support candidate must be available before the first break bar.
2. First D1 close below support is only a candidate event.
3. Second successive completed D1 close below support creates decisive confirmation.
4. Confirmation timestamp is the close time of the second completed D1 bar.
5. No event may use the second bar's information before that bar closes.
6. A later rally/retest may only be evaluated from bars strictly after confirmation.

## Edge cases
- Intrabar low below support without a closing break: not confirmed.
- One close below support followed by a close back above: not confirmed.
- Missing/unavailable second D1 bar: NOT_EVALUABLE.
- Duplicate timestamp: reject / quarantine.
- Support candidate becoming available after the alleged first break: reject as lookahead.
- Retest on the confirmation bar itself: excluded from later-retest evidence.

## Result interpretation
This audit validates temporal causality and deterministic event ordering only. It does not prove that the TIME_FILTER policy is the final production policy and must not be used to tune the rule.

## Freeze gate
Production freeze remains blocked until governance approval, deterministic unit tests, availability validation, historical QA, provenance, and freeze-manifest review are complete.
