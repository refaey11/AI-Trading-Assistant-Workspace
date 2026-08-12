# Murphy 0006–0007 Source Lock Audit V1

Date: 2026-08-12

## Result

**SOURCE LOCK NOT CLOSED.**

The available Workspace/File Library evidence confirms the following working mapping from the dedicated 0006–0007 project snapshot:
- MURPHY_0006 = Confirmed Uptrend Line; LOW anchors; UP; BULLISH.
- MURPHY_0007 = Confirmed Downtrend Line; HIGH anchors; DOWN; BEARISH.

However, the same source artifact explicitly labels this as `WORKING_RESOLUTION — SOURCE_LOCK STILL REQUIRED` and says the searchable Rule Registry excerpts do not independently establish the split.

## Existing source semantics

The supplied Murphy technical source establishes:
- a trendline connects highest points or lowest points;
- at least two points are needed to draw it;
- more tests increase importance;
- the current registry condition for both 0006 and 0007 is: `A third successful touch and reaction confirms the trendline.`

The authoritative operational definition of `successful touch`, `reaction`, `third touch`, and confirmation/availability timing is not present in the retrieved source records.

## Existing infrastructure

- PIVOT_SEQUENCE_V2 exists and uses confirmed pivots with two confirming bars, availability at pivot timestamp + 2 bars, and no lookahead before availability.
- TRENDLINE_GEOMETRY_V1 exists and must be reused.
- Existing adapter contract exists; it normalizes rule outputs and does not decide trades.

## Required evidence for freeze

1. two valid trendline anchors;
2. correct LOW/HIGH line family;
3. UP/DOWN direction;
4. third touch;
5. successful reaction;
6. no break;
7. availability timestamp/no-lookahead.

## Decision

Do **not** mark 0006/0007 FROZEN yet. Do not create a new evaluator or threshold. Keep them at `MAPPING_COMPATIBLE / OPERATIONAL_EVIDENCE_UNPROVEN` until the authoritative Rule Registry/Master KB record or an existing project contract supplies the missing evidence.

This is a blocker for these two rules only and does not alter 0003/0004.

## OOS control

2025 remains OOS and is not used for tuning, selection, or implementation choice.
