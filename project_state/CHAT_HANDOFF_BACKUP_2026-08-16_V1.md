# AI Trading Assistant — Chat Handoff Backup V1

Date: 2026-08-16
Purpose: Continue this project safely in a new chat if the current chat becomes slow, hangs, or breaks.

## 1. Canonical project state
- Total Murphy rules: 51.
- Frozen/closed: 12.
- Frozen IDs: 0003, 0004, 0006, 0007, 0008, 0021, 0022, 0023, 0025, 0026, 0028, 0029.
- Remaining queue: 39 rules.
- Do NOT reopen the 12 frozen rules unless there is contradictory evidence, an approved semantic change, or a formal change request requiring compatibility audit + re-freeze.
- Canonical next rule is 0030.
- Start 0030 with Compatibility Audit.

## 2. Global non-negotiable governance
- Workspace/project files and latest canonical records are source of truth.
- Audit existing project knowledge before rebuilding anything.
- Compatibility audit is mandatory before new integration.
- Do not invent operators, thresholds, tolerances, timeframes, lookbacks, proxies, percentages, ATR/pip distances, or scoring weights.
- NOT_EVALUABLE is preferred over fabricated evidence.
- 2025 is OOS and must not be used for tuning, selection, calibration, optimization, or operator choice.
- Murphy = technical context / market structure.
- Nison = confirmation.
- Trading in the Zone = psychology/process gate only; it cannot generate direction.
- Similarity Engine = historical evidence only; never the sole decision maker.
- Decision Brain combines current market evidence, book knowledge, historical memory, and risk.

## 3. Main accelerator agreed in this chat
Use a Hybrid Rule Factory for the remaining 39 rules, combined with Evidence-First verification, compatibility gates, availability/no-lookahead checks, deterministic tests, historical QA, and explicit freeze governance.

Hybrid clause types:
- HARD_CANONICAL: execute literally from approved canonical contract.
- QUALITATIVE_MEASURABLE: reuse only an explicitly compatible approved primitive through a documented adapter.
- QUALITATIVE_UNMEASURABLE: remain NOT_EVALUABLE until a source-bounded operationalization is approved.
- EVIDENCE_ONLY: preserve context/evidence; does not create direction or scores.

No fuzzy scoring and no auto-freeze.

## 4. GitHub current working branch / PR
Repository: refaey11/AI-Trading-Assistant-Workspace
Working branch: feature/murphy-hybrid-rule-factory-v1
PR: #18 — [DRAFT] Murphy Hybrid Rule Factory V1 for remaining 39 rules
PR URL: https://github.com/refaey11/AI-Trading-Assistant-Workspace/pull/18
PR is OPEN, DRAFT, not merged.
Latest head commit: 888bb49023e565d2900c312a15d3af4fb372a8d6
Latest commit message: ci: install pytest before Murphy 0030 hybrid gate

## 5. 39-rule batch queue
File: project_state/MURPHY_39_BATCH_AUDIT_QUEUE_V1.csv
Validator: tools/validate_murphy_39_batch_queue.py
The validator enforces:
- exactly 39 rows;
- no duplicate IDs;
- none of the 12 frozen IDs can re-enter;
- protected == NO;
- no 2025 values in the queue.
The queue is an integrity gate, not a rule evaluator.

## 6. Hybrid factory manifest
File: project_state/MURPHY_HYBRID_39_FACTORY_MANIFEST_V1.csv
Architecture contract: contracts/MURPHY_HYBRID_RULE_EVALUATOR_ARCHITECTURE_V1.md
Factory does NOT auto-freeze rules. Each rule still needs its own source, compatibility, evidence, availability/no-lookahead, deterministic QA, historical QA, provenance, and governance gates.

## 7. Current 0030 status
Rule: MURPHY_0030
Status: IN PROGRESS / COMPATIBILITY AUDIT; NOT FROZEN.
Canonical source record recovered from Master KB.
Setup: P&F bullish support.
Direction: BULLISH.
Source semantics recovered:
- 3-box / 3-point reversal P&F method.
- High/Low construction.
- 45-degree trendlines on 3-point-reversal charts.
- Bullish support line rises at 45 degrees from under the lowest O column.
- While price remains above the bullish support line, the major trend is bullish.
- Trendline is structural context; it is not itself a trading strategy.

Known open 0030 gates:
1. engine HighLow/3-box behavior equivalence;
2. approved/source-faithful box-size policy;
3. availability/no-lookahead compatibility;
4. deterministic replay;
5. unit tests;
6. 2016–2024 historical QA;
7. availability/leakage audit;
8. provenance;
9. freeze manifest/governance.

Do NOT choose box size by historical optimization. Do NOT import ATR/%/pip box-size rules and call them Murphy. Do NOT use 2025.

## 8. External P&F candidate
Candidate discovered: pnf-chart-system, Python import pypnf, version 0.2.0 used in the smoke workflow.
It is a candidate only, NOT yet integrated and NOT certified as Murphy-equivalent.
It exposes HighLow construction, Traditional box-size method, reversal=3, X/O columns, and bullish-support checks.
Decision: do not rebuild a P&F engine yet. Compatibility-test candidate first; if compatible, use the smallest adapter. If incompatible, identify the smallest missing behavior.

Harness file: project_state/MURPHY_0030_EXTERNAL_PNF_COMPATIBILITY_HARNESS_V1.md
Smoke tests: tests/murphy_0030/test_pypnf_candidate_smoke.py
Smoke workflow: .github/workflows/murphy-0030-pypnf-candidate-smoke.yml
The smoke test proves API/feature availability only; it does NOT certify semantic equivalence or approve box size.

## 9. Latest CI problem and fix
A previous 0030 Hybrid Gate run failed before tests because pytest was not installed. Log showed: No module named pytest.
This was a CI environment failure, not a Murphy 0030 semantic failure.
Fixed in commit 888bb49023e565d2900c312a15d3af4fb372a8d6 by adding:
python -m pip install --upgrade pip pytest
before the 0030 hybrid tests.
The new run must be checked before claiming PASS.

## 10. Exact next action in a new chat
1. Read START_HERE_FOR_ANY_CHAT.md.
2. Read this handoff backup.
3. Verify latest PR #18 head and CI status.
4. Check the new 0030 Hybrid Gate run after commit 888bb49023e565d2900c312a15d3af4fb372a8d6.
5. If the gate passes, continue the real 0030 compatibility harness.
6. Run/verify the pypnf smoke workflow, then compare behavior against Murphy semantics C1–C4.
7. Keep box size policy unresolved until source-faithful governance is established; do not tune it.
8. Only after semantic/operator closure proceed to 2016–2024 Historical QA.
9. Do not move to 0031 as the official next rule until 0030 is Frozen or explicitly Blocked.

## 11. Do not lose this project direction
The goal of the Hybrid Factory is speed through standardized mechanics, NOT shortcutting governance. The 39 rules can enter the factory together, but each rule must retain its own semantics and gates. A successful code generation or smoke test is never equivalent to a Production Freeze.
