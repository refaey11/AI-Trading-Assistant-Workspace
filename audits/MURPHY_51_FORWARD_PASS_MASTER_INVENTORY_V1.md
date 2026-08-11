# Murphy 51 Forward Pass — Master Inventory V1

Date: 2026-08-12

## Purpose

Move through all 51 Murphy rules without allowing one unresolved rule to stall the project. Existing components are reused; unresolved items are recorded for revisit. No new thresholds or semantics are invented.

## Current verified inventory

| Rule | Current workspace status | Dedicated evaluator | Forward-pass action |
|---|---|---:|---|
| 0001 | PARTIAL | No | Source/compatibility review |
| 0002 | NOT_EVALUABLE | No | Source/operator recovery |
| 0003 | REQUIRES_DERIVED_FEATURE | Yes | Existing V2 + tests; provenance separate |
| 0004 | REQUIRES_DERIVED_FEATURE | No | Existing V2 lineage; provenance separate |
| 0005 | NOT_EVALUABLE | No | Source/operator recovery |
| 0006 | NOT_YET_EVALUABLE | No | Working mapping resolved; geometry evidence review |
| 0007 | NOT_YET_EVALUABLE | No | Working mapping resolved; geometry evidence review |
| 0008 | PARTIAL | No | Source/operator recovery |
| 0009 | PARTIAL | No | Source/operator recovery |
| 0010 | NOT_EVALUABLE | No | Time/price filter source review |
| 0011 | PARTIAL | No | Source definition recovery |
| 0012 | NOT_YET_EVALUABLE | No | Source definition recovery |
| 0013 | NOT_YET_EVALUABLE | No | Source definition recovery |
| 0014 | REQUIRES_DERIVED_FEATURE | No | Derived-feature contract recovery |
| 0015 | REQUIRES_DERIVED_FEATURE | No | Derived-feature contract recovery |
| 0016 | NOT_YET_EVALUABLE / REQUIRES_DERIVED_FEATURE | No | Source + feature contract |
| 0017 | REQUIRES_DERIVED_FEATURE | No | Derived-feature contract |
| 0018 | REQUIRES_DERIVED_FEATURE | No | Derived-feature contract |
| 0019 | REQUIRES_DERIVED_FEATURE | No | Derived-feature contract |
| 0020 | NOT_YET_EVALUABLE | No | Source/operator recovery |
| 0021 | PARTIAL | Yes | Existing evaluator + unit tests; compatibility/integration review |
| 0022 | EVALUATABLE_AFTER_FEATURE_SCHEMA_CONFIRMATION / NOT_EVALUABLE / PARTIAL | No | Confirm feature schema; reuse existing evaluator module |
| 0023 | EVALUATABLE_AFTER_FEATURE_SCHEMA_CONFIRMATION / NOT_EVALUABLE / PARTIAL | No | Confirm feature schema; reuse existing evaluator module |
| 0024 | PARTIAL | No | Source/operator recovery |
| 0025 | NOT_YET_EVALUABLE | No | Source/operator recovery |
| 0026 | NOT_YET_EVALUABLE | No | Source/operator recovery |
| 0027 | PARTIAL | Yes | Existing evaluator intentionally blocked pending exact regime operator |
| 0028 | NOT_YET_EVALUABLE / PARTIAL | No | Confirm divergence feature contract |
| 0029 | NOT_YET_EVALUABLE / PARTIAL | No | Confirm divergence feature contract |
| 0030 | NOT_EVALUABLE | No | Source/operator recovery |
| 0031 | NOT_EVALUABLE | No | Source/operator recovery |
| 0032 | NOT_EVALUABLE | No | Source/operator recovery |
| 0033 | PARTIAL | No | Source/operator recovery |
| 0034 | NOT_EVALUABLE | No | Source/operator recovery |
| 0035 | NOT_EVALUABLE | No | Source/operator recovery |
| 0036 | NOT_EVALUABLE | No | Source/operator recovery |
| 0037 | PARTIAL | No | Source/operator recovery |
| 0038 | NOT_EVALUABLE | No | Source/operator recovery |
| 0039 | PARTIAL | No | Source/operator recovery |
| 0040 | NOT_EVALUABLE | No | Source/operator recovery |
| 0041 | NOT_YET_EVALUABLE | No | Source/operator recovery |
| 0042 | PARTIAL | No | Source/operator recovery |
| 0043 | PARTIAL | No | Source/operator recovery |
| 0044 | PARTIAL | No | Source/operator recovery |
| 0045 | PARTIAL | No | Source/operator recovery |
| 0046 | NOT_EVALUABLE / PARTIAL | No | Source/operator recovery |
| 0047 | NOT_EVALUABLE | No | Source/operator recovery |
| 0048 | NOT_EVALUABLE | No | Source/operator recovery |
| 0049 | NOT_EVALUABLE | No | Source/operator recovery |
| 0050 | NOT_EVALUABLE / PARTIAL | Yes | Existing evidence matrix; upstream gaps remain |
| 0051 | PARTIAL | No | Source/operator recovery |

## Existing evaluator evidence already found

### 0021–0023
The workspace contains `MURPHY_0021_0023_EVALUATOR_CONTRACT_V1.json`, marked implemented and unit tested. The operationalization uses existing price/volume/OI evidence, explicitly adds no thresholds, uses runtime/dynamic MTF, and records `2025_used: false`. Historical evaluation artifacts for 2020–2024 are present.

### 0027–0029
The workspace contains a 0027–0029 evaluator/test package. Rule 0027 is intentionally returned as NOT_EVALUABLE until the exact trend-vs-ranging regime operator is approved; the evaluator explicitly refuses to invent an ADX threshold or fixed timeframe. Tests for 0028/0029 divergence cases are present.

### 0050
The workspace contains `MURPHY_0050_CURRENT_EVIDENCE_MATRIX_V1.csv`. Current evidence includes general trend, volume/open interest, and partial trendline evidence; breadth, exact combined retracement/gap evidence, exact reversal/continuation pattern evidence, and confirmed moving-average evidence remain unavailable/partial. Do not add indicators merely to satisfy 0050.

## Non-negotiable controls

- Workspace/File Library remains Source of Truth.
- Existing components are not rebuilt.
- Compatibility audit precedes every integration.
- No invented thresholds or operators.
- 2025 is OOS and never used for tuning or implementation selection.
- Murphy 0003/0004 provenance remains a separate issue and must not be altered to force old results.
- Similarity is evidence/memory only; it cannot create a trade direction by itself.
- Murphy supplies context; Nison supplies confirmation; Trading in the Zone supplies process/psychology gating; Risk is a hard gate.

## Forward-pass policy

1. Close rules whose source and existing upstream artifacts are sufficient.
2. For rules with missing source/operator/feature contracts, record the exact blocker and continue.
3. Revisit all deferred rules after the full 51-rule pass.
4. Only after required rule/evidence gates are closed should the official uniform walk-forward and final Decision Brain freeze proceed.

## Current project conclusion

The project has a complete 51-rule inventory and is no longer blocked on a single Murphy rule. The forward pass is active. The next work is to resolve the source/feature contracts for the rules above and integrate only those components that are already supported by the project's evidence lineage.
