# Event Time Availability Contract V1

## Purpose

Define the minimum source metadata required before a historical evidence row may be consumed at a decision time. The contract is fail-closed and source-neutral. It does not change Murphy, Nison, Market State, MTF, Brain, TIZ, Similarity, or Risk semantics.

## Required fields per evidence row

| Field | Meaning |
|---|---|
| `source_id` | Stable evidence source name, e.g. H1, MTF_M5, MURPHY, NISON, MARKET_STATE |
| `producer_id` | Exact producer or transformation version |
| `source_ref` | Traceable source file/row or immutable provenance reference |
| `timestamp_label_semantics` | Explicitly one of BAR_OPEN, BAR_CLOSE, EVALUATION_TIME |
| `source_timestamp` | Timestamp label actually present in the source row |
| `bar_open_time` | Start of the source bar represented by the evidence |
| `bar_close_time` | End/close time of that source bar |
| `available_at` | Earliest time the completed evidence was actually available to the decision process |

All timestamps must be timezone-aware ISO-8601 values. The label must match its declared semantics:
- BAR_OPEN: source_timestamp == bar_open_time
- BAR_CLOSE: source_timestamp == bar_close_time
- EVALUATION_TIME: source_timestamp == available_at

## Eligibility rules

An evidence row is eligible only if:
1. `bar_open_time < bar_close_time`
2. `available_at >= bar_close_time`
3. `bar_close_time <= decision_time`
4. `available_at <= decision_time`
5. the source label matches its explicit semantics.

A bundle is eligible for downstream evaluation only if every required source is present and every evidence row passes. Otherwise the result is NOT_EVALUABLE. This is an evidence-timing gate, not a BUY/SELL or trade authorization.

## Important constraints

- Do not infer BAR_OPEN or BAR_CLOSE from timestamp spacing, filename, or apparent alignment.
- Do not shift H1, MTF, Murphy, Nison, or Market State timestamps by a guessed fixed interval.
- For derived/multi-timeframe evidence, each contributing source must retain its own provenance and availability; the aggregate is not available before all required inputs are available.
- Do not substitute the separate H1/H4 research-only MTF Reader for Gate3C's six-timeframe alignment archive.
- Missing producer metadata means NOT_EVALUABLE, not an imputed availability time.
- A successful contract test proves the validator behavior only; it does not prove that current historical archives already satisfy the contract.

## Scope of this PR

This PR adds a pure validator, synthetic tests, and focused CI. It does not wire the contract into Gate3C runtime because the current historical outputs expose timestamp labels but do not yet establish producer-level bar-close and earliest-availability semantics. Runtime integration must wait for source-backed producer contracts and a separately reviewed compatibility audit.

## Dataset governance

All development-only validation must stay within 2016-2024. 2025 remains frozen OOS and must not be used for tuning, calibration, or implementation decisions. No historical data is changed by this PR.
