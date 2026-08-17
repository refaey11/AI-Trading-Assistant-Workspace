# Murphy 0042-0045 — Risk Gate Integration Test Plan V1

Status: IMPLEMENTATION-READY / NOT FROZEN

## Purpose
Integrate the existing Risk Engine through the existing Rule Adapter without rebuilding either component.

## Source-locked rule semantics
- 0042: total investment must not exceed 50% of available capital.
- 0043: single-market entry is limited to the source-stated 10%–15% range.
- 0044: risk exposure in a single market is limited to 5% of total capital.
- 0045: total margin is limited to the source-stated 20%–25% range.

The 10%–15% and 20%–25% ranges are source ranges. This plan does not silently select a single project threshold.

## Adapter behavior
Input comes from the authoritative existing Risk Engine. The adapter only normalizes the result:
- PASS -> gate=pass, available=true
- FAIL -> gate=fail, available=true, execution_blocked=true
- NOT_EVALUABLE/missing -> gate=needs_review, available=false, execution_blocked=true

No PASS may be inferred from field presence, text, or missing data.

## Required tests
T1 PASS reaches gate=pass.
T2 FAIL reaches gate=fail and blocks execution.
T3 missing evidence reaches needs_review and blocks execution.
T4 unsupported status reaches needs_review and blocks execution.
T5 Similarity support cannot override risk FAIL.
T6 bullish/bearish Murphy evidence cannot override risk FAIL.
T7 no rule-specific risk result may be synthesized by the adapter.
T8 2025 metadata cannot trigger tuning/threshold selection.

## Availability / leakage
Risk evidence must carry an availability timestamp. The adapter must reject evidence that is unavailable at the decision timestamp. No future state may be consumed.

## Freeze gate
This artifact does not freeze 0042–0045. Production freeze additionally requires implementation tests, 2016–2024 QA where applicable, availability/leakage audit, provenance manifest, and explicit freeze decision.
