# AI Decision Engine V1 — Candidate Chain Audit

Date: 2026-08-21
Status: RUNTIME LAYER LOCATED / COMPATIBILITY PARTIAL

## Why this audit was required
Risk Engine runtime events showed `decision=CANDIDATE`, but the producer of that candidate decision was previously unproven. Dropbox evidence located a separate `AI Trading Decision Engine V1` audit layer.

## Evidence located
Folder:
`/ENGINE_AUDIT/AI_Trading_Assistant_AI_DECISION_ENGINE_V1/`

Artifacts:
- `SPEC.json`
- `README.md`
- `DECISION_EVENTS.csv`
- `DECISION_ENGINE_RESULTS.csv`
- `CANDIDATE_PERFORMANCE.csv`
- `CANDIDATE_CONCENTRATION.csv`

Server modification timestamps: 2026-08-20.

## Decision Engine V1 contract
Inputs:
- Murphy technical context
- Nison candlestick confirmation
- TIZ process score

Fixed knowledge weights in this audited experiment:
- Murphy: 0.35
- Nison: 0.30
- TIZ: 0.35

Decision policy:
- score >= 75 -> `CANDIDATE`
- score 50–74.99 -> `REVIEW`
- score < 50 -> `NO_TRADE`

Status declared by spec: `RESEARCH_ONLY`.

README explicitly states that book-derived features do not independently create market direction.

## Runtime evidence
`DECISION_EVENTS.csv` contains timestamp, side, Murphy, Nison, TIZ, knowledge score/band, and final decision. The observed decisions include `NO_TRADE`, `REVIEW`, and candidate-level outcomes under the fixed policy.

Candidate concentration:
- 2016: 6 candidates out of 543 baseline events (1.10%)
- 2017: 13 / 627 (2.07%)
- 2018: 15 / 673 (2.23%)

Candidate performance artifact:
- 2016: 6 trades, net R -0.3508
- 2017: 13 trades, net R 6.0353
- 2018: 15 trades, net R 8.8461

The spec explicitly warns that PF is not a probability of future profit.

## Candidate -> Risk Engine linkage
Risk Engine runtime evidence contains the same architectural field family:
- Murphy context/technical
- Nison confirmation/candle
- TIZ process fields
- knowledge score/band
- decision=CANDIDATE
- risk and action fields

The counts also align at the audit-layer level:
Decision Engine candidate totals for 2016–2018 = 34; Risk Engine executed total for 2016–2018 = 33, with at least one explicit `SKIP_LOSS_STREAK` event in Risk artifacts. This is consistent with the Risk Engine acting after candidate selection and applying an additional execution gate.

Verdict: **ARCHITECTURE-LEVEL LINK STRONGLY EVIDENCED**.

However, an exact row-for-row adapter/source implementation was not located in the inspected artifacts, so strict runtime adapter provenance remains `UNPROVEN`.

## Critical version distinction
This `AI Trading Decision Engine V1` is a separate research candidate-selection layer from the newer `Decision Brain V1` evidence-aggregator contract.

Therefore the project contains at least these distinct layers/versions:
1. AI Decision Engine V1 — fixed book-feature scoring -> CANDIDATE/REVIEW/NO_TRADE.
2. Risk Engine V1 — applies risk/execution controls to candidate events.
3. Decision Brain V1 — newer evidence aggregator / market-state assessment with six-timeframe context and no automatic execution.

Do not merge these into one component by assumption.

## Compatibility verdict
- Decision Engine -> Candidate generation: PASS (runtime evidence)
- Candidate -> Risk architecture: STRONGLY EVIDENCED / adapter source UNPROVEN
- Murphy/Nison/TIZ role separation in candidate layer: PARTIAL / experiment-specific weights require compatibility check against current 79-rule authority
- Direct equivalence between AI Decision Engine V1 and newer Decision Brain V1: NOT PROVEN

## Next safe action
Perform version/contract reconciliation before end-to-end integration:
- identify whether Decision Brain V1 replaces, wraps, or coexists with AI Decision Engine V1;
- verify how the authoritative 79-rule Knowledge Alignment boundary maps into the newer Brain without importing obsolete fixed weights by assumption;
- locate exact candidate-to-risk adapter if available.

Do not rebuild any module before this reconciliation.
