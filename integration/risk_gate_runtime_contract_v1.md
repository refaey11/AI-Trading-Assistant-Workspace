# Runtime Risk Gate Wiring Contract V1

Status: IMPLEMENTED CONTRACT / NOT FROZEN

## Purpose
Wire authoritative Risk Engine outputs into Murphy rules 0042-0044 without duplicating the Risk Engine or inventing thresholds.

## Required runtime inputs
- total_capital
- total_investment
- market_exposure
- market_risk
- evidence provenance/timestamp

## Rule mapping
- 0042: total_investment <= 50% of total_capital => PASS; otherwise FAIL.
- 0043: market_exposure within authoritative 10%-15% range => PASS; >15% => FAIL; below 10% is NOT_EVALUABLE unless an authoritative source explicitly defines it as a violation.
- 0044: market_risk <= 5% => PASS; otherwise FAIL.

## Fail-closed behavior
- Missing required runtime field => needs_review / NOT_EVALUABLE.
- Stale or causally unavailable evidence => needs_review / NOT_EVALUABLE.
- Explicit risk violation => execution BLOCKED.
- Nison, Similarity Memory, or narrative text cannot override a Risk FAIL.

## Architecture
Risk Engine -> Rule Adapter -> Hard Risk Gate -> Decision Brain.
No duplicate Risk Engine is created by this integration.

## Test vectors required
1. 0042: 50% PASS / 50%+ FAIL / missing NOT_EVALUABLE.
2. 0043: 10% PASS / 15% PASS / >15% FAIL / below 10% NOT_EVALUABLE / missing NOT_EVALUABLE.
3. 0044: 5% PASS / >5% FAIL / missing NOT_EVALUABLE.
4. Any FAIL must produce execution BLOCKED.
5. Any missing/stale evidence must never produce PASS.

## Governance
No tuning, calibration, or threshold selection is introduced here. 2025 remains OOS and excluded from tuning, calibration, optimization, and operator selection.
