# NISON 2025 Runtime Status Handoff — 2026-08-24

## Purpose

Checkpoint the current Nison 2025 production-state investigation before further integration work. This is an audit/handoff record only. It does not tune rules, invent thresholds, or alter the 2025 OOS policy.

## Source of truth examined

Authoritative production runner currently present in the repository:

- `OOS_2025/nison_2025_runtime_producer_v1.py`
- `OOS_2025/nison_2025_source_adapter_v1.py`
- existing `RUNTIME/NISON_EVALUATORS_V1/*` evaluators

The production runner delegates evaluation to the existing Nison runtime/router and evidence bridge. Missing inputs are intentionally allowed to remain `NOT_EVALUABLE`; the producer explicitly states that it must not invent formation facts, thresholds, or direction.

## 2025 production result observed

Input scope:

- GBPUSD H1
- 2025 only
- 6,225 timestamps
- 44 governed Nison rules
- 273,900 evidence rows
- lookahead policy: `none`
- OOS policy: `2025 is evaluation-only; no tuning or threshold selection`

Observed status counts:

- `FAIL`: 83,298 (30.41%)
- `NOT_EVALUABLE`: 190,602 (69.59%)

No `PASS` rows were produced in the observed run.

## Coverage result

### Zero coverage: 18 rules

`NISON_0021` through `NISON_0031`, plus `NISON_0038` through `NISON_0044`.

Primary reasons observed:

- source-backed upstream formation facts absent
- existing uptrend/formation-completion facts absent
- five-candle continuation structure absent
- previous/current session OHLC and direction absent
- methodology evidence unavailable

### Very low coverage

Several two-candle rules were effectively evaluated only at the first eligible history boundary because the source adapter was passing a truncated recent candle window while the runtime contracts reported `requires exactly 2 candles`.

### Partial/high coverage

Other rules were evaluable where the currently available OHLC/context fields matched their runtime contracts.

## Market State contract audit

The current market-state dataset provides:

- timestamp
- OHLCV
- EMA/ATR context
- trend
- structure_event
- volume/volatility state
- support/resistance distance
- location
- selected candle flags
- market_interpretation

It does **not** provide the following upstream Nison inputs expected by some runtime contracts:

- `formation_confirmed`
- `formation_complete`
- `final_bullish_strong`
- `final_bearish_strong`
- `evidence_available`
- `role`
- `previous_session`
- `current_session`
- `direction`
- nested source-backed `context`, `candlestick`, or `confirmation` facts

Therefore the current 18 zero-coverage rules must not be made evaluable by inventing those values from ad-hoc thresholds.

## Existing adapter capability

`nison_2025_source_adapter_v1.py` already has a runtime boundary capable of passing these fields through **if an authoritative upstream producer supplies them**.

The immediate integration problem is therefore not to create another Nison evaluator. The missing work is to locate and/or connect authoritative upstream producers for formation/session/methodology evidence to the existing adapter contract.

## Decision

1. Keep all existing Nison runtime contracts authoritative.
2. Keep `2025` evaluation-only; no tuning or threshold selection.
3. Do not fabricate formation, confirmation, session, methodology, or directional facts.
4. Audit existing project artifacts and producers before implementing any new producer.
5. If no authoritative producer exists for a required fact, keep the affected rule fail-closed / `NOT_EVALUABLE` rather than synthesizing unsupported evidence.
6. The next engineering step is a compatibility audit of the upstream evidence path for `NISON_0021..0031` and `NISON_0038..0044`.

## Current project status

- Nison 44-rule runtime: present.
- Nison production runner: present.
- Source adapter: present.
- 2025 production execution: completed and audited.
- Main blocker: authoritative upstream evidence coverage for the 18 zero-coverage rules.
- No rebuild of existing Nison knowledge is authorized.

## Next action

Inspect the repository for existing producers/contracts that can emit the missing source-backed facts and map only compatible outputs into the current Nison adapter. Any integration must pass a compatibility audit before code changes.
