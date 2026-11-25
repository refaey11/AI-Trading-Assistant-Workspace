# Product Completion Audit — Decision Brain V1
Date: 2026-11-25
Branch: `audit/product-completion-v1-2026-11-25`
Base: `766e60a3b43abfea0c16ace7112468a5b4007cac`
Scope: GitHub-only, read-only product/architecture audit recorded as a report. No runtime, rule, test, data, workflow, or `main` changes. No 2025/2026 market-data payloads were accessed.

## Executive conclusion

The workspace is not starting from zero. It contains a recovered Decision Brain, book/rule knowledge, a Three-Book evaluator, a Risk Engine, a live-event runtime, historical replay components, and MT5 capture/bridge work.

However, **there is not yet one end-to-end, trusted, multi-pair V1 product**. The current live runtime can return `SIGNAL_READY` or `NO_TRADE` from a caller-supplied event, but this is a contract-level composition, not proof that the upstream market-data, Murphy, MTF, Nison, and account/risk producers are connected, authenticated, and operating in MT5.

The immediate delivery target should remain a **decision-support V1**: analyze supported FX pairs and produce BUY / SELL / NO_TRADE with evidence, entry, SL, TP, risk explanation, and audit trail. User approval remains required; no automatic orders in V1.

## What already exists

| Component | Evidence-backed state | Product interpretation |
|---|---|---|
| Knowledge / books | Murphy and Nison frozen records exist; Nison checkpoint records 44/44 frozen. Murphy master freeze manifest records 33/51 closed. | Reuse existing knowledge; do not rebuild. |
| Decision Brain | Recovered `decision_brain.py` exists and produces market-state/context assessment from MTF and Volume. | Existing brain is an assessment component, not a standalone signal generator. |
| Three-Book evaluator | WP2 implementation makes Murphy the sole BUY/SELL direction authority; Nison contradiction blocks; confidence is NOT_EVALUABLE. | Direction policy is implemented at this evaluator boundary, not yet source-authenticated end-to-end. |
| Risk Engine | Existing integration validates supplied entry/SL/TP, stop distance 0.5–4 ATR, 3R minimum, risk budget and drawdown breaker. | Risk validation exists; it does not itself derive the trade setup or broker-specific lot size. |
| Live Decision Runtime | Accepts one event and can return SIGNAL_READY/NO_TRADE; output is SIGNAL_ONLY and orders are disabled. | Runtime skeleton exists; its evidence envelope is caller-asserted and not authenticated. |
| Historical runner / Gate3C | Existing 2016–2024 replay and one-event composition artifacts exist. | Historical proof is not complete/official; the current live runtime is not a substitute for full replay. |
| Similarity | Existing historical-memory components and policy exist. | Evidence/audit only; not directional authority. |
| MT5 | Multiple raw-capture, display-bridge, clock-gate, and integration proposals exist. | No verified MT5 Demo end-to-end order lifecycle has been demonstrated. |

## Critical gaps preventing a usable V1

### P0 — Must close before claiming a trustworthy signal

1. **Real source-to-decision wiring is absent.** The live runtime accepts a supplied event envelope. Its `authoritative=true`, `source`, and `producer` fields are self-asserted; they are not checked against a trusted producer registry, signed attestation, immutable code/config digest, or authenticated clock.
2. **Murphy provider/eligibility contract is not closed.** WP3 found no verified active producer/adapter that simultaneously satisfies the approved source contract and the live runtime contract. Row-level PASS/direction, eligible rule IDs, exact event identity, and source timestamps are not fully bound to the top-level direction.
3. **MTF/Volume production source is not ready.** The historical MTF source has unresolved timestamp, missing-value, formula/feature semantics, and producer provenance. The MTF V2 work is still a design/prototype track: the pivot detector is not implemented; L/R values, trusted source-bar identity, clock provenance, and lifecycle rules remain open. Synthetic fixture CI is not production data validation.
4. **Risk receives a proposed bracket; it does not create one.** The live runtime requires `entry_price`, `stop_loss`, `take_profit`, and ATR as inputs. A governed setup/entry/SL/TP generation policy must be connected and validated without inventing thresholds. Generic Risk `position_size` is not broker lot sizing.
5. **No real MT5 Demo cycle has been proven.** The repo records that MQL5 compilation/terminal validation is separate from GitHub CI. A Demo adapter and safe order lifecycle (open/modify/close, reconnect/restart, duplicate prevention, broker constraints) are not proven. This is later than signal-only V1, but required before any execution-capable release.

### P1 — Must close for a complete decision-support product

6. **No end-to-end multi-pair coverage proof.** A source inspector supports a small named symbol set, but prior PR #102 explicitly says this does not make the full Brain/backtest runner multi-pair end-to-end. Need a governed symbol/instrument contract and pair-by-pair coverage tests.
7. **Confidence is intentionally unavailable.** Do not show a numeric confidence until a canonical Murphy-only confidence contract is approved and validated.
8. **Brain no-trade reasons are metadata in the WP2 live runtime.** Decide governance treatment explicitly; do not silently treat these as hard gates or discard them.
9. **Freshness/clock contract is incomplete.** Live runtime checks ordering and rejects a future timestamp, but has no approved maximum event age and no authenticated clock. Do not invent a freshness threshold.
10. **Historical performance proof is incomplete.** Existing PR #97 describes a runner that fails its official gate because available Murphy evidence was only 7/34 decision-eligible rules and its Dropbox-backed source action returned HTTP 401. No official profitability claim is supported. Given the GitHub-only operating constraint, any replay inputs must be made available through an approved GitHub-only artifact/source path; do not revive Dropbox/CircleCI.
11. **MT5 integration / broker sizing remains separate.** No broker-specific calculation using MT5 symbol contract properties / OrderCalcProfit has been demonstrated.

## Confirmed workflow / branch topology risks

- PR #144 is validation-only and based on PR #120's feature branch, not a reconciled integration base; its own description says do not merge as-is.
- PR #119/#120 remain separate draft tracks with unresolved source-lineage/integration blockers.
- PR #141 is a specification + synthetic fixture + isolated identity encoder proposal; it explicitly says no production pivot detector exists and no Brain integration is done.
- PR #139 is a prototype structure consumer of confirmed pivots, not a pivot detector or production MTF source.
- PR #140 validates envelope structure/causality only and explicitly keeps `production_eligible=false`.
- PR #130/#131 and related MT5 clock work do not authenticate broker clock or native per-bar identity.
- PR #97 is not an official historical result and its source path is incompatible with the current GitHub-only constraint until replaced by an approved GitHub-only artifact flow.

No PR is approved for merge by this report.

## Recommended delivery plan — shortest safe path

### Track A: deliver signal-only V1 first

1. **Freeze the V1 acceptance contract.** Input: one completed market event for a supported FX pair. Output: BUY / SELL / NO_TRADE; direction source; evidence and contradictions; entry; SL; TP; RR; risk budget/result; reasons; timestamp/source provenance; audit record. No numeric confidence until approved.
2. **Choose and close one real data path.** Identify one authoritative MT5 market-data source, symbol mapping, native timeframe, bar-close semantics, verified clock, and source-bar identity. Keep the existing MTF/legacy paths untouched until compatibility is demonstrated.
3. **Close one approved Murphy provider path.** Reuse frozen evaluators/adapters; do not modify protected 0006/0007 semantics in this workstream. Bind producer identity, rule eligibility, row PASS/direction, event identity, and freshness to the same event.
4. **Connect Nison and existing Brain context.** Nison remains confirmation/contradiction only. MTF/Volume remain context only. Similarity remains evidence only. TIZ remains metadata-only under the current dated project decision.
5. **Close setup and Risk handoff.** Define where entry/SL/TP come from, prove no-lookahead and price geometry, then run the existing canonical Risk hard gate (3R minimum). No invented ATR/pip/percentage thresholds.
6. **Run one-symbol end-to-end replay on 2016–2024** using approved source evidence and a GitHub-only artifact path. Then expand to the agreed FX symbol universe. Do not inspect or tune on 2025/2026 market-data payloads.
7. **Run a controlled live-feed, signal-only shadow test** with recorded source events and no orders. Validate event freshness, duplicates, outages, restart behavior, and auditability.
8. **Release V1 only after the above gates pass.** The user reviews and approves each recommendation; no automatic execution.

### Track B: execution-capable Demo — after Track A

Implement broker-aware volume/lot sizing, a separate MT5 Demo EA/adapter, and order lifecycle/recovery tests. Compile in MetaEditor and prove Demo-only open/modify/close/restart behavior. Live execution remains out of scope.

## Scope control / explicit non-goals

- No rebuild of existing books, Brain, Similarity, or historical aggregation.
- No change to frozen Murphy/Nison rules or protected 0006/0007 semantics.
- No main changes, no merges, no live orders.
- No Dropbox or CircleCI.
- No 2025/2026 market-data payload access, tuning, calibration, threshold selection, or optimization.
- Do not claim an Actions pass proves data provenance, full replay, profitability, or MT5 terminal behavior.

## Final product verdict

**Current state: substantial components and a signal-only runtime prototype exist; end-to-end production-grade Decision Brain V1 is not complete.**

The most effective next task is not another broad audit. It is to close one vertical slice in order: **trusted source event → approved Murphy direction → existing Brain context/Nison checks → generated and validated bracket → Risk hard gate → explainable signal output**, first for one supported FX pair, then scale to all agreed pairs. Every stage must have real-source evidence and targeted tests before expanding scope.
