# Murphy 0001–0010 Compatibility Audit V1

Date: 2026-08-11
Source: extracted workspace artifact `extracted-workspace-workspace-v1` from Full Workspace Read run #3.

## Purpose

Compatibility audit only. No tuning, no new thresholds, and no use of 2025 OOS data.

## Findings

| Rule | Current state | Compatibility finding | Gate |
|---|---|---|---|
| MURPHY_0001 | PARTIAL / REVIEW | Existing trend-regime and break features exist, but the exact "definite reversal" operator is not frozen. | Do not evaluate PASS/FAIL until reversal gate is explicitly defined from existing architecture. |
| MURPHY_0002 | NOT_EVALUABLE | Execution/timing/process statement; no single market-structure primitive should be invented for it. | Keep as process/decision-layer condition, not a market-direction evaluator. |
| MURPHY_0003 | Evaluator exists, incomplete | Existing evaluator compares confirmed reaction troughs only. Exact mapping also requires successive reaction peaks to be higher. | Complete evaluator using existing confirmed pivot sequence; no new thresholds. |
| MURPHY_0004 | Evaluator exists, incomplete | Existing evaluator compares confirmed reaction troughs only. Exact mapping also requires successive reaction peaks to be lower. | Complete evaluator using existing confirmed pivot sequence; no new thresholds. |
| MURPHY_0005 | Feature available, definition blocked | Pivot sequence exists, but "relatively tight price band" has no approved project threshold. | Do not tune/invent threshold. Keep NOT_EVALUABLE. |
| MURPHY_0006 | Feature available, evaluator blocked | Trendline geometry outputs exist and are QA-clean, but the contract is specification-only and the third-touch/reaction operator is not frozen. | Freeze exact touch/reaction semantics before evaluator implementation. |
| MURPHY_0007 | Feature available, evaluator blocked | Same issue as 0006 for descending trendline. | Freeze exact touch/reaction semantics before evaluator implementation. |
| MURPHY_0008 | PARTIAL / REVIEW | Support/resistance and break-structure primitives exist, but "decisive break" is not operationally frozen. | Do not invent a break threshold. |
| MURPHY_0009 | PARTIAL / REVIEW | Support/resistance and break-structure primitives exist, but "decisive break" is not operationally frozen. | Do not invent a break threshold. |
| MURPHY_0010 | NOT_EVALUABLE | Trendline geometry exists as a derived module, but meaningful breakout acceptance requires an approved price/time filter that is not defined. | Keep blocked; no filter tuning. |

## Important inconsistency detected

`MARKET_STRUCTURE_RULE_COMPATIBILITY_AUDIT_V2.csv` marks Murphy 0001–0010 as `SUPPORTED_PRIMITIVE`, but the later exact-mapping / refresh artifacts correctly show several rules as only partial or requiring derived definitions/evaluators. Therefore `SUPPORTED_PRIMITIVE` must not be interpreted as `EVALUATABLE`.

## Existing artifacts confirmed

- PIVOT_SEQUENCE_V2 exists with confirmed-pivot availability timestamps and no 2025 tuning usage.
- TRENDLINE_GEOMETRY_V1 outputs exist across the available timeframes and its QA reports slope, availability, chronology and type checks as true with `no_2025=true`.
- MURPHY_0003_0004 evaluator exists and is unit-tested, but currently implements only the reaction-trough comparison portion of the exact mapping.

## Decision

P0 compatibility gate: **PASS for audit completion; FAIL for freezing Murphy 0001–0010 as fully evaluable.**

Next safe build target: complete Murphy 0003–0004 evaluator coverage for both reaction highs and lows using the existing confirmed Pivot Sequence V2. Do not change source definitions, introduce thresholds, tune parameters, or touch 2025.
