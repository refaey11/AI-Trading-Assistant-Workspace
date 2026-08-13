# Murphy 0006–0007 — Full Workspace Audit V1

Date: 2026-08-13
Status: DEEP AUDIT COMPLETE / FINAL OPERATOR GAP NARROWED

## Scope actually inspected

Local project archives and accessible workspace artifacts were inspected at file/content level, including:
- 21 ZIP archives available in the workspace, 7,494 archived members before duplicate/metadata normalization.
- John Murphy source archive (298 members).
- MASTER_KB_V1 (1,182 members).
- TRADING_RULES_V2 (6 members).
- 3_BOOK_INTEGRATION_V1 (1,183 members).
- GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_RECONSTRUCTED and V2 (241 members each; CRC/file-size comparison shows identical member content).
- Historical Context/Outcome Memory, Similarity, Market State/Reader, Scenario Engine, MTF Reader, Nison modules, True Backtest, and continuation/handoff artifacts.
- Standalone 0006/0007 candidate evidence V2/V3/V4, rule adapter, rule adapter contract, refresh contract, and refresh CSV.

GitHub branch/history and the workspace release were also checked where connector access allowed.

## Major finding #1 — Pivot availability is actually specified in PIVOT_SEQUENCE_V2

`PIVOT_SEQUENCE_V2_OUTPUT/PIVOT_SEQUENCE_CONTRACT_V2.json` states:
- confirmation rule = 2 confirming bars;
- availability timestamp = pivot event row + 2 bars in the same source timeframe;
- pivot evidence unavailable before that confirmation timestamp;
- 2025 not used.

This means the old V1 `PIVOT_CONFIRMATION_AVAILABILITY_CONTRACT_V1.json` blocker is superseded for the built V2 lineage. The production availability problem is therefore NOT the primary remaining blocker, provided the V2 lineage is the one used and its source provenance is retained.

## Major finding #2 — Trendline Geometry is built and no longer the blocker

`TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json` states:
- input = PIVOT_SEQUENCE_V2;
- lines are generated from consecutive same-type pivots;
- exact slope calculation;
- availability = later confirmation timestamp of the two anchors;
- breakout detection excluded;
- thresholds added = false;
- no lookahead.

The geometry contract explicitly prohibits inventing tolerance, minimum-touch count, angle, or breakout thresholds.

## Major finding #3 — Original 0006/0007 records are recovered and source semantics are clear

MASTER_KB and TRADING_RULES_V2 contain the original records:
- 0006 = Confirmed uptrend line; reaction lows; upward slope; two tentative points; third successful touch and reaction; BULLISH; `confirmation=[]` and `missing_fields=[confirmation]` in V2.
- 0007 = Confirmed downtrend line; reaction highs; downward slope; two tentative points; third successful touch and reaction; BEARISH; same missing confirmation field.

The integrated registry duplicates these records but marks primary_source as UNATTRIBUTED / needs_source_review; it must not be treated as a stronger source than the original rule record.

## Major finding #4 — Murphy Chapter 4 source artifacts contain explicit trendline filter semantics

The Chapter 4 source artifacts contain:
- tentative line = 2 points;
- confirmed trendline = third successful touch and reaction without breaking;
- trendlines should enclose the daily price range;
- intraday penetration is distinguished from closing breaks;
- price filter example = 3% closing price penetration for major trends and 1% for short-term;
- time filter = 2 consecutive daily closes beyond trendline.

The Chapter 4 JSON/SQL are more explicit than the 0006/0007 rule records about general trendline break filters.

IMPORTANT: these filters are source-backed general trendline semantics, but the project still has no explicit rule-level binding that says which filter policy is to be used specifically for 0006/0007. Therefore do not silently choose 3% major, 1% short-term, or a 2-day policy as the 0006/0007 production operator without an explicit binding decision.

## Major finding #5 — The existing candidate evidence already contains most raw observables

`MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv`:
- 347 rows total;
- 166 MURPHY_0006;
- 181 MURPHY_0007;
- all rows `CANDIDATE_ONLY`;
- all rows `OBSERVATION_ONLY` for no-break;
- 340 directional reaction observations true, 6 false, 1 missing;
- 62 daily-range/line intersections, 285 non-intersections.

Fields include:
- anchors and availability;
- candidate pivot type/price;
- line price at candidate;
- signed/absolute distance;
- daily high/low;
- daily range intersection;
- reaction candidate timestamp/type;
- directional reaction consistency;
- no-break observation.

The adapter intentionally does not promote these observations to PASS/FAIL.

## Major finding #6 — The refresh artifacts do NOT solve 0006/0007

`MURPHY_REFRESH_UNBLOCKED_CONDITIONS_V1.csv` contains refreshed rows for 0021, 0027, 0028, 0029, 0050, 0022, 0023; it does NOT contain 0006 or 0007.

`MURPHY_51_RULE_LEVEL_REFRESH_V1.csv` marks 0006 and 0007 as `UNBLOCKED — EVALUATOR/DEFINITION STILL REQUIRED` while its `remaining_definition_or_evaluator_gaps` field is `0`. This is internally inconsistent. The status text and existing exact mapping must be treated as authoritative evidence that the evaluator/definition gap remains; the numeric zero must not be interpreted as closure.

## Major finding #7 — The dedicated evaluator workspace confirms the exact remaining gap

`MURPHY_0006_TO_0010_EXACT_MAPPING_V1.csv` explicitly records:
- third successful touch/reaction operator = `third touch followed by reaction away from line`;
- status = `NOT_YET_EVALUABLE`;
- reason = successful touch and reaction needs an approved operational definition.

`MURPHY_51_EXACT_RULE_EVALUATOR_CONTRACT_V1.json` requires an explicit feature + operator for every condition and says missing definitions remain NOT_EVALUABLE.

## Final technical conclusion

The blocker has narrowed from four unknowns to two real operator decisions:

1. SUCCESSFUL TOUCH / REACTION operator:
   - raw candidate pivot, line geometry, distance, range intersection and directional reaction evidence exist;
   - source semantics say third successful touch + reaction;
   - no approved project operator maps the raw fields to a deterministic success predicate.

2. NO-BREAK binding:
   - Murphy Chapter 4 supplies general closing/break filter semantics;
   - project artifacts do not explicitly bind one of those policies to 0006/0007;
   - therefore a final no-break predicate is still not source/project-locked.

Availability itself is no longer the main gap because PIVOT_SEQUENCE_V2 specifies the two-bar confirmation/availability lineage.

## What must NOT be done

- Do not rebuild Pivot V2 or Geometry V1.
- Do not use the older V1 availability blocker as if V2 did not exist.
- Do not invent touch tolerance, reaction magnitude, ATR, pip, lookback, or timeframe.
- Do not silently select 3%, 1%, or 2-day as the 0006/0007 production break policy.
- Do not tune on 2025.
- Do not convert candidate evidence into PASS/FAIL until the operator binding is explicitly approved.

## Next exact action

Create a source-binding proposal containing only source-backed choices:
- candidate third touch evidence = confirmed same-type pivot after line availability + line interaction evidence;
- reaction evidence = subsequent directionally consistent reaction candidate;
- no-break alternatives = explicit Murphy closing/filter semantics from Chapter 4, with the binding decision recorded rather than guessed.

Then run a compatibility gate. If the project accepts one of the source-backed break policies, implement the smallest evaluator and tests. If not, retain NOT_EVALUABLE.

2025 remains OOS.
