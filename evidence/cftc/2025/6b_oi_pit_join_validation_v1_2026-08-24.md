# CFTC 6B OI 2025 — PIT Join Validation V1

Date: 2026-08-24
Contract: British Pound Futures
CFTC contract market code: 096742

## Purpose
Validate that each retained 2025 OI observation has a publication/availability timestamp before it can be consumed by Murphy rules 0022/0023.

## Rules
- Never equate `report_date` with `available_time`.
- No interpolation.
- No Spot-FX OI proxy.
- No inferred publication timestamp when an authoritative CFTC exception/catch-up schedule exists.
- OOS 2025 remains NOT_EVALUABLE until the materialized evidence rows pass both value completeness and PIT binding.

## Current evidence state
- Expected CFTC 2025 report-date inventory: 51 retained report dates after excluding the non-independent 2025-11-11 catch-up label.
- Previously materialized web-verified numeric observations in repository artifact: 37.
- PIT publication schedule: 51/51 dates mapped to an authoritative or officially specified availability date/time.
- Therefore value completeness is currently 37/51, while PIT timestamp coverage is 51/51.

## Gate result
STATUS: BLOCKED

Reason: 14 numeric OI observations are not present in the materialized evidence artifact currently available to the evaluator. Publication-time mapping alone does not make the missing values usable.

## Required next gate
1. Materialize the missing 14 numeric 096742 OI observations from authoritative CFTC reports.
2. Recompute row count and checksum.
3. Perform deterministic PIT join.
4. Run Murphy 0022/0023 evaluator.
5. Only then update 2025 coverage from NOT_EVALUABLE.

This artifact intentionally does not claim USABLE coverage before the evaluator consumes the complete materialized dataset.
