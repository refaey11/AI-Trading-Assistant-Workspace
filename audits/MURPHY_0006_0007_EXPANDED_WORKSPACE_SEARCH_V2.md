# Murphy 0006–0007 Expanded Workspace Search V2
Date: 2026-08-12

## Search scope
Expanded search across the currently available uploaded Workspace/File Library material and project handoff/current-state artifacts for:
- MURPHY_0006
- MURPHY_0007
- original_rule / primary_source / setup / conditions / decision
- Confirmed Uptrend Line / Confirmed Downtrend Line
- third successful touch / reaction / availability
- Trendline Geometry V1 contracts and outputs

## Findings

### 1. Rule wording
The available Rule Registry status artifact records both 0006 and 0007 as NOT_YET_EVALUABLE with the same condition:
`A third successful touch and reaction confirms the trendline.`

### 2. Working mapping
A current-state snapshot records the working operational split:
- 0006 = LOW + UP -> BULLISH
- 0007 = HIGH + DOWN -> BEARISH
and names them Confirmed Uptrend Line / Confirmed Downtrend Line.
However, that same artifact explicitly marks this as WORKING_RESOLUTION — SOURCE_LOCK STILL REQUIRED and says the searchable Rule Registry excerpts do not prove the split from an authoritative original record.

### 3. Trendline infrastructure
The Workspace contains existing Trendline Geometry V1 artifacts, including:
- TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json
- TRENDLINE_GEOMETRY_QA_V1.csv
- TRENDLINE_GEOMETRY_MANIFEST_V1.csv
- timeframe-specific trendline output CSVs

The Pivot Sequence lineage is also present with confirmed pivots, two confirming bars, availability at pivot timestamp + 2 bars, and no lookahead before availability.

### 4. Missing semantic contract
The expanded search still did not recover an authoritative row-level Rule Database record that defines:
- what constitutes a successful touch;
- what constitutes a reaction;
- whether the third touch or the reaction is the confirmation event;
- exact no-break condition;
- exact confirmation/availability timestamp;
- any rule-specific distinction between 0006 and 0007.

No source-backed tolerance, threshold, lookback, or fixed timeframe was recovered.

## Compatibility result
**MAPPING_COMPATIBLE / OPERATIONAL_EVIDENCE_UNPROVEN**

Existing Trendline Geometry can be reused, but the present searchable evidence does not prove all fields required for a production evaluator:
1. two valid anchors;
2. LOW/HIGH family;
3. UP/DOWN direction;
4. third touch;
5. successful reaction;
6. no break;
7. availability/no-lookahead.

## Decision
Do not implement or freeze 0006/0007 from the current evidence.
Do not infer the working split as authoritative.
Do not invent touch/reaction thresholds or timeframes.

## Next recovery targets
Search or recover an authoritative original source/database object from the Master Rule Database / TRADING_RULES_V2 archive that contains the row-level records and metadata for 0006 and 0007. If recovered, rerun compatibility against Trendline Geometry V1 before creating an evaluator.

## Controls
- 2025 remains OOS and untouched.
- Existing Trendline Geometry and Pivot Sequence are preserved.
- 0003/0004 provenance issue remains separate.
- Similarity is historical evidence only.
