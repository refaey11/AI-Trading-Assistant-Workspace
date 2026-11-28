# Governed Backtest Workflow Compatibility Audit
Date: 2026-11-28

## Scope
A bounded preflight audit of the existing development backtest workflow and runner on
`current-stack-dev-backtest-2016-2024-v3`. This is not a backtest result and does not
authorize any OOS access, broker execution, or production change.

## Baseline
- Repository: `refaey11/AI-Trading-Assistant-Workspace`
- Base branch: `current-stack-dev-backtest-2016-2024-v3`
- Base commit inspected: `34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e`
- Official workflow inspected: `.github/workflows/development-decision-brain-backtest-2016-2024.yml`
- Runner inspected: `BACKTEST/DEV_BACKTEST_RUNNER_V1.py`
- Governance inspected: `PROJECT_INDEX/DO_NOT_TOUCH.md`

## Compatibility audit

| Area | Existing contract | Result | Finding |
|---|---|---|---|
| H1 source | Workflow downloads `GBPUSD_H1_2016_2025_MASTER.zip`; runner filters H1 rows to 2016–2024 after loading | CONFLICT | The workflow reads a mixed-year source containing locked 2025 data. Filtering after acquisition/loading does not satisfy the no-read OOS boundary. |
| Murphy input | Workflow recovers one of several legacy Dropbox paths | MISSING_SOURCE | The path candidates are not bound to a verified immutable file ID/revision or an approved physically partitioned source. |
| Nison input | Workflow downloads `NISON_2016_2024_FULL_EVIDENCE.csv` and checks 2016–2024, 44 rules, and row count | ADAPTER_REQUIRED | The runner interface is not fully wired to the source manifest and its exact artifact identity. The Nison scope check alone does not prove whole-run dataset lineage. |
| Market State | Workflow downloads one of two candidate paths | MISSING_SOURCE | No verified immutable source identity/revision or complete source contract was established in this audit. |
| MTF | Runner requires `--mtf`; workflow does not acquire/pass it | MISSING_SOURCE | Required runner input is absent from the workflow. |
| Historical Context | Runner requires `--historical-context`; workflow does not acquire/pass it | CONFLICT | Prior audit found only mixed-year context/outcome files; no physically isolated 2016–2024 source was verified. Do not read mixed files and filter afterward. |
| Historical Outcome | Runner requires `--historical-outcome`; workflow does not acquire/pass it | CONFLICT | Same physical-isolation and provenance blocker as Historical Context. |
| Similarity / Retrieval | Runner requires `--similarity` and `--retrieval`; workflow does not acquire/pass them | MISSING_SOURCE | Required inputs and their approved development-period contracts are not established. A known 2025 retrieval snapshot must remain excluded. |
| Risk / execution simulation | Runner uses a fixed 0.75 ATR stop and 3R target; execution enters at event close; costs are explicitly not applied | CONFLICT | This is diagnostic simulation, not broker-realistic profitability testing. Canonical risk and broker cost/lot constraints must not be inferred from these assumptions. |
| Runner invocation | Workflow passes only H1, Murphy, Nison, context and output; runner CLI requires H1, market, MTF, Murphy, Nison, historical context, historical outcome, similarity, retrieval and output | CONFLICT | Current workflow invocation cannot satisfy the runner CLI contract. |

## Protected boundaries
- 2025 remains locked OOS: no acquisition, reading, filtering, tuning, calibration, selection, or development use.
- Murphy remains the sole directional evidence source under the current allowlist.
- Nison remains confirmation/contradiction only.
- Similarity and historical memory remain evidence only and cannot generate direction.
- TIZ remains optional/unresolved metadata; never silently PASS it.
- Canonical Risk remains a hard gate; do not substitute legacy research adapters.
- Existing Decision Brain and knowledge files must not be rebuilt or semantically altered.

## Decision
**BACKTEST DISPATCH BLOCKED — SAFE FAIL-CLOSED.**

Do not run the current workflow. It acquires a mixed 2016–2025 H1 archive, lacks required runner inputs, and does not apply trading costs. Do not patch around these blockers by inventing paths, fabricating inputs, reading mixed-year memory files, or changing runner semantics.

## Smallest safe next actions
1. Obtain/identify a physically partitioned, source-proven H1 2016–2024 artifact. No mixed-year archive may be downloaded or read for this run.
2. Verify immutable source IDs/revisions and approved 2016–2024 partitions for Murphy, Nison, Market State, MTF, Historical Context, Historical Outcome, Similarity and Retrieval.
3. Reconcile runner/official workflow input contracts and add preflight validation that fails before any download if a required artifact is missing or not explicitly scoped to 2016–2024.
4. Audit event timing, as-of joins, no-lookahead, ambiguous SL/TP bars, position overlap, costs, spread, commission, slippage and swap before interpreting any profitability metrics.
5. Only then run the existing governed runner/workflow, capture exact commit SHA, logs, manifests and artifacts, and report metrics with their limitations.

## Changes and verification
- No production source, Decision Brain, risk, book knowledge, frozen rule, or OOS file was changed.
- No workflow was dispatched.
- No historical dataset was downloaded or opened in this audit.
- No tests or backtest were run.
- This document records the compatibility blockers; it is not a PASS, profitability result, or release approval.
