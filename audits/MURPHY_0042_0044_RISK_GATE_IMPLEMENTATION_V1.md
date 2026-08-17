# Murphy 0042–0044 Risk Gate Implementation V1

Status: INTEGRATION-READY / NOT PRODUCTION FROZEN

## Source-locked semantics
- 0042: total investment must not exceed 50% of available capital; capital reserve guideline.
- 0043: single-market entry/exposure is stated as 10%–15% of total capital.
- 0044: risk exposure in a single market is limited to 5% of total capital.

Independent MT5 archive provenance agrees with the Master KB records.

## Implementation boundary
This layer does NOT invent a new Risk Engine. It maps authoritative risk evidence into the existing Rule Adapter / Decision Brain gate.

Inputs:
- rule_id
- risk evidence
- risk_available
- risk_status
- source metadata
- availability timestamp

Outputs:
- module=murphy_risk
- source_rule_id
- available
- gate=pass|fail|needs_review
- conflict=neutral|insufficient
- source-backed statement

## Range handling
0043 is a source range (10%–15%), not a project-selected single threshold. Therefore the adapter must not silently select 10% or 15% as a universal software threshold.

Interim source-safe interpretation:
- evidence above the stated upper bound is FAIL;
- evidence within the stated source range is compatible;
- evidence below the lower guideline boundary is NOT automatically a violation;
- missing evidence is NOT_EVALUABLE / needs_review.

Any stricter project policy requires explicit governance approval and is outside this adapter.

## Hard precedence
Risk FAIL blocks execution.
Nison cannot override risk.
Similarity cannot override risk.
Missing risk evidence cannot become PASS.
2025 remains OOS and is excluded from tuning/selection.

## Deterministic gate cases
1. PASS evidence -> available=true, gate=pass.
2. FAIL evidence -> available=true, gate=fail.
3. Missing evidence -> available=false, gate=needs_review.
4. Unsupported status -> available=false, gate=needs_review.
5. Bullish/bearish market evidence with risk FAIL -> gate remains fail.

## Closure
Source/provenance: RESOLVED.
Integration contract: IMPLEMENTED.
Historical rule-level QA: PENDING.
Availability/leakage audit: PENDING.
Production freeze: NOT CLAIMED.
