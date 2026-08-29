# Real-Source E2E Preflight Decision — 2026-08-29

Branch: decision-brain-integration-audit-2026-08-29
Purpose: close integration gaps before any expensive governed 2016-2024 profitability run.

## Confirmed project state
- Decision Brain project, not an indicator.
- Six native timeframes are fixed in the project: M5, M15, M30, H1, H4, D1.
- Murphy provides directional context.
- Nison provides confirmation/contradiction only.
- TIZ is process-only and neutral; missing process evidence is NOT_EVALUABLE.
- Historical/Similarity/Retrieval are evidence-only.
- Risk is a hard execution gate.
- 2025 is OOS-locked.

## Verified runtime discrepancy
The current CircleCI source acquisition historically downloads the legacy MTF Reader package and explicitly resolves `GBPUSD_MTF_H4_H1.csv`. That path is not equivalent to the project's six-timeframe infrastructure.

A separate Dropbox package, `/MULTI_TF_MARKET_DATA_V1.zip`, exists and is now included in the audit branch acquisition changes so the full six-timeframe source package is available to the runner/preflight. The legacy H4/H1 package is retained only for compatibility/reference.

## Dynamic MTF finding
The existing `dynamic_mtf_binding_adapter_v1.py` validates explicit role assignments against the six-timeframe contract and fails closed when roles are absent or incompatible. It does not invent a selector or scoring model. The backtest path must consume this adapter or an equivalent source-backed boundary; direct H4/H1 projection is not accepted as proof of six-timeframe consumption.

## Murphy finding
The runtime allowlist contains 34 Murphy rules, but the canonical historical fan-in manifest currently identifies only 7 rules as decision-eligible source-backed directional evidence in the reviewed 2016-2024 recovery. Other statuses must remain provenance/context/candidate/process/NOT_EVALUABLE and cannot be promoted silently.

## Risk / execution finding
The current Risk Engine requires numeric SL, TP, and ATR and enforces `CURRENT_CANONICAL_MIN_RR = 3.0`. Historical project evidence separately records a candidate execution convention of 0.75 ATR stop + 2R target. These are not interchangeable. Until a source-backed compatibility decision reconciles them, no full profitability result is official.

## Execution finding
The simplified governed runner contains its own execution construction and should not be treated as authoritative merely because it can produce trades. The canonical plan requires upstream execution inputs and frozen cost/slippage/ambiguity rules before profitability is claimed.

## Memory / Retrieval / TIZ
The current governed runner has only shadow/snapshot consumption for some memory/retrieval layers and does not yet prove a complete timestamp/as-of evidence envelope for the real runtime path. TIZ's authoritative boundary is present and process-only, but absent historical process evidence remains NOT_EVALUABLE/optional as defined by the project.

## Preflight gate
Do not run the expensive 2016-2024 backtest until a small deterministic real-source sample proves:
1. six-timeframe source package is actually consumed;
2. dynamic role binding is validated without invented selection logic;
3. Murphy/Nison evidence reaches Handoff with provenance;
4. memory/retrieval remain evidence-only and are timestamp/as-of bounded;
5. TIZ is evaluated only through its authoritative process boundary;
6. Risk is evaluated only with genuine upstream execution inputs;
7. execution SL/TP/position sizing/cost/slippage/ambiguity are sourced from a reconciled project contract;
8. 2025 is excluded.

## Current status
BLOCKED_FOR_PROFITABILITY_RUN — engineering integration preflight in progress.
This is not a strategy performance verdict.
