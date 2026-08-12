# Murphy 0006–0007 — Master KB / Rule Adapter Compatibility Audit V1

Date: 2026-08-12
Status: SEMANTICS RESOLVED / OPERATOR DEFINITION STILL BLOCKED

## Master KB finding

The project source-resolution record identifies `02_Trading_Rules/MASTER_CANDIDATE_RULES_V1.json` as the authoritative candidate rule source for MURPHY_0006 and MURPHY_0007.

0006:
- confirmed uptrend line
- successive reaction lows
- two points create tentative line
- third successful touch and reaction confirms
- decision = BULLISH

0007:
- confirmed downtrend line
- successive reaction highs
- two points create tentative line
- third successful touch and reaction confirms
- decision = BEARISH

The source cross-check also states that the confirmed line requires the third successful touch/reaction without breaking.

## Rule Adapter boundary

The current project Rule Adapter / evaluator boundary is compatible with these semantics only as an evidence consumer. It may bind:
- 0006 -> LOW + UP -> BULLISH
- 0007 -> HIGH + DOWN -> BEARISH

It must not invent a numeric definition for "touch", "reaction", or "without breaking" when the Master KB/source does not specify one.

## Compatibility result

The Master KB resolves the semantic requirements but does not provide a deterministic numeric operator for:
1. touch tolerance;
2. successful reaction magnitude/distance;
3. reaction duration/lookback;
4. no-break implementation threshold.

The existing Geometry V1 output was verified separately to contain line geometry and availability only; it does not expose third-touch/reaction/no-break fields.

Therefore there is currently no source-backed path from canonical Geometry V1 rows to the evaluator's required booleans without an explicit additional derivation contract.

## Decision

DO NOT modify Geometry V1.
DO NOT modify the existing evaluator to invent thresholds.
DO NOT promote candidate evidence to PASS/FAIL.
Keep the production confirmation operator `NOT_EVALUABLE`.

The remaining engineering task is not to "find" a hidden existing operator; it is to determine whether an already-authorized project contract elsewhere explicitly defines these semantics. If no such contract exists, the correct state is blocked pending a source-backed operator specification.

## Leakage / OOS controls

Use only confirmed evidence available at the relevant availability timestamp.
2025 remains OOS and cannot be used to tune or select an operator.

## Closure criteria

The gate can close only when an authoritative project/source artifact defines all required deterministic semantics, after which a compatibility implementation and tests can be added without changing existing components.
