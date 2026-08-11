# Murphy 0006–0007 Compatibility / Validation V1

Date: 2026-08-12

## Scope

Validate the existing Trendline Geometry V1 against the resolved project mapping supplied from the project knowledge/source review. Do not rebuild Trendline Geometry and do not introduce new thresholds.

## Resolved rule mapping

| Rule | Line anchors | Trendline direction | Decision direction |
|---|---|---|---|
| MURPHY_0006 | LOW / reaction lows | UP | BULLISH |
| MURPHY_0007 | HIGH / reaction highs | DOWN | BEARISH |

This mapping is accepted as the current project handoff resolution. The Workspace snapshot still contains an older NOT_YET_EVALUABLE note stating that the registry text alone did not distinguish the two rules; therefore this file records the resolution but does not claim that the older registry text itself proved the split.

## Existing component compatibility

### 0006
- Input line type: `LOW`
- Expected geometry direction: `UP`
- Expected decision direction: `BULLISH`
- Existing Trendline Geometry V1 is the required producer.

### 0007
- Input line type: `HIGH`
- Expected geometry direction: `DOWN`
- Expected decision direction: `BEARISH`
- Existing Trendline Geometry V1 is the required producer.

## Pivot dependency

The existing project uses PIVOT_SEQUENCE_V2. Its verified contract uses confirmed pivots with two confirming bars and makes the pivot available at `pivot timestamp + 2 bars`; evaluation must not use information before that availability point.

## Third-touch / reaction gate

Murphy source wording requires a third successful touch and reaction to confirm the trendline. No numeric tolerance, ATR threshold, percentage threshold, or lookback is introduced here.

Therefore:
- mapping validation can be completed;
- the confirmation operator remains `NOT_YET_EVALUABLE` unless the existing Trendline Geometry V1 contract exposes an explicit source-backed successful-touch/reaction field.

## Validation result

**MAPPING: RESOLVED**

**GEOMETRY COMPATIBILITY: PASS in schema/semantic direction**

**THIRD-TOUCH/REACTION OPERATOR: NOT_YET_EVALUABLE**

**2025: untouched / OOS**

## No-go conditions

Do not:
- create a new trendline engine;
- invent a numeric touch tolerance;
- tune against 2025;
- modify Murphy 0003/0004;
- copy the 102 rules into the Decision Brain.

## Next action

Inspect the existing Trendline Geometry V1 output schema for an already-defined third-test/reaction/confirmation field. If present, wire 0006/0007 to it and add tests. If absent, keep only the mapping resolved and leave the third-touch operator NOT_YET_EVALUABLE pending source-backed definition.
