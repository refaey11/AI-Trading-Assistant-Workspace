# Remaining 48 Rules Master Queue V1

Date: 2026-08-12

## Correct remaining count

After reconciling the authoritative 102-rule registry with the work already performed in this chat:
- Murphy 51: initial verification/closure inventory already processed.
- Steve Nison: 3 rules explicitly processed (0026, 0030, 0031).
- Trading in the Zone: 0 processed.

Therefore the exact remaining unprocessed rule count is **48**, not 62:
- Steve Nison: 41 remaining (44 total - 3 processed)
- Trading in the Zone: 7 remaining

## Registry source

Authoritative registry: `02_Trading_Rules_V2/MASTER_TRADING_RULES_V2.json`.
It contains exactly 102 rules and records 23 READY_FOR_BACKTEST + 79 INCOMPLETE_NEEDS_RULE_DEFINITION. All 102 registry testing statuses are UNTESTED.

## Execution batches

Batch A — 20 rules
- First 20 remaining Nison rules, prioritizing READY_FOR_BACKTEST and existing evaluator infrastructure.

Batch B — 20 rules
- Next 20 remaining Nison/Zone rules, same priority.

Batch C — 8 rules
- Final 8 remaining rules.

## Rule closure protocol

For every rule:
1. Authoritative source/registry row
2. Mapping
3. Existing feature compatibility
4. Dynamic MTF role where applicable
5. Exact operator/logic
6. Existing evaluator
7. Unit tests
8. Historical/provenance QA
9. Freeze only when all required gates pass

`READY_FOR_BACKTEST` is not the same as tested/frozen. The registry itself marks testing as UNTESTED. Existing evaluator artifacts also do not imply semantic freeze.

## Architectural controls

- Decision Brain V1/V1.1 already exists; do not rebuild.
- Rule Adapter is normalization only.
- Murphy = technical context.
- Nison = confirmation only and cannot create direction alone.
- Trading in the Zone = process/psychology gate only and cannot generate direction.
- Similarity = historical evidence only.
- Risk = hard gate.
- 2025 remains OOS and cannot be used for tuning, threshold selection, feature/model/rule optimization.
- Do not invent missing thresholds/operators/timeframes.

## Current objective

Finish the remaining 48 rule definitions/evaluators/tests as far as the authoritative project evidence permits, while preserving blockers explicitly. Once the 102-rule closure set is complete enough for integration, return to Decision Brain compatibility/integration, then baseline/walk-forward gates.
