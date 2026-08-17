# Murphy 39-Rule Corrected Master Batch Audit V1

Source of truth: AI_Trading_Assistant_TRADING_RULES_V2 / MASTER_TRADING_RULES_V2.json.

Scope: 39 rules remaining after excluding the 12 already closed in the project workflow: 0001-0007, 0011-0012, 0030-0032.

IMPORTANT: `READY_FOR_BACKTEST` is NOT `IMPLEMENTED`, `PASS`, or `FROZEN`.
`INCOMPLETE_NEEDS_RULE_DEFINITION` is not executable until the missing definition/evidence is resolved.
No thresholds, lookbacks, tolerances, indicators, or semantics may be invented.
2025 remains OOS and cannot be used for tuning.

## 39-rule source status

| Rule | Source status | Current action |
|---|---|---|
| 0008 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0009 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0010 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0013 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0014 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0015 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0016 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0017 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0018 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0019 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0020 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0021 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0022 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0023 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0024 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0025 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0026 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0027 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0028 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0029 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0033 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0034 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0035 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0036 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0037 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0038 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0039 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0040 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0041 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0042 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0043 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0044 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0045 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0046 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0047 | READY_FOR_BACKTEST | compatibility + evaluator + tests |
| 0048 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0049 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0050 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |
| 0051 | INCOMPLETE_NEEDS_RULE_DEFINITION | resolve definition/evidence; do not implement by inference |

## Counts

- Remaining rules: 39
- READY_FOR_BACKTEST: 16
- INCOMPLETE_NEEDS_RULE_DEFINITION: 23
- Implemented/PASS/FROZEN: 0 established by this audit

## Execution policy

1. Work the 16 READY_FOR_BACKTEST rules as the executable queue.
2. For each rule: source lock -> compatibility audit -> reuse existing primitive -> evaluator -> unit/contract tests -> availability/no-lookahead -> 2016-2024 QA where applicable.
3. Do not convert a source statement into a numeric threshold unless the source/project contract explicitly supplies it.
4. Rules in INCOMPLETE_NEEDS_RULE_DEFINITION remain blocked until their missing fields are resolved from authoritative project sources.
5. Do not touch the separate Nison workstream.
6. Do not tune on 2025 OOS.

This file supersedes earlier informal batch labels that called the 39-rule queue `UNBLOCKED` based only on accelerator presence.