# AI Trading Assistant — Master Project Status V2

Date: 2026-08-15
Status: CANONICAL PROJECT STATUS

## Source-of-truth rule
This status supersedes older handoff/status notes when they conflict with newer verified records on `main`. Historical notes remain historical evidence and must not be treated as current state.

## Murphy rule status

| Rule | Current status | Evidence / note |
|---|---|---|
| 0001 | PARTIAL / NOT FROZEN | Contract gap remains around definite reversal semantics. |
| 0002 | NEXT VERIFICATION TARGET | Must be audited against existing Workspace before implementation/rebuild. |
| 0003 | PRODUCTION FROZEN | V2 availability-aligned evaluator + tests + 2016–2024 historical validation passed. |
| 0004 | PRODUCTION FROZEN | Same V2 freeze record and validation as 0003. |
| 0005 | STATUS TO BE VERIFIED | Do not infer completion from adjacent rules. |
| 0006 | VALIDATION / FREEZE REVIEW | Existing operational candidate/evidence exists; production freeze not yet recorded on main. |
| 0007 | VALIDATION / FREEZE REVIEW | Existing operational candidate/evidence exists; production freeze not yet recorded on main. |
| 0008 | PRODUCTION FROZEN | Final validated path merged to main through PR #10. |
| 0009 | NOT FROZEN | Source semantics/evaluator work remains; do not assume completion. |
| 0010–0020 | MIXED / AUDIT REQUIRED | Existing source/reconciliation artifacts exist; each rule requires its own verified status before promotion. |
| 0021–0023 | VALIDATION-ONLY / AUDIT REQUIRED | Existing adapter/evaluator validation PR remains open; production freeze not established. |

## Verified frozen rules
### MURPHY_0003–0004
- Status: PRODUCTION FROZEN.
- Contract: 0003 = current reaction peak > prior reaction peak AND current reaction trough > prior reaction trough.
- Contract: 0004 = current reaction peak < prior reaction peak AND current reaction trough < prior reaction trough.
- Confirmed pivots require confirmation after 2 bars.
- Evidence must satisfy availability_timestamp <= evaluation_availability_timestamp.
- Future pivots excluded; missing required evidence = NOT_EVALUABLE.
- Historical validation: 2016–2024.
- 2025 included: NO.
- Validation workflow Run #5 / Run ID 31452549681: SUCCESS.
- Final freeze record: audits/MURPHY_0003_0004_EVALUATOR_V2/MURPHY_0003_0004_FREEZE_RECORD_V1.md.

### MURPHY_0008
- Status: PRODUCTION FROZEN.
- PF-H1: singleton confirmed LOW pivot from PIVOT_SEQUENCE_V2 as Support boundary.
- PF-B1: first completed D1 close strictly below Support = candidate; immediately following completed D1 close strictly below the same Support = decisive confirmation.
- Retest starts strictly after confirmation.
- Historical validation: 2016–2024.
- Corrected confirmation count: 242; earlier 324 replay is superseded.
- 2025 confirmations: 0.
- Production merge: PR #10; merge commit 515aac5785ed36529763cbf1b4e0f8324b2aeee3.

## Project-wide guardrails
- 2025 is OOS and must never be used for rule selection or tuning.
- Never rebuild existing project knowledge from scratch; audit and integrate existing artifacts first.
- Every new integration requires a compatibility audit.
- No invented ATR/pip/percentage/tolerance/lookback unless explicitly source-supported and contract-approved.
- Evidence frequency is not profitability.
- Production freeze requires deterministic tests, availability/no-lookahead validation, historical validation, provenance, and explicit freeze evidence.

## Immediate work queue
1. Verify and close 0006/0007 freeze gates using current main/workspace evidence.
2. Verify 0002 against the existing canonical Workspace before building anything new.
3. Resolve 0001 contract gap.
4. Audit 0009 and subsequent rules individually.
5. Continue project-wide Rule Adapter / Decision Brain integration only after rule contracts are verified.
6. Complete official baseline and walk-forward gates after the rule layer is sufficiently closed.

## Do-not-do list
- Do not reopen 0003/0004 or 0008 without a versioned change request.
- Do not retune frozen rules using historical outputs.
- Do not treat old handoff documents as current status when a newer freeze record exists.
