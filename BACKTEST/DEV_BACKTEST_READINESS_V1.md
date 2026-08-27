# Development Backtest Readiness V1

Purpose: execute the current Decision Brain on development data only, without rebuilding existing subsystems.

Development window: 2016-2024.
Evaluation-only/OOS: 2025.

Required runtime composition:
- 34 Murphy rules
- 44 Nison rules
- governed 78-rule adapter
- MTF evidence
- Historical Context Memory
- Historical Outcome Memory
- Similarity Memory as evidence-only
- Context-Aware Retrieval as interpretation/knowledge evidence only
- TIZ process gate only
- Risk as hard execution gate

Prohibited:
- 2025 tuning/calibration
- changing rule semantics to increase trade count
- allowing historical memory/similarity to generate direction
- substituting legacy 2016-2018 artifacts for current 78-rule evaluation

Validation requirement before profitability claims:
- unified event stream on 2016-2024
- explicit timestamp/as-of checks
- memory candidate availability and lookahead audit
- explicit MTF consumption audit
- execution funnel measured from event eligibility through executed trades
- costs/slippage applied according to frozen backtest contract

Status: READINESS SPEC ONLY. No profitability result is claimed by this file.
