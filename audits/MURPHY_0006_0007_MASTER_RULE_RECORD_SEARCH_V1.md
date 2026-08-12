# Murphy 0006–0007 Master Rule Record Search V1

Date: 2026-08-12
Status: SEARCH COMPLETED / ORIGINAL RECORD NOT RECOVERED

## Search scope

Searched current Workspace/File Library and project archives for the authoritative original records of:
- MURPHY_0006
- MURPHY_0007

Search fields/terms included:
- rule_id
- primary_source
- original_rule
- rule_name
- setup
- conditions
- decision
- source_row / metadata
- trendline
- touch
- reaction
- Confirmed Uptrend Line
- Confirmed Downtrend Line

Also checked the GitHub development/provenance mirror for matching source implementation/records.

## What was found

The current project state / Rule Registry confirms both rules exist and currently uses the wording:
`A third successful touch and reaction confirms the trendline.`

The current handoff records the working mapping:
- 0006 = LOW + UP -> BULLISH
- 0007 = HIGH + DOWN -> BEARISH

However, the same authoritative project-state artifacts explicitly mark this mapping as `WORKING_RESOLUTION — SOURCE_LOCK STILL REQUIRED` and instruct that the original database records must be retrieved before promoting it to official/frozen status.

The current status also confirms the exact operational meaning of successful touch, reaction, third touch, and confirmation/availability timing is not proven from the authoritative project contract.

## Search result

No independent Master Rule Database record was recovered that provides the requested full field set for MURPHY_0006/MURPHY_0007.

No GitHub source file was found that supersedes the Workspace/Rule Registry provenance with an authoritative original record.

Therefore this search does NOT authorize:
- promotion of the working mapping to Source-Locked;
- a deterministic touch threshold;
- a deterministic reaction threshold;
- an automatic 3%/2-day binding;
- production PASS/FAIL evaluation.

## Important distinction

The Murphy Chapter 4 source semantics are already documented separately. This audit concerns recovery of the project's ORIGINAL RULE RECORD / metadata, not re-proving Chapter 4 semantics.

## Current gate

MURPHY_0006 = MAPPING COMPATIBLE / SOURCE-LOCK REQUIRED
MURPHY_0007 = MAPPING COMPATIBLE / SOURCE-LOCK REQUIRED

Operational evidence and evaluator remain open.

## Next action

Do not restart Chapter 4 research. Proceed with the planned compatibility audit against:
1. existing PIVOT_SEQUENCE_V2;
2. existing TRENDLINE_GEOMETRY_V1;
3. D1 OHLC evidence;
4. existing break/no-break contracts;
5. Historical Memory evidence-only infrastructure.

If an authoritative original record becomes available later, reconcile it against this audit before changing any operator or evaluator.

2025 remains OOS and excluded from tuning/selection.
