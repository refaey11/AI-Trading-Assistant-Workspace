# AI TRADING ASSISTANT — PROJECT HANDOFF / RECOVERY STATE

Date: 2026-08-29
Branch: backtest-only-2026-08-28
Repository: refaey11/AI-Trading-Assistant-Workspace

## PURPOSE
Continuity checkpoint for moving the project to a new ChatGPT chat without losing execution state, fixes, blockers, architecture, or next actions.

## NON-NEGOTIABLE RULES
- Long-term AI Trading Assistant / Decision Brain, NOT a simple indicator.
- John Murphy = technical context / market structure / primary directional evidence.
- Steve Nison = confirmation / contradiction evidence; not an independent final direction generator.
- Trading in the Zone (TIZ) = process/psychology gate only; cannot generate direction; missing/unresolved TIZ must not become PASS.
- Similarity Engine = historical memory/evidence only; never sole decision maker or direction generator.
- Historical Context Memory and Historical Outcome Memory = historical evidence only; cannot generate direction.
- Dynamic MTF / Time Context supplies multi-timeframe context upstream of final evidence aggregation.
- Risk = explicit execution/risk gate; missing execution inputs must fail closed.
- 2025 = OOS/LOCKED; never use 2025 for tuning or development selection.
- Development backtest scope = 2016-2024.
- Audit and integrate existing project knowledge; do not rebuild from scratch.
- Compatibility audit before any new integration.

## MASTER ARCHITECTURE
Market Data -> Market Reader -> Market State -> Market Structure -> Dynamic MTF / Time Context -> Current Market Evidence (Murphy + Nison + TIZ process) -> Historical Evidence (Similarity + Historical Context + Historical Outcome) -> Rule/Evidence Normalization -> Knowledge Alignment -> Evidence Agreement/Contradiction Gate -> DECISION BRAIN -> LONG/SHORT/NO TRADE -> Risk Gate -> Position Sizing -> Execution Contract -> MT5 Demo -> Monitoring -> Real MT5 only after all gates.

## CURRENT STATUS
### Confirmed working / proven in recent runs
- GitHub repository is accessible and writable.
- Branch `backtest-only-2026-08-28` is the active governed development branch.
- CircleCI `build_and_test` passed after the last syntax fix.
- Dropbox acquisition worked after updating `DROPBOX_ACCESS_TOKEN`.
- Earlier governed run showed Murphy canonical PASS and Nison canonical PASS for 2016-2024; Nison report had 2,428,448 rows and 44 rules.
- Earlier H1 integrity check: 61,417 rows, 2016-2025, no duplicate timestamps, OHLC integrity valid.
- Canonical E2E contract exists and checks evidence-layer presence, memory/retrieval non-direction behavior, TIZ process-only behavior, explicit risk gating, Decision Brain execution, and 2025 lock.

### Fixes completed
1. Murphy canonical schema mismatch: canonical uses `rule_id`; the gate had expected `source_rule_id`.
2. Risk runtime probe was corrected to use numeric execution inputs while preserving Risk Engine policy.
3. `BACKTEST/GOVERNED_RUNNER_STATIC_LINT_V1.py` Python SyntaxError was fixed.
4. CircleCI lightweight automatic `build_and_test` workflow was restored.
5. Several noisy/duplicate GitHub Actions workflows were changed to manual-only to stop uncontrolled runs.
6. CircleCI governed trigger bridge was revised to resolve the pipeline definition ID and use the `/pipeline/run` endpoint, but this trigger is NOT yet proven end-to-end.

## CI / CIRCLECI STATE
### `.circleci/config.yml`
Pipeline parameters:
- `run_integration_gate` default false
- `run_governed_backtest` default false

Automatic cheap workflow:
- checkout
- lightweight dependencies
- Canonical E2E integration contract test
- compileall

Governed workflow:
- canonical contract
- governed smoke preflight
- source acquisition
- frozen scope / 2025 lock check
- GOVERNED INTEGRATION GATE V3
- optional 2016-2024 governed backtest only when explicitly parameterized

The CircleCI project visible in UI is `Ai my`, connected to this GitHub repository and branch.

### Important CI result
Commit `0c4d567f4137ff42f7bd1d4bd1f85882cc2de7f7` had status:
`ci/circleci: build_and_test = success`
Target workflow:
https://app.circleci.com/workflow/65ade20d-4f12-41a6-a306-137c4a4cef97/job/44d479eb-a081-413d-8ee8-06fa12db6505

## GITHUB WORKFLOW HYGIENE
These were moved to manual-only during cleanup:
- `.github/workflows/0006-0007-deterministic-audit.yml`
- `.github/workflows/actions-smoke-test.yml`
- `.github/workflows/decision-brain-progressive-gate.yml`
- `.github/workflows/overnight-0006-0007-runner.yml`
- `.github/workflows/overnight-0006-0007-smoke-test.yml`

Governed Integration Gate is intended to be the official manual execution path.

## TRIGGER BRIDGE
`.github/workflows/trigger-circleci-governed.yml` is manual-dispatch oriented and supports:
- `integration_gate`
- `backtest_2016_2024`

A previous trigger run successfully resolved CircleCI project/pipeline definition access but failed while creating the CircleCI pipeline. Therefore do NOT claim API-trigger success until a real CircleCI workflow containing the governed job is visible.

## LAST GOVERNED-GATE STATE
The gate previously progressed through:
- Dropbox acquisition: success
- Murphy canonicalization: success
- Nison canonicalization: success
- Market State / MTF: success
- Historical Context / Outcome: connected
- Similarity / Context-Aware Retrieval: connected as governed metadata/evidence
- TIZ: unresolved/process-only; never promote to PASS
- Decision Brain: contract execution reached it
- Risk: previous failure came from a bad test probe passing None, not from a proven policy failure

## KNOWN FAILURE HISTORY
### CircleCI API 403
Earlier API attempts returned 403 at pipeline creation. Project resolution itself worked. Latest bridge was revised to use pipeline definitions and `/pipeline/run`, but a fresh end-to-end proof is still required.

### Risk probe
Previous failure:
`'<=' not supported between instances of 'NoneType' and 'int'`
The probe was passing None execution values. Risk Engine requires numeric values and is intended to fail closed with `MISSING_EXECUTION_INPUT` when inputs are absent. Probe was corrected.

### Static lint SyntaxError
Previous CircleCI failure occurred before tests due to invalid Python syntax in `GOVERNED_RUNNER_STATIC_LINT_V1.py`. This was fixed and a subsequent cheap build passed.

### Too many runs
The old branch state had multiple push/schedule/diagnostic workflows that created many unrelated runs. Cleanup separated cheap CI from governed execution.

## WHAT IS DONE
- Architecture and project governance documented.
- Historical/Similarity evidence integration exists.
- Historical Context Memory exists.
- Historical Outcome Memory exists.
- Decision Brain handoff exists.
- Dynamic MTF compatibility work exists.
- Market Reader/Market State compatibility work exists.
- Nison 44-rule canonicalization/development work exists.
- Murphy 34-rule canonicalization/development work exists.
- TIZ process-only boundary exists.
- Risk runtime integration exists.
- Canonical E2E integration contract exists.
- CircleCI cheap build-and-test currently passes.
- Duplicate automatic legacy workflows were substantially reduced.
- 2025 remains locked/OOS.

## WHAT REMAINS
1. Prove a fresh CircleCI governed Integration Gate run on the current corrected commit.
2. Confirm a real CircleCI workflow with the governed job is created and completes.
3. If Gate fails, fix ONLY the first real blocker; do not start backtest.
4. Once Gate PASS, run the governed 2016-2024 backtest.
5. Analyze actual results: trade count, expectancy, drawdown, win/loss distribution, decision funnel, execution behavior.
6. Re-verify the historical observation that some earlier tests produced zero trades; it is not a current validated metric.
7. Freeze Decision/Risk/Execution contracts only after validation.
8. MT5 Demo only after gates/freeze.
9. Monitoring before Real MT5.

## IMMEDIATE NEXT ACTION — DO NOT DEVIATE
A) Use the working CircleCI project `Ai my`.
B) Trigger ONLY the governed Integration Gate.
C) `run_integration_gate=true`, `run_governed_backtest=false`.
D) Read the actual job/log result.
E) PASS -> only then run 2016-2024 backtest.
F) FAIL -> repair blocker and repeat Gate only.

## IMPORTANT DISTINCTIONS
- CircleCI pipeline shell != workflow execution.
- `build_and_test PASS` != Integration Gate PASS.
- Integration Gate PASS != profitable trading system.
- Code readiness != validated trading performance.
- Historical zero-trade observation must be re-verified, not assumed.

## NEW-CHAT INSTRUCTIONS
Read this file first. Then inspect the active branch and latest CircleCI result. Do not rebuild the architecture. Do not run broad diagnostics. Do not touch 2025 for tuning. Keep execution governed and singular.

## RECENT VERIFIED COMMITS
- `3fa84ceed3f79845828d34b935471c707a140850` — restored cheap CircleCI automatic build-and-test workflow.
- `b4e0e6e0fb09a07d93b801716b0fd6afab3bda73` — fixed governed runner static-lint syntax error.
- `dfe10e08131827fb78b9e8c2485231c93af863f6` — trigger bridge revision.
- `0c4d567f4137ff42f7bd1d4bd1f85882cc2de7f7` — commit with verified CircleCI build_and_test success.

## USER REQUIREMENT
The project must be treated as a real long-term Decision Brain build. No fake run claims, no uncontrolled credit-burning runs, no accidental 2025 tuning, and no unnecessary architecture rebuilds.
