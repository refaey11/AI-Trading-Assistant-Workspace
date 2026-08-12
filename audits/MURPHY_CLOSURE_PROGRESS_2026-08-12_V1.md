# Murphy Closure Progress — 2026-08-12 V1

## Purpose
Source-backed closure board for the current Murphy verification sprint. This file records what can be advanced from existing evidence and what remains blocked. It does not promote any rule to FROZEN by status alone.

## Hard controls
- Workspace/project files remain Source of Truth.
- Reuse existing components; compatibility audit before integration.
- Do not invent thresholds, operators, fixed timeframes, proxies, or semantic splits.
- 2025 is OOS and excluded from tuning, implementation selection, feature optimization, and fitting.
- Similarity is historical evidence only.

## 0001–0007
- 0001: PARTIAL — trend_regime and break_structure mappings exist; exact "definite reversal" operator is not source-frozen.
- 0002: NOT_EVALUABLE — source mapping exists as an execution/timing/process statement, but current source evidence does not freeze an exact implementation. No evaluator authorized yet.
- 0003–0004: corrected V2 evaluator/tests exist, but provenance/semantic reconciliation remains unresolved; MUST remain NOT_FROZEN.
- 0005: NOT_EVALUABLE — source row not currently retrievable.
- 0006–0007: working mapping is LOW+UP→BULLISH and HIGH+DOWN→BEARISH, but the authoritative source lock and operational definition of third successful touch/reaction are not proven. Existing Trendline Geometry V1 is reused; no new geometry or threshold is created.

## 0008–0014
Source semantics are resolved for the following rules, but evaluator/selection contracts are not yet closed:
- 0008: decisive support break → later rally toward broken support = bearish role reversal.
- 0009: decisive resistance break → later pullback toward broken resistance = bullish role reversal.
- 0010: trendline price penetration must be filtered; source allows price or time filter, but project contract must select the existing compatible family.
- 0013: symmetrical triangle: ≥4 reversal points; upper boundary descends; lower boundary ascends; breakout typically around 2/3–3/4 of horizontal width.
- 0014: ascending triangle: horizontal resistance + rising lows; ≥4 reversal points; upside breakout/close beyond resistance confirms bullish direction.
No new evaluator is created where an existing compatible component is not yet proven.

## 0015–0020
- 0015, 0017, 0018, 0019: REQUIRES_DERIVED_FEATURE.
- 0016: NOT_YET_EVALUABLE / derived feature.
- 0020: NOT_YET_EVALUABLE.
Feature Engineering V2 is an existing core component and must be inspected for compatible existing features before any new feature is proposed.

## 0021–0023
Existing evaluator is implemented and unit-tested. It uses completed-bar price direction, existing volume_direction, and existing CFTC futures OI direction; no new thresholds or spot-FX OI proxy. Dynamic MTF is runtime-selected rather than hard-coded. Historical artifacts exist for 2020–2024; 2025_used=false. These are evaluator-ready candidates, but official freeze still requires the project's complete freeze/provenance acceptance.

## 0024–0026
- 0024: PARTIAL.
- 0025: NOT_YET_EVALUABLE.
- 0026: NOT_YET_EVALUABLE.
Feature Engineering V2 compatibility remains the next legitimate check; no invented derived feature.

## 0027–0029
- 0027: BLOCKED / NOT_EVALUABLE until an exact trend-vs-range regime operator is source-approved; no invented ADX threshold or fixed timeframe.
- 0028: evaluator + tests pass for confirmed BEARISH divergence at HIGH pivot; historical summary records 1,592 confirmed events; 2025_used=false.
- 0029: evaluator + tests pass for confirmed BULLISH divergence at LOW pivot; historical summary records 1,644 confirmed events; 2025_used=false.
0028–0029 remain Freeze Candidates, not Production Frozen, until official freeze-manifest acceptance is recorded.

## 0030–0051
Current verified status registry:
- 0030–0032 NOT_EVALUABLE
- 0033 PARTIAL
- 0034–0036 NOT_EVALUABLE
- 0037 PARTIAL
- 0038 NOT_EVALUABLE
- 0039 PARTIAL
- 0040 NOT_EVALUABLE
- 0041 NOT_YET_EVALUABLE
- 0042–0045 PARTIAL
- 0046 NOT_EVALUABLE / PARTIAL
- 0047–0049 NOT_EVALUABLE
- 0050 NOT_EVALUABLE / PARTIAL; structural evaluator exists but combined evidence contract is incomplete
- 0051 PARTIAL

## Current closure decision
This pass does NOT justify claiming 51/51 Murphy Frozen. It does establish a tighter closure queue and prevents repeated inventory work.

The highest-value remaining work is:
1. recover authoritative 0006–0007 source records and close the third-touch/reaction contract if supported;
2. perform Feature Engineering V2 compatibility checks for 0015–0019 and 0024–0026;
3. close evaluator contracts for source-resolved 0008–0014 using existing compatible components only;
4. keep 0027 and 0050 explicitly blocked where their exact evidence contracts are incomplete;
5. run tests + 2016–2024 historical QA only after operator contracts are source-locked;
6. reconcile official freeze status for all eligible rules.

## Integrity note
A rule is not frozen merely because a mapping, evaluator, or historical CSV exists. The required chain remains:
Workspace → Mapping → Feature → Dynamic MTF → Operator/Logic → Evaluator → Tests → Historical/Provenance QA → Official Freeze.
