# Decision Brain V1 vs AI Decision Engine V1 — Version Reconciliation Audit

Date: 2026-08-21
Status: RECONCILIATION COMPLETE AT AVAILABLE-EVIDENCE BOUNDARY

## Question
Does the newer Decision Brain V1 formally replace, wrap, or coexist with the older AI Trading Decision Engine V1 candidate-selection layer?

## Evidence searched
Dropbox searches were performed for explicit integration/replacement/handoff evidence, including:
- Decision Brain Integration Handoff
- Decision Brain V1 Risk Engine Integration
- decision_brain.py risk_engine candidate
- Decision Brain V1.1
- 79_RULE / KNOWLEDGE_ALIGNMENT / RUN_074

No explicit replacement, wrapper, or end-to-end adapter artifact was located by those searches.

A project archive for Context-Aware Retrieval V2 was located at:
`/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_CONTEXT_AWARE_RETRIEVAL_V2.zip`
This confirms the project contains additional knowledge/retrieval architecture, but this discovery alone does not prove a Decision Brain-to-Candidate integration contract.

## Proven facts from already inspected artifacts

### AI Trading Decision Engine V1
- Research-only candidate-selection layer.
- Inputs: Murphy, Nison, TIZ-derived fields.
- Fixed experiment policy produces CANDIDATE / REVIEW / NO_TRADE.
- Runtime audit artifacts exist.
- Candidate-level architecture is strongly evidenced as upstream of Risk Engine, although exact adapter source remains unproven.

### Decision Brain V1
- Evidence aggregator / market-state assessment layer.
- Explicitly consumes six-timeframe context.
- Outputs market state, directional bias, confidence, evidence, contradictions and no-trade reasons.
- Does not automatically execute BUY/SELL.
- Risk is evaluated after market understanding.
- Similarity remains evidence only.
- 2025 remains OOS/no calibration.

## Reconciliation verdict

### NOT PROVEN
The available evidence does not prove that Decision Brain V1:
- replaces AI Decision Engine V1;
- wraps AI Decision Engine V1;
- directly emits the exact CANDIDATE contract consumed by Risk Engine V1;
- is already wired into the old Decision Engine -> Risk runtime chain.

### NOT A CONTRADICTION
The two components have different evidenced contracts and can coexist as distinct architectural layers/versions. However, coexistence alone must not be mistaken for an already-proven integrated runtime chain.

## Current safe architecture state

Proven historical research chain:
`AI Decision Engine V1 -> CANDIDATE -> Risk Engine V1`
(adapter source not yet proven, architecture strongly evidenced)

Proven newer market-understanding layer:
`Market Pipeline + 6 TF + evidence/knowledge -> Decision Brain V1 -> market assessment`

Unproven bridge:
`Decision Brain V1 -> candidate/decision gate -> Risk Engine V1`

## Governance decision
Do not merge or delete either component by assumption.

Treat the missing bridge as an explicit integration contract that must be defined and tested before end-to-end Decision Brain integration. This is an architecture/adapter gap, not a reason to rebuild completed modules.

Any future bridge must preserve:
- Murphy = technical context / market structure.
- Nison = confirmation/contradiction, not standalone direction.
- Trading in the Zone = psychology/process gate only; must not generate direction.
- Similarity = historical evidence only; never sole decision-maker.
- Volume unavailable != volume zero.
- 2025 = final OOS; never used for tuning/calibration.
- Risk gates remain downstream of market understanding and before any live execution.

## Next safe action
Before building the bridge, inspect the existing Context-Aware Retrieval / knowledge runtime artifacts and current project contracts to determine whether an existing integration boundary already defines:
`market assessment -> candidate/review/no-trade -> risk`

If no existing contract is found, define the smallest compatible adapter contract only after that audit. Do not rebuild Decision Brain V1, AI Decision Engine V1, Risk Engine V1, or the completed 79-rule Knowledge Alignment.
