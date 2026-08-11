# Murphy 0006–0007 Source Semantics Audit V1

Date: 2026-08-12
Status: BLOCKED / NOT_YET_EVALUABLE

## Scope

Compatibility/source audit only. No evaluator implementation, no threshold invention, no tuning, and no use of 2025 OOS data.

## Source-of-truth policy

The project Workspace / File Library artifacts remain the source of truth. GitHub is treated as a development/provenance source and must not replace the Workspace source of truth.

## Rule registry evidence

The current project state records both `MURPHY_0006` and `MURPHY_0007` as `NOT_YET_EVALUABLE` with the same registry wording:

> A third successful touch and reaction confirms the trendline.

The current state explicitly says the exact operational meaning of `successful touch`, `reaction`, `third touch`, and confirmation/availability timing has not been proven from an authoritative project source.

It also explicitly forbids assuming that 0006 is bullish and 0007 bearish, or any other split, without source evidence.

## Search performed

Searched the available File Library for:

- `MURPHY_0006` + `rule_id` + `original_rule` + `primary_source` + `setup` + `conditions`
- `MURPHY_0007` + the same metadata
- Master Rule Database / Rule Registry references
- the exact phrase `A third successful touch and reaction confirms the trendline`
- `successful touch and reaction`
- Trendline Geometry V1 metadata

Searched the linked GitHub repository for:

- files containing `MURPHY_0006`
- files containing `MURPHY_0007`
- trendline-related files / commits

## Findings

1. The available current-state artifact confirms Trendline Geometry V1 already exists. It must not be rebuilt.
2. The available rule-status artifact confirms 0006 and 0007 are both `NOT_YET_EVALUABLE`.
3. No authoritative original database record for 0006/0007 was recovered by the searches above.
4. No GitHub file or commit was found that establishes the semantic distinction between 0006 and 0007.
5. Therefore the exact touch/reaction operator cannot be frozen yet.

## Compatibility result

Trendline Geometry V1 is an existing upstream primitive, but the following contract fields remain unresolved for 0006/0007:

- trendline identity/type per rule
- what qualifies as a successful touch
- what qualifies as a reaction after the touch
- whether the third touch itself or the subsequent reaction is the confirmation event
- exact availability timestamp
- any chronology/no-lookahead requirements beyond the existing geometry contract
- any source-defined distinction between 0006 and 0007

## Prohibited actions at this stage

Do not:

- invent a touch tolerance;
- invent ATR/percentage thresholds;
- invent a lookback;
- infer bullish/bearish mapping from rule numbering;
- build an evaluator around guessed semantics;
- tune against 2016–2024 or any other historical data before the source contract is frozen;
- use 2025 for tuning or implementation selection.

## Gate decision

**MURPHY_0006–0007: NOT_YET_EVALUABLE**

The correct next action is to recover the authoritative original rule/database records and then perform the compatibility audit against Trendline Geometry V1.

Only after the source semantics are frozen should the sequence proceed:

`source semantics → compatibility → availability/no-lookahead contract → evaluator → unit tests → 2016–2024 historical QA → freeze`
