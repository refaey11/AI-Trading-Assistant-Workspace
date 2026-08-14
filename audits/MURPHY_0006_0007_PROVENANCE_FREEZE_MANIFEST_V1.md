# MURPHY 0006/0007 — PROVENANCE / FREEZE MANIFEST V1

Status: FREEZE CANDIDATE / NOT PRODUCTION FROZEN

## Rule identities
- MURPHY_0006: confirmed uptrend line / LOW + UP / bullish.
- MURPHY_0007: confirmed downtrend line / HIGH + DOWN / bearish.

## Evidence lineage
1. John Murphy Chapter 4 source semantics.
2. PIVOT_SEQUENCE_V2 confirmed pivots and availability.
3. TRENDLINE_GEOMETRY_V1 existing trendline construction.
4. Murphy confirmation/event operator candidate V1.
5. Canonical 2016–2024 confirmation-availability evidence.
6. Final QA reconciliation artifact.
7. Deterministic unit-test suite.

## QA record
- Period: 2016–2024.
- 2025: excluded from tuning and operator selection.
- 0006 confirmations: 8.
- 0007 confirmations: 7.
- Total confirmations: 15.
- Exact reconciliation: 15/15.
- Operator-only: 0.
- Reference-only: 0.
- Availability-before-reaction violations: 0.
- Third-touch availability violations: 0.
- 2025+ confirmations: 0.
- Deterministic tests: 7/7 PASS.

## Operationalization boundary
The no-break predicate is a deterministic project operationalization of Murphy's qualitative line-hold / meaningful-break semantics. It must not be represented as verbatim source text.

## Forbidden changes
Do not introduce ATR/pip/percentage tolerance, arbitrary lookback, automatic 3% filter, automatic 2-day binding, or 2025 tuning.

## Freeze decision
NOT YET FROZEN.

Required final approvals:
- historical QA sign-off;
- availability/no-lookahead sign-off;
- governance approval of the formal project contract;
- explicit production-freeze decision.

Until those approvals are recorded, the candidate must remain isolated from production.
