# AI Trading Assistant — Decision Brain
## Chat Handoff / Continuation State
Date: 2026-08-27

## Project mission
Build the governed AI Trading Assistant / Decision Brain, not a simple indicator.

## Non-negotiable architecture
- Murphy = technical context / market structure / directional context.
- Nison = candlestick confirmation / contradiction only; not independent direction.
- Trading in the Zone (TIZ) = process/psychology context; never a directional generator.
- Similarity Engine / Historical Memory = historical evidence only; never sole decision maker or direction generator.
- Risk = hard execution gate.
- 2025 = OOS; never use for tuning/calibration.
- Do not rebuild existing project knowledge from scratch.
- Before new integration, perform compatibility audit.
- Never invent rule IDs, evidence, thresholds, or missing historical data.

## Current verified state
### GitHub
Repository: refaey11/AI-Trading-Assistant-Workspace
Important paths already present:
- BACKTEST/DEV_BACKTEST_RUNNER_V1.py
- BACKTEST/DEV_BACKTEST_RUNNER_PLAN_V1.md
- BACKTEST/DEV_BACKTEST_EXECUTION_CHECKPOINT_2026-08-27.md
- DEVELOPMENT_2016_2024/run_nison_development_2016_2024_v1.py
- OOS_2025/run_nison_historical_production_v1.py
- OOS_2025/build_historical_context_execution_inputs_v1.py
- evaluation/three_book_decision_evaluator_v1.py
- RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py
- governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json
- PROJECT_STATE/MURPHY_RUNTIME_ROUTING_REGISTRY_V1.json

### Decision Brain
Recovered Decision Brain exists at RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py.
The Three-Book evaluator exists and maps existing Brain assessment + Murphy/Nison/Risk evidence to BUY/SELL/NO_TRADE without creating new direction.

### Murphy runtime
Current runtime registry reports 34 Murphy evaluators as ACTIVE_DISPATCHED. Do not use older snapshots to downgrade this.

### Nison runtime
Nison 44 runtime is operational. The earlier Dropbox token/import/Candle timestamp issues were fixed; Nison runtime jobs 0001–0044 passed in CI.

## Historical evidence discovery
A single file named MURPHY_2016_2024_FULL_EVIDENCE.csv was not found in GitHub/Dropbox.
However, historical Murphy evidence was recovered from the uploaded workspace archive.
Recovered source files include:
- MURPHY_0003_0004_HISTORICAL_EVALUATION_2016_2024.csv
- MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv
- MURPHY_0027_0029_HISTORICAL_EVALUATION_2020_2024.csv
- MURPHY_51_COVERAGE_SUMMARY_V1.csv
- RECOVERY_INDEX.md

A normalized local artifact was generated from those sources:
MURPHY_HISTORICAL_EVIDENCE_NORMALIZED_2016_2024.csv / .zip
Current normalized artifact:
- 402,710 rows after restricting timestamps to 2016–2024.
- 7 rules represented: 0003, 0004, 0021, 0022, 0023, 0028, 0029.
- 27 of the current 34 Murphy rules are still not represented by this particular recovered historical artifact.
- No missing directions/rules were invented.

## Current true blocker
The project has a real end-to-end BACKTEST runner, but it currently requires current Murphy 2016–2024 evidence fan-in. The workflow intentionally stops if MURPHY_2016_2024_FULL_EVIDENCE.csv is absent instead of using 2025 or legacy artifacts.

Therefore the next engineering task is:
BUILD SOURCE-BACKED MURPHY HISTORICAL EVIDENCE FOR THE CURRENT 34-RULE RUNTIME SCOPE FROM EXISTING PROJECT DATASETS / MAPPINGS / MTF MAPS / MARKET-STATE INPUTS / EVALUATORS.

For any Murphy rule without sufficient historical source-backed inputs:
- keep it NOT_EVALUABLE / governed unavailable state;
- never invent evidence or thresholds.

## Existing BACKTEST path
Current runner is BACKTEST/DEV_BACKTEST_RUNNER_V1.py.
It is designed to:
1. load authoritative H1 bars;
2. aggregate Murphy evidence by timestamp;
3. aggregate Nison confirmation/contradiction;
4. load recovered Decision Brain;
5. produce decision events;
6. simulate bar-by-bar trades;
7. produce events, trades, funnel, metrics and validation manifest.

Important: current runner's metrics are diagnostic unless the frozen transaction-cost/slippage contract is represented and all acceptance gates pass. Do not call diagnostic output the official profitability result.

## Exact next execution sequence
1. Inventory all Murphy mapping/evaluator/MTF/market-state files already in the workspace.
2. Derive source-backed 2016–2024 evidence for each of the 34 current Murphy runtime rules where possible.
3. Emit MURPHY_2016_2024_FULL_EVIDENCE.csv + manifest.
4. Join Murphy 34 + Nison 44 into unified_78_events_2016_2024.csv by timestamp/as-of.
5. Run recovered Decision Brain unchanged.
6. Apply Three-Book Decision evaluator.
7. Apply frozen Risk/Execution contract.
8. Run bar-by-bar 2016–2024 backtest.
9. Produce executed_trades, funnel, metrics and validation manifest.
10. Only when all gates pass, report official development P&L/Win Rate/PF/Drawdown.
11. Freeze development methodology, then evaluate 2025 as true OOS with no tuning.

## Governance locks
- Murphy provides direction.
- Nison confirms/contradicts.
- Similarity/Memory are evidence only.
- TIZ is process context only.
- Risk is a hard gate.
- 2025 must remain locked from tuning.
- Do not use legacy 2016–2018 profitability as the current system result.
- Do not change rule semantics just to increase trade count.

## Recent implementation notes
- Dropbox token is configured in CI and works.
- Nison source download/runtime imports were fixed.
- Nison Candle timestamp error was fixed by keeping timestamp outside Candle payload.
- A development Nison workflow exists and completed successfully as a governance/test workflow; this is not itself the profitability backtest.
- A real Decision Brain 2016–2024 backtest workflow was added, but it is currently blocked until the Murphy historical 34-rule fan-in artifact exists.

## Critical source files uploaded in the project/workspace
Earlier project packages include:
- AI_Trading_Assistant_CONTEXT_AWARE_RETRIEVAL_V2.zip
- AI_Trading_Assistant_MASTER_KB_V1.zip
- AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip
- AI_Trading_Assistant_TRADING_RULES_V2.zip
- AI_Trading_Assistant_NISON_CANDLE_CONFIRMATION_V1.zip
- AI_Trading_Assistant_NISON_CONTEXT_ENGINE_V1.zip
- AI_Trading_Assistant_MARKET_READER_V1.zip
- AI_Trading_Assistant_MARKET_STATE_READER_V1.zip
- AI_Trading_Assistant_MARKET_SCENARIO_ENGINE_V1.zip
- AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1.zip
- AI_Trading_Assistant_HISTORICAL_CONTEXT_MEMORY_V1.zip
- AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1.zip
- AI_Trading_Assistant_SIMILARITY_MEMORY_V2.zip
- TRUE_BACKTEST_V2.zip
- OFFICIAL_BASELINE_AUDIT_V1.txt
- VERSION_FREEZE_PLAN_V1.json
- GBPUSD_RULE_EVALUATOR_V2 workspace split archive parts

Recent uploaded mapping/audit CSVs under /mnt/data/rule_ws include:
- DYNAMIC_TIMEFRAME_SELECTION_EXAMPLES_V1.csv
- MARKET_STRUCTURE_RULE_COMPATIBILITY_AUDIT_V2.csv
- Murphy exact mappings for 0001–0051 (multiple V1/V2_RESET/V3 versions)
- MURPHY_51_COVERAGE_GAP_AUDIT_V1.csv
- MURPHY_51_COVERAGE_SUMMARY_V1.csv
- MURPHY_51_EXACT_CONDITION_PREP_V1.csv
- MURPHY_51_EXACT_RULE_MAPPING_WORKSHEET_V1.csv
- MURPHY_51_GAP_MODULES_V1.csv
- MURPHY_51_RULE_MAPPING_AUDIT_V1.csv
- MURPHY_51_RULE_TO_MTF_FUNCTION_MAP_V1.csv
- MURPHY_51_TIMEFRAME_MAPPING_AUDIT_V1.csv
- MURPHY_COMPATIBILITY_AUDIT_V1.csv
- MURPHY_GAP_PRIORITIZATION_V1.csv
- PIVOT_CONFIRMATION_AVAILABILITY_AUDIT_V1.csv
- PIVOT_CONFIRMATION_SAMPLE_V1.csv

## What the next chat must NOT do
- Do not restart from zero.
- Do not rebuild Murphy/Nison/Decision Brain.
- Do not spend the session only explaining architecture.
- Do not use 2025 to tune.
- Do not fabricate Murphy historical evidence.
- Do not present diagnostic metrics as official.
- Do not replace frozen semantics with guessed comparators.

## Immediate user goal
The user wants execution and actual results, not more setup loops.
The new chat must start at:
MURPHY 34-RULE HISTORICAL FAN-IN -> UNIFIED 78 -> DECISION BRAIN -> RISK/EXECUTION -> BACKTEST 2016–2024.

## Copy/paste prompt for the new chat
"ده الـhandoff الرسمي لمشروع AI Trading Assistant — Decision Brain. اقرأه كاملًا الأول واعتبره مصدر الحقيقة للحالة الحالية. ممنوع تبدأ من الصفر. الـDecision Brain وNison runtime وMurphy runtime موجودين. المشكلة الحالية فقط هي إكمال source-backed Murphy historical evidence للـ34 rule على 2016–2024 من الملفات الموجودة بالفعل. استخرج باقي Murphy evidence بدون اختراع أي بيانات، وبعدها نفّذ Unified 78 -> Decision Brain -> Three-Book -> Risk/Execution -> Backtest 2016–2024. 2025 OOS وممنوع استخدامه في tuning. كل خطوة لازم تنتج artifact قابل للمراجعة. ابدأ بالتنفيذ مباشرة." 
