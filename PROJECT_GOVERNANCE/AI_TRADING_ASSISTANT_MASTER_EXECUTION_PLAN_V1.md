# AI Trading Assistant / Decision Brain — Master Execution Plan V1

**Status:** Active project reference  
**Created:** 2026-11-18  
**Repository:** `refaey11/AI-Trading-Assistant-Workspace`  
**Reference branch:** `feature/mtf-producer-v1-design` (PR #122; draft, open, not merged)  
**Purpose:** Keep one agreed engineering direction, governance boundary, implementation sequence, and acceptance standard for the project.

---

## 1. Product identity and objective

This project is an **AI Trading Assistant / Decision Brain**, not a trading indicator and not an unrestricted auto-trading bot.

The system must combine:
1. Current market evidence and market structure.
2. The already collected and integrated book knowledge.
3. Historical similarity/memory as supporting evidence.
4. A strict risk and process gate.

The system must explain its conclusion, show supporting and conflicting evidence, and return `NO_TRADE` whenever evidence is missing, stale, invalid, contradictory, or fails a required gate.

The target coverage is **all supported Forex pairs**, not Gold only.

## 2. Non-negotiable authority boundaries

| Component | Permitted responsibility | Must not do |
|---|---|---|
| John Murphy | Technical context, trend, market structure, support/resistance and broader market interpretation | Be silently replaced by an unapproved indicator formula |
| Steve Nison | Candlestick confirmation, contradiction, and evidence quality | Independently create the market direction |
| Trading in the Zone (TIZ) | Psychology, discipline, readiness and process gate | Generate BUY/SELL direction or override market evidence |
| Similarity Engine | Historical memory and comparable-case evidence | Become the sole decision maker or independently issue direction |
| Decision Brain | Combine current evidence, book rules, memory context and risk; explain the result | Ignore missing evidence, hard gates, or component authority boundaries |
| Risk Engine | Enforce risk constraints and produce a valid risk plan | Guess broker lot sizes or bypass broker/account constraints |

Existing book knowledge and project artifacts are the source of truth. Do not rebuild them from scratch. Before any new integration or replacement, perform a compatibility review against the existing implementation and source material.

## 3. Hard governance and safety rules

- **2025 is locked out-of-sample (OOS).** Never use it for training, tuning, calibration, feature selection, threshold selection, or optimization.
- Do not change `main` as part of this work. Work on feature branches and reviewable pull requests.
- Do not merge any PR without the project owner's explicit approval.
- Do not enable live trading or place live orders.
- No profitability, readiness, or completion claim without reproducible evidence.
- A passing unit test is evidence only for the behavior it covers; it is not proof of full MT5 or broker correctness.
- Do not invent feature formulas, timeframe weights, timestamp conversions, missing-value imputations, session boundaries, or broker properties.
- Do not use CircleCI. Project workflow verification is GitHub Actions only.
- Do not replace the existing architecture with a quick EMA/indicator shortcut.
- V1 must not autonomously issue or execute BUY/SELL orders. The intended early output is an explainable decision/trade plan with `NO_TRADE` when gates fail. Any later Demo execution must be isolated, controlled, and explicitly approved.

## 4. Target system flow

```text
MT5 Native Market Data + Account/Broker Snapshot
                    |
                    v
        Data Contracts / Provenance Gates
                    |
                    v
        Six-Timeframe MTF Producer
          M5 / M15 / M30 / H1 / H4 / D1
                    |
                    v
     Existing Book Evidence Evaluators
       Murphy / Nison / TIZ process gate
                    |
                    +------ Similarity / historical memory
                    |       (evidence only)
                    v
              Decision Brain
       Explainable decision or NO_TRADE
                    |
                    v
              Canonical Risk
                    |
                    v
          Trade Plan / Human Review
                    |
                    v
     Later: isolated MT5 Demo E2E adapter
                    |
                    v
        Monitoring, audit trail, release gate
```

## 5. Canonical risk and decision gates

The project-level risk constraints currently recorded are:
- Minimum reward-to-risk: **3R**.
- Stop distance: **0.5–4 ATR**.
- Drawdown breaker: mandatory.
- Position sizing must respect actual broker symbol/account properties. A generic risk-engine quantity must not be assumed to equal valid MT5 lots.
- Use MT5 broker calculation/specification facilities (including OrderCalcProfit and symbol contract properties where applicable) before claiming broker-valid sizing.
- Missing or invalid inputs must fail closed to `NO_TRADE`.

Decision output must include, at minimum:
- Decision state and reason.
- Evidence sources and timestamps.
- Murphy context and result.
- Nison confirmation/contradiction state.
- TIZ process-gate state.
- Similarity evidence as non-authoritative context.
- Risk-gate result and any rejection reason.
- Explicit missing/stale/conflicting evidence.

## 6. Engineering roadmap and acceptance gates

### Stage 0 — Baseline and source-of-truth inventory
- Record current branches, PRs, code paths, contracts, tests and GitHub Actions evidence.
- Separate implemented behavior from design documents and historical audit claims.
- Preserve existing frozen components and their ownership boundaries.

**Acceptance:** Every claimed capability points to a concrete file, test, workflow run, or reproducible artifact.

### Stage 1 — MTF source contract recovery and integration (current priority)
- Recover the authoritative six-timeframe source contract and its examples from existing GitHub history/artifacts.
- Reconcile field definitions, roles, timeframe assignment, alignment semantics, timestamp provenance, candle-close rules, missing-value behavior and source identity.
- Inspect the existing MTF adapter/resolver/ranker and strict join; do not add a competing scoring or join layer.
- Map MT5 raw capture fields to the required source contract. Do not synthesize absent server/UTC/close/retrieval timestamps.
- Build source-to-runtime tests using authoritative contracts and real aligned rows where available.
- Preserve fail-closed behavior until unresolved semantics and provenance are closed.

**Acceptance:** Each required field has an authoritative definition and lineage; timestamps are demonstrably valid and no-lookahead; missing data is handled by contract; real source rows pass the same integration path consumed by the Decision Runtime; GitHub Actions proves the relevant tests.

### Stage 2 — Book evaluator closure
- Audit the existing Murphy, Nison and TIZ implementations against the collected source knowledge.
- Preserve Murphy as technical context, Nison as confirmation only, and TIZ as process gate only.
- Verify rule IDs, source references, input requirements, conditions, output semantics and test coverage.
- Complete TIZ only from the already collected source material; do not invent missing book rules.

**Acceptance:** Every active rule is traceable to the source material, has explicit input/condition/output semantics, and has positive, negative, boundary and missing-data tests.

### Stage 3 — Decision Brain integration
- Connect the real MTF output and verified book evidence to the existing Decision Brain.
- Make evidence aggregation, precedence, contradiction handling and rejection reasons explicit.
- Keep Similarity as memory/evidence only.
- Return `NO_TRADE` on any mandatory missing or failed gate.

**Acceptance:** End-to-end decision fixtures demonstrate valid decisions and fail-closed behavior for missing, stale, contradictory, malformed and future-dated evidence.

### Stage 4 — Risk Engine and trade-plan validity
- Verify the canonical risk contract and drawdown breaker.
- Integrate broker-specific symbol, tick, contract, volume-step, minimum/maximum volume, margin and account constraints.
- Calculate risk in account currency; do not treat generic units as MT5 lots.
- Produce explainable SL/TP and sizing only when all required broker inputs are available.

**Acceptance:** Deterministic tests cover broker specifications, currency conversion, rounding, min/max volume, invalid stops, spread/cost assumptions, drawdown lockout and 3R/ATR constraints.

### Stage 5 — Historical validation
- Use only approved development data (not 2025 OOS) for development checks and controlled backtesting.
- Check data quality, lookahead, survivorship/selection effects, costs, spread, commission and slippage assumptions.
- Keep research metrics separate from deployment readiness.

**Acceptance:** Reproducible reports identify exact data ranges, assumptions, exclusions, code version and limitations. The 2025 OOS lock remains intact.

### Stage 6 — MT5 Demo end-to-end
- Connect native MT5 market and account snapshots.
- Implement an isolated Demo-only execution adapter after the decision and risk layers are stable.
- Test order submission, rejection, fill, modify, close, partial fill where relevant, disconnect, reconnect, duplicate events, restart and idempotency.
- Verify compile/runtime behavior in MetaEditor/MT5 Demo; Python unit tests alone are insufficient.

**Acceptance:** A complete audited Demo lifecycle succeeds across normal and failure/recovery cases, with no route to a live account.

### Stage 7 — Monitoring and release governance
- Add structured logs, decision/evidence snapshots, risk events, health checks and incident handling.
- Define versioning, rollback and release criteria.
- Keep human approval and live-trading authorization separate from technical test success.

**Acceptance:** Reproducible monitoring and rollback evidence exists; no live release occurs without a separate explicit approval.

## 7. Current known project state (snapshot: 2026-11-18)

### Decision Runtime — PR #120
- Draft, open, not merged.
- Branch: `feature/live-decision-runtime-v1`.
- Adds a live-event adapter around the existing Decision Brain and Three-Book evaluator.
- Requires source-backed evidence, timezone-aware timestamps and rejects evidence later than decision time.
- Keeps 2025 excluded; requires Nison rule IDs and TIZ process readiness.
- Runs canonical risk checks but does not invent broker lots or SL/TP.
- Output remains signal-only; it does not place orders.
- Dedicated GitHub Actions evidence is recorded in the PR description. This is not MT5 Demo E2E proof.

### MTF Producer design — PR #122
- Draft, open, not merged.
- Branch: `feature/mtf-producer-v1-design`.
- Design/documentation scope; does not implement feature formulas or emit MTF values.
- Uses the six-timeframe family M5/M15/M30/H1/H4/D1.
- Historical MTF evidence and source-family identity have been recovered, but semantic mapping, timestamp provenance and live runtime compatibility remain partially unresolved.
- The strict join and timestamp/finite-value gates are useful foundations, not proof of a complete producer.
- The Dynamic MTF adapter/resolver/ranker review identified unresolved alignment semantics, role-selection behavior, upstream trust assumptions and unconfirmed wiring into the live runtime.
- Do not treat design documentation or synthetic unit tests as proof of real aligned-row runtime behavior.

### MT5 Raw Capture
- Existing capture supports native M5/M15/M30/H1/H4/D1 and reads the latest closed candle.
- Existing contract/ingest tests cover core validation, OHLC, finite values, volume, duplicates and hashing.
- Important provenance gaps remain: distinct historical broker-server bar time, independently trusted UTC lineage, bar close time, retrieval time and timezone policy are not all emitted as separate validated fields.
- Do not derive missing timestamps by adding timeframe duration or by guessing broker timezone/DST.
- Existing V1 GitHub Actions success validates the current Python fixture suite only; it does not establish MQL5 compile/runtime or broker clock correctness.

### Existing knowledge and architecture
- Murphy, Nison and TIZ source material and prior integration work must be reused and audited, not recreated.
- The official six-timeframe architecture is distinct from the older H1/H4-only research reader.
- The W1 macro role described in one architecture document is not part of the six-field runtime input contract unless formally reconciled and approved.
- The canonical standalone Dynamic MTF contract still needs to be recovered/verified from GitHub evidence before implementation decisions depend on it.

## 8. Immediate execution plan — Sprint 1

1. Refresh PR #122 and its current head before editing.
2. Search GitHub branches, commits, PRs and repository files for the exact original Dynamic MTF contract JSON, examples and references.
3. Read the complete six-timeframe as-of alignment audit and the underlying source/feature contracts.
4. Inspect the actual producer/adapter/resolver/ranker implementation and tests on the relevant branches.
5. Trace the exact integration boundary from MTF source/join to the Live Decision Runtime in PR #120.
6. Decide based on evidence:
   - If the original contract fully defines the fields and semantics, implement a narrow, tested adapter/integration using that contract.
   - If required semantics remain missing, stop at the missing contract and recover/approve the contract before writing feature logic.
7. Add real integration tests and run the relevant GitHub Actions workflows.
8. Update this reference with exact changed files, commit/PR, workflow run IDs, test counts, results and remaining blockers.

**Do not create another audit-only document instead of closing a verified implementation gap.** Documentation updates are appropriate only when they record a decision, contract, acceptance result or unresolved blocker needed to govern the next code change.

## 9. Evidence and progress reporting standard

Every progress report must distinguish:
- **Implemented:** code exists on a named branch/commit.
- **Tested:** exact test command/workflow and result are known.
- **Integrated:** actual data passes through the intended runtime path.
- **Demo-verified:** MT5 Demo lifecycle has been observed and audited.
- **Released:** separate release approval exists.

Never collapse these states into one percentage. If a percentage is requested, report separate measured completion by stage and state the evidence/denominator used. If evidence is unavailable, say so.

## 10. Change control

This document is the agreed execution reference, not permission to bypass review. Update it when:
- a stage acceptance gate is met or fails;
- an authoritative contract is recovered or formally superseded;
- a project-level architecture/risk decision is explicitly approved;
- a material blocker or scope change is established.

Any change to the component authority boundaries, risk constraints, 2025 OOS protection, or live-trading prohibition requires explicit project-owner approval.
