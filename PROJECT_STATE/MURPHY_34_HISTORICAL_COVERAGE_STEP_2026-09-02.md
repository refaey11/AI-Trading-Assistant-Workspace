# Murphy 34 Historical Coverage Step — 2026-09-02

## Starting checkpoint
- Master checkpoint: `PROJECT_STATE/AI_TRADING_ASSISTANT_MASTER_CHECKPOINT_2026-09-02.md`
- Diagnostic branch: `diagnostic/mtf-gate-observable-2026-09-02`
- Last implementation commit before this step: `64d17c3236a1311968a4d248b01fe36a17ec862d`

## Finding confirmed before implementation
- Murphy governed runtime boundary: 34 rules.
- Murphy 0008 remains explicitly blocked / outside the governed 34.
- Current historical evidence feed exposes only 7 distinct Murphy rule IDs with source rows in the prior diagnostic replay.
- This is a historical evidence/fan-in coverage limitation, not proof that the other runtime evaluators are missing.
- Repository history confirms 0018/0019 and 0025/0026 have runtime implementations and tests.

## Work performed
1. Added `BACKTEST/MURPHY_34_HISTORICAL_COVERAGE_AUDIT_V1.py`.
2. The audit loads the frozen 34-rule allowlist and the supplied historical Murphy CSV.
3. Compound `source_rule_id` values such as `MURPHY_0025|MURPHY_0026` are split losslessly for coverage accounting.
4. Every governed Murphy ID receives an explicit row in the audit, even when no historical source row is present.
5. The audit distinguishes `SOURCE_BACKED` from `RUNTIME_ONLY` and separately counts rules with directional PASS evidence.
6. Unknown rule IDs fail the audit.
7. The audit is restricted to 2016–2024 and records `2025_locked=true`.
8. The audit explicitly records `synthetic_evidence_created=false`.
9. Updated `.github/workflows/development-decision-brain-backtest-2016-2024.yml` to run the Murphy 34 coverage audit before the development backtest and to retain the coverage report as an artifact.

## What this step does NOT do
- It does not fabricate historical evidence.
- It does not change Murphy rule semantics.
- It does not change Risk constants.
- It does not tune thresholds or risk.
- It does not claim all 34 rules are historically source-backed yet.
- It does not make a profitability claim.

## Expected next evidence
The next diagnostic run should produce:
- a complete 34-row Murphy coverage report;
- exact source-backed rule count;
- exact directional-PASS rule count;
- explicit runtime-only rules;
- no unknown Murphy IDs.

## Next implementation target
Build the actual historical producer/fan-in path that evaluates the existing 34 Murphy runtime evaluators against authoritative pre-2025 inputs where each evaluator's required evidence exists, while preserving `NOT_EVALUABLE` where upstream evidence is legitimately unavailable. Then validate on a bounded 2016–2024 sample before the full strict-as-of replay.
