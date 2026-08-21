# Dropbox Source Discovery — Risk Engine + Decision Brain

Date: 2026-08-21
Status: SOURCE ARTIFACTS LOCATED / READY FOR COMPATIBILITY AUDIT

## Why this record exists
A prior GitHub-only search did not locate the executable/source artifacts needed for a real Risk Engine and Decision Brain audit. The project Dropbox was then searched. The required artifacts were located there. This record corrects the earlier retrieval conclusion: absence from the searched GitHub paths did not mean the modules were absent from the project.

## Decision Brain V1 — located artifacts

### 1. `/decision_brain.py`
Dropbox server-modified: 2026-08-19T04:47:54Z.

Direct source findings:
- V1 explicitly states it is an evidence aggregator, not a trading signal generator.
- Produces a market-state assessment.
- Consumes multi-timeframe evidence and explicitly reads six trend-regime inputs: M5, M15, M30, H1, H4, D1.
- Uses `volume_available` as an availability gate; unavailable volume is represented as unavailable rather than treated as zero evidence.
- Similarity is used as HistoricalMemory evidence only.
- Produces market state, directional bias, confidence, evidence, contradictions, and explicit no-trade reasons.

### 2. `/DECISION_BRAIN_V1_SPEC.json`
Dropbox server-modified: 2026-08-19T04:41:28Z.

Spec findings:
- Purpose: combine independent market evidence into a structured market-state assessment.
- Similarity is historical memory, not the decision maker.
- Six-timeframe inputs are specified for market structure and volatility.
- Volume is active only when `volume_available=true`.
- Knowledge explains patterns/conditions and must not invent market data.
- Risk is evaluated after market understanding.
- Hard rules include: no future data; 2025 remains OOS and is not used for calibration; volume unavailable is not zero; similarity is not standalone; no automatic BUY/SELL execution in V1; conclusions must cite evidence modules.

## Risk Engine V1 — located artifacts

### 1. Active project spec
`/ai_trading_assistant_full_project_v1/ai_trading_assistant_core_v1/risk_engine/RISK_ENGINE_SPEC_V1.json`

### 2. Archived spec
`/ai_trading_assistant_full_project_v1/ai_trading_assistant_core_v1/archive/ai_trading_assistant_risk_engine_v1/risk_engine/RISK_ENGINE_SPEC_V1.json`

### 3. Runtime/audit artifacts
- `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1/RISK_ENGINE_EVENTS.csv`
- `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1/RISK_ENGINE_RESULTS.csv`
- `/ai_trading_assistant_full_project_v1/ai_trading_assistant_core_v1/archive/ai_trading_assistant_risk_engine_v1/risk_engine/RISK_ENGINE_TRADES_2017.csv`
- `/ENGINE_AUDIT/AI_Trading_Assistant_RISK_ENGINE_V1.zip`

### Risk spec findings
Hard gates:
- positive stop distance
- stop distance between 0.5 ATR and 4 ATR
- defined take profit
- risk budget fixed before entry

Other declared behavior:
- risk profiles: 0.25%, 0.5%, 1%, 1.5%
- position size formula: risk_money / stop_distance
- stop modes: structure, 2x ATR, hybrid
- research target: 1.5R
- drawdown tracked, not yet used as a trading halt
- research-only warning: costs, spread, slippage, leverage, contract size, and broker-specific pip value must be added before live execution

## Correction to project status
Previous status:
`Risk + Decision Brain = source artifacts not found in GitHub search`

Corrected status:
`Risk + Decision Brain = source/spec/runtime artifacts located in Dropbox`

This is a retrieval-location correction, not a rebuild or architecture change.

## Compatibility implications already evidenced
1. Decision Brain V1 recognizes the six-timeframe architecture.
2. Decision Brain V1 preserves `volume unavailable != volume zero`.
3. Decision Brain V1 preserves Similarity as evidence, not sole decision-maker.
4. Decision Brain V1 preserves 2025 as OOS/no-calibration.
5. Decision Brain V1 does not automatically execute BUY/SELL.
6. Risk Engine is defined as a hard-gated research component and explicitly warns that live-execution costs/market mechanics remain incomplete.

## Next safe action
Perform the actual compatibility audit using the located source/spec artifacts:

`Market Pipeline + 6-Timeframe Evidence + Knowledge Alignment (79 authoritative rules) -> Decision Brain V1 -> Risk Engine V1`

Audit the contracts, ordering, boundaries, hard gates, missing inputs, and runtime evidence. Do not rebuild any module unless a demonstrated compatibility failure requires a minimal fix.

## Governance
- Do not reopen completed Market Pipeline or Knowledge Alignment stages without new contradictory evidence.
- Preserve the separately proven six-timeframe architecture.
- Preserve 2025 as final OOS; never use it for tuning/calibration.
- Murphy = technical context/market structure; Nison = confirmation; Trading in the Zone = psychology/process gate only; Similarity = historical evidence only.
