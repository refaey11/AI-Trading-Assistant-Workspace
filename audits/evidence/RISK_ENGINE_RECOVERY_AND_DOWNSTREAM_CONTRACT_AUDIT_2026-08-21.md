# Risk Engine Recovery and Downstream Contract Audit — 2026-08-21

## Correction to prior position
The active GitHub tree did not expose a Risk Engine runtime during the initial downstream search. That does NOT mean the project lacks a Risk Engine. A wider recovery search in Dropbox found the original V1 risk-engine artifacts and specification.

## Recovered evidence
Dropbox contains both active-project and archived V1 artifacts, including:

- `RISK_ENGINE_SPEC_V1.json`
- `RISK_ENGINE_EVENTS.csv`
- `RISK_ENGINE_RESULTS.csv`
- yearly `RISK_ENGINE_TRADES_*.csv`
- `POSITION_SIZING_EXAMPLES.csv`
- `AI_Trading_Assistant_RISK_ENGINE_V1.zip`

The preferred provenance source is the non-archive project path when content is equivalent; archived copies are evidence/backup, not a reason to rebuild the engine.

## Recovered Risk Engine V1 contract
Hard gates:
1. positive stop distance
2. stop distance between 0.5 ATR and 4 ATR
3. defined take profit
4. risk budget fixed before entry

Risk profiles:
- 0.25%
- 0.50%
- 1.00%
- 1.50%

Position sizing formula:
`risk_money / stop_distance`

Stop modes:
- structure
- 2x ATR
- hybrid

Research target:
- 1.5R in the prototype

Drawdown rule:
- tracked, not yet used as a trading halt

Live-execution warning from the source contract:
The comparison is research only; costs, spread, slippage, leverage, contract size, and broker-specific pip value must be added before live execution.

## Downstream architecture implication
The Risk Engine is an existing downstream module. It must be recovered/audited and connected rather than rebuilt from scratch.

The governed chain remains conceptually:

Knowledge / Process Gates
→ Decision Brain Assessment
→ Risk Engine Hard Gates + Position Sizing
→ Eligibility / execution boundary

This audit does NOT authorize the Risk Engine to generate market direction. Market direction/context remains upstream evidence. Risk only determines whether a candidate can satisfy risk constraints and how size is calculated under the existing contract.

## Compatibility status
- Risk Engine existence: CLOSED / recovered
- Position sizing existence: CLOSED / recovered
- Risk Engine specification: CONFIRMED
- Active GitHub runtime copy: NOT YET RECOVERED
- Exact input/output adapter to current Decision Brain: PENDING
- Full end-to-end runtime PASS: NOT YET CLAIMED
- 2025 OOS: remains locked; no tuning authorized

## Next controlled action
Recover the executable Risk Engine V1 runtime or canonical implementation artifact, inspect its exact input/output fields, then perform a compatibility audit against the current governed Decision Brain runner before any code integration.
