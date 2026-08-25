# AI Trading Assistant — MTF Runtime Resolution Preflight

Date: 2026-08-26

## Verified source state

The new workspace contains a Dynamic Timeframe Selection Policy with the available native project timeframes:
- M5
- M15
- M30
- H1
- H4
- D1

The policy states that the Decision Brain reads all available timeframes first, generates candidate execution timeframes, evaluates evidence completeness and risk feasibility, records the selected timeframe and reasons, and must not invent a fixed timeframe hierarchy.

## Critical finding

`MURPHY_51_RULE_TO_MTF_FUNCTION_MAP_V1.csv` contains exactly 51 Murphy rules and all 51 have:

`timeframe_resolution = UNRESOLVED_BY_RULE`

The mapping contract explicitly says timeframe resolution must come from an explicit MTF policy/runtime and must never be guessed from the rule name.

## Execution implication

The project has timeframe data and a policy definition, but the inspected workspace does not contain a concrete runtime resolver/selection artifact that turns the policy into per-event outputs:

- selected_execution_timeframe
- context_timeframes_used
- confirmation_timeframes_used
- holding_horizon
- selection_reasons
- rejected_candidate_reasons
- status

Therefore a true 2016-2024 Shadow Arbitration run must NOT be treated as valid until this runtime resolution layer is present and produces auditable per-event bindings.

## Do not do

- Do not assign static timeframes to Murphy rules based on rule names.
- Do not invent D1/H4/H1/M30/M15/M5 hierarchy.
- Do not tune any threshold or weighting on 2025 OOS.
- Do not reinterpret Murphy or Nison semantics to make trades appear.

## Required next implementation gate

Build/restore the missing MTF Runtime Resolver using the existing Dynamic Timeframe Selection Policy only. The resolver must:

1. Read all available timeframe evidence.
2. Generate candidate execution timeframes.
3. Evaluate structure/setup/confirmation completeness and risk feasibility.
4. Preserve higher-timeframe conflict semantics.
5. Emit the six auditable outputs above for every event.
6. Fail closed when no candidate is valid.
7. Produce deterministic traces suitable for 2016-2024 validation.

Only after this gate passes should the Direction Arbitration V2 Shadow Audit be executed.

## Status

BLOCKED — not by missing M5/M15/M30 data, but by missing concrete runtime resolution from the already-defined Dynamic MTF policy to per-event timeframe bindings.
