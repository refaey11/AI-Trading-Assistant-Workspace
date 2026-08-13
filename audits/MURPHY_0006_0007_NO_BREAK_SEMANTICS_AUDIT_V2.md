# Murphy 0006/0007 — No-Break Semantics Audit V2
Date: 2026-08-13
Status: VERIFIED / PRODUCTION GATE STILL OPEN

## Question
Can the existing `no_break_observation` field be promoted directly to the Confirmation Layer's `no_break_valid` without introducing unsupported semantics?

## Evidence inspected
- Murphy 0006/0007 current-status and handoff artifacts.
- Candidate Evidence V4 schema and real 2016-2024 rows.
- Existing Confirmation Layer design.
- Existing Geometry V1 scope.
- Existing 2016-2024 confirmation-availability QA.
- GitHub history/commits for 0006/0007 compatibility and candidate evidence.

## Finding 1 — Current field is explicitly observation-only
Candidate Evidence V4 exposes `no_break_observation`, but its value is `OBSERVATION_ONLY` and the overall `evidence_status` remains `CANDIDATE_ONLY`. The field is therefore not a production validity predicate.

## Finding 2 — Geometry V1 cannot supply the missing predicate
Canonical Geometry V1 emits line identity, family, anchors, slope, direction and availability. Breakout detection is outside its scope. No Geometry modification is authorized.

## Finding 3 — Existing 15 provisional confirmations do not close provenance
The 2016-2024 QA has 32 strong candidates for 0006 and 30 for 0007, with 8 and 7 provisional confirmations respectively. The confirmation availability is correctly tied to reaction-pivot V2 availability, preserving no-lookahead. The QA itself states that the no-break event is an operationalization using completed D1 bars between third touch and reaction and requires provenance approval before production freeze.

## Finding 4 — General Murphy break filters are not automatically a 0006/0007 contract
The project records Murphy's general price/time breakout examples (including 3% and two consecutive daily closes) but explicitly prohibits automatically binding those examples to 0006/0007. Therefore neither 3% nor 2-day can be silently promoted here.

## Decision
`no_break_observation` MUST remain observation-only.
`no_break_valid` remains NOT_EVALUABLE for production until an authoritative project/source contract approves the exact predicate.

## Safe next action
Do not modify Geometry, Pivot, Adapter, or Evaluator. Keep the current event layer as candidate evidence. The only remaining work is provenance approval of the deterministic no-break predicate (and, if required by the same contract, the exact successful-touch/reaction predicates). Once approved, bind it to the existing Confirmation Layer and run deterministic tests + 2016-2024 QA.

## Controls
- 2025 excluded.
- No ATR.
- No pip/percentage tolerance.
- No fixed lookback.
- No automatic 3% binding.
- No automatic 2-day binding.
- No lookahead.
