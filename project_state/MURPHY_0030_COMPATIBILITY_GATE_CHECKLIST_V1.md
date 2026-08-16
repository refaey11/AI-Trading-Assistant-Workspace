# Murphy 0030 — Compatibility Gate Checklist V1

This checklist is an executable-gate contract, not a production freeze.

- [ ] C1 construction semantics match canonical source-bounded 3-box High/Low behavior.
- [ ] C2 bullish support semantics match the canonical 45-degree structural support.
- [x] C3 implementation no-lookahead property: prefix snapshot is unchanged by a future suffix.
- [x] C4 implementation determinism: identical input replay produces identical normalized columns.
- [ ] C5 box-size policy is source-faithful and governance-approved; no optimization/tuning used.
- [ ] External candidate is classified `COMPATIBLE_CANDIDATE`, `INCOMPATIBLE`, or `NOT_EVALUABLE`.
- [ ] 2016–2024 historical QA is run only after C1–C5 closure.
- [x] 2025 exclusion is enforced by the gate fixture; no 2025 data is used by the new evidence tests.
- [ ] Provenance is recorded.
- [ ] Freeze decision is made only by the formal governance gate.

## Evidence added

Commit `bdaf1a2aeca69bbd04343fbf0c05296fcf6d8a4b` adds executable tests for C3/C4 and an explicit pre-OOS fixture check. These are implementation-property checks only; they do not certify Murphy semantics, box-size governance, or Freeze.

Current decision: `NOT_EVALUABLE` pending C1/C2/C5 closure and fresh CI evidence.
