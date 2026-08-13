# AI Trading Assistant — Decision Brain
## Current Project Status — 2026-08-13

### Purpose
This file records the latest verified project state so future work resumes from the exact current state instead of rebuilding or guessing.

### Source-of-truth policy
- Workspace / actual project artifacts are the source of truth.
- GitHub is the development/provenance mirror and must be checked when history, contracts, commits, or audits matter.
- Existing components must be audited and integrated, not rebuilt.
- Compatibility audit is required before any new integration.
- 2025 is OOS and must never be used for tuning, operator selection, threshold selection, or implementation selection.

### Architecture status
- John Murphy = technical context / market structure.
- Steve Nison = confirmation.
- Trading in the Zone = psychology/process gate; it cannot generate market direction.
- Similarity / Historical Memory = historical evidence only; it cannot be the sole decision maker.
- Decision Brain = current market evidence + book knowledge + historical memory + risk.
- Existing Pivot Sequence V2 and Trendline Geometry V1 are canonical upstream primitives and must not be rebuilt.

### Murphy rules — production state
#### MURPHY_0003–0004
**STATUS: PRODUCTION FROZEN**

Freeze basis:
- Existing availability-alignment contract verified.
- Existing evaluator implementation verified.
- Unit tests: 7/7 passed.
- Historical validation: 2016–2024 passed.
- 2025 excluded.
- Confirmed pivots require confirmation after 2 bars.
- Only evidence with availability_timestamp <= evaluation_availability_timestamp may participate.
- Future pivots are excluded.
- Missing required evidence returns NOT_EVALUABLE.
- No thresholds or pivot-generation parameters were tuned from 2025 or evaluation outputs.

Canonical freeze record:
`audits/MURPHY_0003_0004_EVALUATOR_V2/MURPHY_0003_0004_FREEZE_RECORD_V1.md`

Freeze commits include:
- `d080880f8f08b21fda6645aca526e1660d619482` — Freeze Murphy 0003-0004 after successful V2 validation
- `de171a054aa89292ab28d3d4b9d49e345f628fa1` — Add Murphy 0003-0004 production freeze record
- `0ab177c0bbb99b2d4b3b4242ca7d9e64a5ed6037` — Add Murphy 0003-0004 frozen handoff backup 2026-08-13

Exact rule semantics:
- MURPHY_0003: current reaction peak > prior reaction peak AND current reaction trough > prior reaction trough.
- MURPHY_0004: current reaction peak < prior reaction peak AND current reaction trough < prior reaction trough.

Historical results recorded in the freeze evidence:
- D1: 341 evaluatable; 0003 PASS 101; 0004 PASS 118
- H1: 7,728 evaluatable; 0003 PASS 2,257; 0004 PASS 2,056
- H4: 1,923 evaluatable; 0003 PASS 584; 0004 PASS 592
- M15: 29,388 evaluatable; 0003 PASS 8,373; 0004 PASS 8,362
- M30: 14,928 evaluatable; 0003 PASS 4,304; 0004 PASS 4,156
- M5: 84,266 evaluatable; 0003 PASS 24,447; 0004 PASS 23,940

#### MURPHY_0006–0007
**STATUS: NOT_EVALUABLE / OPERATIONAL GATE OPEN**

Already closed:
- source-level qualitative semantics
- 0006/0007 mapping
- Pivot Sequence V2
- Trendline Geometry V1
- D1 2016–2024 evidence input
- candidate evidence population
- evidence adapter and tests
- generic evaluator architecture
- confirmation-layer design

Still missing and source-sensitive:
- deterministic successful third-touch operator
- deterministic successful reaction operator
- deterministic 0006/0007 no-break contract
- final confirmation timing semantics

Do not use the exploratory 2-day test as binding. The 42 survivors are evidence only, not PASS.
Do not add ATR, pip, percentage, lookback, tolerance, reaction magnitude, or reaction duration thresholds without an approved source/contract.

### Current resume point
The next work item is NOT to revisit 0003/0004. They are frozen.

Resume at the next Murphy rule with the same workflow:
`source → provenance/contract → compatibility audit → existing primitives → evaluator → unit tests → 2016–2024 QA → freeze`

For 0006/0007, resume only if a new authoritative source/contract can resolve the confirmation operator; otherwise preserve NOT_EVALUABLE and continue with the next evaluable Murphy rule.
