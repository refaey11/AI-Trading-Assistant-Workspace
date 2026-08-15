# Murphy 0030–0032 — Gate Manifest V2

Date: 2026-08-16
Branch: proposal/murphy-0030-box-policy-v1

## Source / compatibility
- Murphy Chapter 11 mapping: PASS
- Rule contract: PASS / DRAFT
- 0030 structural-only boundary: PASS
- 0031 risk-only stop relation: PASS
- 0032 risk-only stop relation: PASS

## Operational policies
- Logarithmic 3-box P&F core: PRESENT
- Box Policy 0.6257356643%: REPRODUCIBLE PROJECT PROPOSAL / NOT SOURCE-VERBATIM
- External deterministic bootstrap: DOCUMENTED / NOT SOURCE-VERBATIM
- Production policy approval: NOT YET GRANTED

## Implementation
- Shared P&F engine: PRESENT
- 0030–0032 evidence evaluator: PRESENT
- Focused evaluator tests: PRESENT
- Prefix replay test: PRESENT

## Historical gates
- Canonical GBPUSD D1 dataset: PRESENT in project File Library (2016–2024)
- Fresh 2019–2024 evaluator replay: BLOCKED in current runtime because the complete canonical dataset bytes are not mounted for execution
- Dataset-level availability audit: NOT RUN
- Dataset-level no-lookahead audit: NOT RUN
- Final structural sensitivity acceptance: NOT RUN against final evaluator

## CI
- Dedicated Murphy 0030–0032 workflow: PRESENT
- Actual workflow run for current proposal commits: NOT OBSERVED

## Governance
- 2025 used for tuning/selection: NO
- Profitability-based box selection: NO
- Merge to Production: NO
- Production freeze: NO

## Current decision
**BLOCKED**

## Exact release gate
Do not change the decision to PASS until all of the following are evidenced:
1. canonical dataset is available to the evaluator runtime;
2. fresh 2019–2024 replay completes;
3. availability and no-lookahead checks pass on that replay;
4. pre-declared structural sensitivity checks pass;
5. CI execution is evidenced or an equivalent reproducible CI record is attached;
6. governance explicitly accepts the two operational policies as project policies, without representing them as Murphy/Tower formulas.
