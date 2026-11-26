# Forex Demo MVP — 7-Day Execution Plan

**Date:** 2026-11-26  
**Status:** PLAN ONLY — NO SOURCE/RUNTIME IMPLEMENTATION AUTHORIZED BY THIS DOCUMENT  
**Target environment:** User-owned Windows PC + MT5 Demo  
**Market scope:** Forex only; one broker Demo account; one symbol for initial validation  
**Protected scope:** `main`, frozen Murphy/Nison knowledge, canonical risk contracts, historical source archives, and 2025 OOS.

## 1. Executive decision

A complete autonomous AI Decision Brain with trustworthy live data, validated setup generation, broker-aware risk sizing, automatic MT5 order management, recovery, and production-grade monitoring is **not realistically deliverable in seven days** from the currently verified repository state.

A seven-day target can only be treated as a **conditional engineering sprint** toward a narrowly scoped Demo proof:
- establish a local Windows/MT5 Demo environment;
- verify live quote and closed-bar acquisition;
- freeze one explicit entry/setup rule and its source/semantics;
- implement an isolated Demo-only order adapter only after a separate implementation approval;
- prove order open/modify/close and fail-safe behavior;
- keep all real-money trading disabled.

If the source/entry rule or broker integration gate fails, the correct outcome is **NO_TRADE / NOT READY**, not a fabricated successful launch.

## 2. Repository compatibility findings (verified 2026-11-26)

### Existing reusable work
- The canonical project branch is `current-stack-dev-backtest-2016-2024-v3`, observed at commit `34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e`.
- Murphy/Nison knowledge and governance already exist; do not rebuild them.
- PR #120 branch `feature/live-decision-runtime-v1` contains a Live Decision Runtime V1 candidate.
- PR #144 branch `fix/wp2-murphy-exclusive-direction-2026-11-25` contains a validation-only candidate that makes Murphy the exclusive directional authority and TIZ optional metadata.
- The Live Decision Runtime consumes an already assembled source-backed event and returns a signal / fail-closed result. It explicitly has `orders_enabled=False`; it does not send broker orders.
- Canonical Risk Engine integration validates supplied Entry, SL, TP, ATR, equity, drawdown and minimum RR 3.0. It does not independently create a market setup or broker-specific lot size.
- `risk_engine/risk_execution_runtime_v1.py` converts supplied entry and stop/target distances into levels; it does not discover the entry or structure-derived stop distance.
- Existing candidate PRs remain Draft/open/unmerged. They are not treated as integrated production components.

### Blocking gaps for autonomous Demo trading
1. No verified, integrated MT5 order execution adapter / position manager is present in the canonical branch.
2. No broker-specific lot sizing and contract-property validation has been proven. Generic `position_size` is not assumed to equal MT5 lots.
3. The live decision runtime requires a complete MTF event. The exact six-timeframe producer semantics, timestamp availability, and missing-value lineage remain unresolved in the audit record.
4. The existing runtime does not generate Entry/SL/TP. A source-backed setup-generation rule must be selected and approved before implementation.
5. MT5 Raw Capture V1.3 is a raw capture utility, not an execution adapter. It uses raw unverified MT5 time and has known restart/catch-up limitations.
6. The D0 read-only diagnostic script is not compiled or run. It requires desktop MT5/MetaEditor on Windows and only checks bounded CopyRates repeatability; it does not prove recovery or execution readiness.
7. The live-runtime candidate PRs are validation candidates, not merged, and must undergo compatibility review before any integration.

## 3. Seven-day gated work plan

### Day 1 — Local environment and broker handshake
- Confirm Windows version, MT5 Desktop installation, broker Demo server, and terminal build.
- Confirm terminal can log into Demo and display the selected Forex symbol.
- Record symbol's exact broker name, digits, point, tick size/value, contract size, minimum/maximum/step volume, stops level, freeze level, execution mode, and trading sessions.
- Do not store passwords, investor credentials, or account numbers in GitHub or chat.
- Gate D1: Demo terminal connected; broker/symbol metadata captured without exposing credentials.

### Day 2 — Read-only market-data proof
- Review the D0 script and operator guide from the MT5 recovery specification branch.
- If authorized and available locally, compile/run D0 on Demo only and preserve original CSV/log evidence.
- Verify live tick availability and closed-bar timestamps separately; do not relabel raw MT5 time as UTC.
- Do not run historical jobs that touch mixed-year data or OOS_2025.
- Gate D2: evidence is complete and internally consistent; otherwise mark INCONCLUSIVE and stop progression.

### Day 3 — Entry/setup contract freeze
- Choose one Forex symbol and one timeframe for the first Demo proof.
- Select one entry rule from already approved/source-backed project knowledge.
- Explicitly define trigger candle, entry timing, invalidation, SL, target, spread/slippage handling, expiry, and NO_TRADE cases.
- Reconcile the rule with the canonical minimum RR 3.0 and stop-distance 0.5–4 ATR constraints.
- Do not use the old V5.4 2R/0.75 ATR adapter as the canonical live risk policy.
- Gate D3: the user approves the exact source-backed entry/setup contract. If not approved, no autonomous orders.

### Day 4 — Isolated Demo adapter implementation (requires separate approval)
- Only after D3 and explicit implementation approval, build an independently versioned Demo-only adapter.
- Default state must be disabled; enforce Demo account identity at runtime.
- Implement broker-aware volume calculation using MT5 contract properties and profit/loss calculation, then normalize to broker volume step and limits.
- Add idempotent order intent IDs, duplicate prevention, request/response audit logs, and safe handling of requotes/rejections.
- No connection to a Live account and no secret values in source control.
- Gate D4: code review and deterministic tests pass before any order is sent.

### Day 5 — Order lifecycle proof on Demo
- Test one controlled Demo order with minimum valid volume and explicit user-supervised approval.
- Prove open, SL/TP placement, modify, partial/complete close, rejection handling, and reconciliation against terminal positions/deals.
- Confirm no duplicate order after retry/restart.
- Gate D5: every order intent reconciles to broker state and audit log.

### Day 6 — Fault and risk tests
- Test terminal restart, network interruption, stale quote, missing candle, invalid symbol, market closed, insufficient margin, invalid volume, broker stop-distance rejection, and price deviation.
- Verify kill switch, daily loss limit, max open positions, and fail-closed NO_TRADE behavior.
- Confirm the system never advances a capture cursor or executes on missing/unverified source data.
- Gate D6: no unresolved critical fault; otherwise disable execution.

### Day 7 — Demo soak and release decision
- Run in Demo with tightly bounded settings and full logging.
- Review every generated signal, order request, fill, modification, close, spread, slippage, and rejection.
- Produce a signed-off readiness report.
- Possible outcomes: DEMO_LIMITED_READY, SIGNAL_ONLY, or NOT_READY.
- No automatic transition to Live. Live trading requires a separate explicit authorization and independent release gates.

## 4. Required safety defaults

- Forex only; one symbol at first.
- Demo account only; refuse all non-Demo accounts.
- Orders disabled by default.
- No trading when data, clock, symbol mapping, MTF lineage, setup, risk, or broker state is uncertain.
- Canonical risk engine remains authoritative: minimum RR 3.0, stop distance 0.5–4 ATR, existing risk budget and drawdown breaker.
- No automatic risk escalation or self-modification of production rules.
- No 2025 OOS data read, tuning, training, calibration, or threshold selection.
- No merges to `main` as part of this sprint.

## 5. User-side prerequisites

The user needs:
1. A Windows PC that can remain on during the Demo run.
2. MT5 Desktop installed (mobile MT5 alone cannot run MQL5 scripts/MetaEditor).
3. A broker-issued Demo login and server.
4. Permission to install Python packages or run a reviewed local tool if the approved adapter uses the Python MT5 integration.
5. Availability for supervised Demo order tests; no credentials should be pasted into chat.

## 6. Schedule realism

Seven days is a **target for a constrained Demo proof, not a delivery guarantee**. It depends on immediate access to the PC and Demo terminal, broker API compatibility, and approval of a precise entry/setup contract. Given the unresolved MTF producer and setup-generation gaps, the complete existing AI Decision Brain is not expected to become fully autonomous within this week.

If any gate fails, the sprint stops safely at SIGNAL_ONLY / NO_TRADE. A longer schedule is required to close source lineage, setup generation, order lifecycle, recovery, and soak-test gaps.

## 7. Authorization boundary

This plan authorizes audit and planning only. It does not itself authorize:
- source/runtime code changes;
- changing the MT5 production capture EA;
- connecting to a Live account or sending Live orders;
- selecting an unapproved entry rule or changing risk parameters;
- reading or using 2025 OOS datasets;
- merging PRs or changing `main`.

A separate, explicit approval is required before implementation of the isolated Demo execution adapter.
