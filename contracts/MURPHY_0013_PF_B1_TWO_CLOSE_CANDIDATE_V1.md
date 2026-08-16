# Murphy 0013 — PF-B1 Two-Close Candidate V1

Status: CANDIDATE / NOT PRODUCTION FROZEN

## Purpose
Reuse the validated 0008 two-close confirmation mechanism as an operational candidate for the 0013 Triangle boundary, without importing 0008 Support semantics.

## Boundary
The boundary MUST be the canonical 0013 pattern boundary produced by the shared geometry layer. It is not a Support Identity and must not be selected using `support_20`, `support_50`, `support_100`, clustering, or any newly invented tolerance.

## Candidate state machine
1. `BOUNDARY_AVAILABLE`: the boundary is available before break observation.
2. `BREAK_CANDIDATE`: a completed D1 close is strictly beyond the applicable 0013 boundary in the breakout direction.
3. `BREAK_CONFIRMED`: the immediately following completed D1 close is also strictly beyond the same boundary in the same breakout direction.
4. Missing/ambiguous boundary or chronology evidence => `NOT_EVALUABLE`.

## Borrowed from 0008
Only the confirmation mechanism is reused: first completed close creates a candidate; the immediately following completed close confirms.

## Not borrowed from 0008
No Support identity, support-period selection, ATR/pip/percentage threshold, clustering tolerance, hidden lookback, or historical-performance-derived threshold is transferred.

## Governance
This is an integration candidate only. It requires 0013 source-compatibility review, unit tests, availability/no-lookahead tests, 2016–2024 replay, and explicit freeze approval before production use. 2025 remains OOS and MUST NOT be used for tuning or policy selection.
