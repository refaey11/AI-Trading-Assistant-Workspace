# Murphy 0006–0007 Candidate Evidence Layer V1

Date: 2026-08-12
Status: CANDIDATE-ONLY / NOT A PRODUCTION EVALUATOR

## Purpose

Provide a source-safe evidence layer over existing PIVOT_SEQUENCE_V2, TRENDLINE_GEOMETRY_V1, and completed D1 OHLC evidence without inventing a deterministic touch/reaction threshold.

## Upstream reuse

- PIVOT_SEQUENCE_V2: canonical pivot sequence and availability/no-lookahead lineage.
- TRENDLINE_GEOMETRY_V1: anchors, line family, slope, direction, and line availability.
- Existing D1 OHLC evidence: completed High/Low/Open/Close bars for evidence inspection.

Do not rebuild or modify these upstream components.

## Candidate events

### 0006 candidate touch

Expected family:
- line_type = LOW
- direction = UP
- third event is a confirmed LOW pivot after the two defining anchors.

Candidate evidence may record:
- third pivot timestamp
- third pivot price
- line price at the third pivot timestamp
- signed/absolute distance between pivot and line
- daily High/Low range intersection with the line

These are observations only. No fixed distance threshold is applied.

### 0007 candidate touch

Expected family:
- line_type = HIGH
- direction = DOWN
- third event is a confirmed HIGH pivot after the two defining anchors.

Record the same evidence fields. No fixed distance threshold is applied.

## Candidate reaction

Record subsequent completed-bar/pivot movement that is directionally consistent with the Murphy semantic `reaction/rebound away from the line`.

Do not define reaction by a new fixed number of bars, close threshold, percentage, ATR, or pip amount.

Therefore reaction evidence is candidate evidence only.

## Candidate no-break

Record whether the completed D1 range remains consistent with the source statement that the trendline encloses the daily price range.

If a potential penetration occurs, record the raw observation and do not classify it as a confirmed break unless an approved project break-filter contract is bound.

General Murphy 3% and 2-consecutive-day break filters remain separate source material and are not automatically bound to 0006/0007.

## Output contract

Each candidate record should contain at minimum:
- rule_id
- line_id
- line_type
- direction
- anchor timestamps/prices
- line availability timestamp
- third pivot timestamp/price
- line price at third pivot
- distance observation
- daily range intersection observation
- reaction candidate observation
- no-break candidate observation
- source timestamps used
- status = `CANDIDATE_ONLY`

## Explicit non-goals

This layer MUST NOT:
- return production PASS/FAIL for 0006/0007;
- invent touch tolerance;
- invent reaction magnitude/duration;
- use ATR, pips, percentages, or lookbacks as hidden thresholds;
- automatically bind 3% or 2-day filters;
- use 2025 for selection or tuning.

## Gate

Production confirmation remains `NOT_EVALUABLE` until a source/project-approved deterministic operator exists for successful third touch + reaction and the associated no-break binding.

This layer exists to preserve all observable evidence so that the eventual operator can be added without rebuilding Geometry or Pivot Sequence.
