# FINAL 78-Rule Wiring Audit — 2026-08-25

## Purpose
Protect the 2025 OOS evaluation from being promoted to profitability while the final Decision Brain evidence wiring is incomplete.

## Frozen scope
The frozen Decision Brain allowlist declares 78 allowed rules: 44 Nison + 34 Murphy. The allowlist is deny-by-default and is not changed by this audit.

## What the final artifact actually contained
The successful final CircleCI artifact produced 6,225 decision events and 0 trades.

Observed source rule IDs in the Murphy candidate stream:
- MURPHY_0021
- MURPHY_0022
- MURPHY_0023

Therefore only 3 of the 34 allowlisted Murphy rule IDs were actually represented in the final candidate stream.

The Nison production artifact contains all 44 Nison rule IDs, but the final candidate builder collapsed the per-rule evidence into one timestamp-level candidate and emitted `NISON_NONE` when no directional Nison rule was available. `NISON_NONE` is not a real rule ID and was correctly rejected by the deny-by-default allowlist.

## Independent runtime/governance mismatch found
The current Murphy runtime status document says 24 Murphy rules are runtime implemented out of 35 frozen rules, while 11 remain frozen-only/runtime-unproven. The runtime entry point currently dispatches a smaller explicit set of rule IDs rather than all 34 IDs listed in the frozen 78-rule allowlist.

This means the project currently has a **canonical governance scope of 34 allowed Murphy rules**, but the current final OOS execution path does **not** have 34 Murphy runtime outputs.

## Required correction
Do not change the frozen allowlist. Do not invent missing Murphy outputs. Do not synthesize directions for unavailable rules.

The final OOS path must first be upgraded to a governed per-rule Murphy fan-in:
1. Produce/consume one evidence record per allowlisted Murphy rule ID per timestamp where source facts permit evaluation.
2. Preserve `NOT_EVALUABLE` for unavailable/deferred rules.
3. Preserve per-rule provenance instead of collapsing Murphy to one selected rule ID.
4. Aggregate only the actually available, allowlisted Murphy evidence for the timestamp-level Decision Brain handoff.
5. Keep all 44 Nison rule evidence per timestamp and use Nison only for confirmation/contradiction.
6. Pass a list of real contributing rule IDs to the Three-Book evaluator; never use synthetic sentinels such as `NISON_NONE`.
7. Only after the full governed evidence fan-in is validated should the profitability evaluator be allowed to run.

## Current status
**NOT READY for official 2025 P&L.**

The existing `FINAL_2025_TRADES.csv` is empty and the 0-trade result must not be interpreted as strategy performance; it is a wiring/governance outcome.

## Governing constraints
- 2025 remains evaluation-only.
- No tuning or threshold selection on 2025.
- Murphy remains the only directional book.
- Nison remains confirmation/contradiction only.
- TIZ remains a process/psychology gate only.
- Similarity/historical memory remains evidence only.
- Risk remains a hard execution gate.

## Evidence sources
- `governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json`
- `governance/RULE_ADAPTER_79_PROVENANCE_COMPLETENESS_AUDIT_V1.json`
- `PROJECT_STATE/CURRENT_MURPHY_24_RUNTIME_STATUS_2026-08-22.md`
- `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`
- `OOS_2025/run_final_2025_decision_brain_and_pnl_v1.py`
- `OOS_2025/full_decision_brain_historical_event_producer_v1.py`
