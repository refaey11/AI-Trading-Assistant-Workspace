# MURPHY 0006/0007 — GOVERNANCE DECISION V1

Date: 2026-08-14
Status: DECISION RECORDED — CONDITIONAL APPROVAL FOR PROJECT IMPLEMENTATION

## Decision
The current deterministic 0006/0007 operational contract is APPROVED for project implementation as an explicit operationalization of Murphy Chapter 4 semantics, subject to final production-path validation and freeze gates.

This approval does NOT claim that Murphy provides the exact numeric/deterministic implementation verbatim. Murphy is the semantic authority; the Project Operational Contract is the executable translation.

## Source basis
- Chapter 4 supports reaction-high/reaction-low trendline construction, two anchors, a third successful touch/reaction, and confirmation associated with a line that has not been meaningfully broken.
- The full-book audit found no separate authoritative 0006/0007 deterministic numeric contract that supersedes the project operationalization.
- General Chapter 4 3% and 2-consecutive-daily-close examples are not authorized as 0006/0007-specific parameters.

## Operational boundary
The approved implementation must remain deterministic and source-safe. It must not introduce ATR, pip thresholds, arbitrary percentages, hidden lookbacks, 3% filters, 2-day filters, or 2025-derived tuning unless a future source/governance change explicitly authorizes them.

## Evidence already closed
- M1→D1 lineage verified across 2,544 2016–2024 dates with max OHLC difference 0.
- Canonical Pivot V2 preserved.
- Canonical Geometry V1 preserved.
- Fresh replay evidence: 0006=8, 0007=7, total=15, 2025 excluded, no-lookahead/availability checks recorded.
- Operator regression fixes for first eligible third-touch candidate and strict post-touch reaction ordering are committed on the freeze-review branch.

## Remaining gates
1. Run the final deterministic test suite on the corrected operator.
2. Run a fresh production-path validation using the corrected operator and canonical inputs.
3. Record exact commit/input hashes, outputs, case IDs, and no-lookahead result.
4. If all pass, create the final freeze manifest and explicit freeze decision.

## Non-negotiable rule
Do not alter the approved operator merely to recover a historical case count. Any behavior change requires a documented source/governance change request and a new audit.
