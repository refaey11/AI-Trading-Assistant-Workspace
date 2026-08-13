# Murphy 0006/0007 Compatibility Audit V3

Date: 2026-08-13
Status: AUDIT COMPLETE / DETERMINISTIC OPERATOR STILL OPEN

## Scope
Final compatibility audit of the Murphy 0006/0007 Confirmation Layer against:
1. File Library / Workspace state
2. Full Project handoffs/contracts
3. GitHub implementation/history/commits/search
4. Historical Memory role/contracts
5. Existing break/no-break references and evaluator infrastructure

## Source-of-truth result
Workspace/File Library remains source of truth; GitHub is development/provenance mirror. Existing Pivot and Geometry components are reusable and must not be rebuilt.

## Confirmed existing chain
PIVOT_SEQUENCE_V2 -> TRENDLINE_GEOMETRY_V1 -> MURPHY_CONFIRMATION_LAYER -> existing 0006/0007 evaluator.

## Geometry compatibility
Geometry V1 provides line identity, HIGH/LOW family, anchors, direction, slope, and availability. Direct audit confirms its output does not contain third-touch event, reaction event, no-break event, or confirmation timestamp. Breakout detection and added thresholds are explicitly excluded from Geometry.

## Existing evidence adapter
The existing source-safe adapter intentionally calculates line geometry and raw candidate evidence only. It explicitly does not implement successful-touch, reaction, or no-break PASS/FAIL predicates. This component must be preserved.

## GitHub provenance search
Searched repository files and commit history for:
- third_touch
- reaction_bounce
- successful touch
- meaningful break
- no break
- break_structure_up/down
- touch tolerance
- reaction threshold
- breakout threshold
- price penetration trendline filter
- breakout filter
- two consecutive days
- operator-related commits

Findings:
- `break_structure_up/down` exists as a reference/concept in broader Murphy work, including 0001 mapping, but no executable contract was found that binds it to 0006/0007 `no_break`.
- No executable `reaction_bounce` implementation was found.
- No deterministic `third_touch` implementation/contract was found.
- No approved numeric touch/reaction threshold or 0006/0007-specific break filter was found.
- Existing evaluator expects upstream facts rather than deriving these semantics itself.

## Historical Memory
Historical Memory is explicitly evidence/QA infrastructure only. It cannot define Murphy semantics, select an operator, or tune thresholds. The available handoff does not establish an internal Historical Memory artifact that can serve as an authoritative 0006/0007 operator contract.

## Murphy source semantics
The uploaded Murphy Chapter 4 supports the qualitative chain:
- two points establish a tentative trendline;
- a third successful test/touch with reaction increases/establishes confirmation;
- temporary/intraday penetration is not automatically a meaningful break;
- closing beyond a trendline is more significant;
- general price/time filters are discussed.

The project explicitly does not bind the general 3% / 2-consecutive-day examples to 0006/0007 without an explicit project contract.

## Final field reconciliation
Required evaluator facts vs current authoritative upstream evidence:

| Fact | Current state |
|---|---|
| line_id | AVAILABLE |
| LOW/HIGH family | AVAILABLE |
| UP/DOWN direction | AVAILABLE |
| anchor 1/2 | AVAILABLE |
| line availability | AVAILABLE |
| third_touch | CANDIDATE EVIDENCE ONLY |
| reaction_bounce | CANDIDATE EVIDENCE ONLY |
| no_break | OBSERVATION ONLY |
| confirmation timestamp | BLOCKED by above predicates |

## Gate decision
No source-backed deterministic operator was found that can safely convert the candidate observations into production PASS/FAIL.

Therefore the correct state is:
- 0006 = MAPPING COMPATIBLE / OPERATOR OPEN / NOT_EVALUABLE
- 0007 = MAPPING COMPATIBLE / OPERATOR OPEN / NOT_EVALUABLE

The 347-row corrected 2016–2024 candidate population remains evidence-only and must not be promoted to production confirmation.

## Non-negotiable constraints preserved
- Do not rebuild Pivot V2.
- Do not rebuild Geometry V1.
- Do not replace the existing evaluator.
- Do not invent ATR, pip, percentage, distance, lookback, duration, or timeframe thresholds.
- Do not automatically bind Murphy's general 3%/2-day examples to 0006/0007.
- Do not use 2025 for tuning or implementation selection.
- Do not use Historical Memory to define the Murphy operator.

## Next authorized work
The compatibility audit is now complete. If the project owner wants production evaluation, a new authoritative operator contract must be supplied/recovered. Until then, only candidate-evidence generation and deterministic QA are authorized; production 0006/0007 evaluation remains NOT_EVALUABLE.
