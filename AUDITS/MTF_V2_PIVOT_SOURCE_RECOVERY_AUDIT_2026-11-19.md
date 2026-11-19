# MTF Producer V2 — Pivot Source Recovery Audit V1

Date: 2026-11-19
Scope: GitHub-only recovery of the executable source and six-timeframe coverage for the canonical `PIVOT_SEQUENCE_V2` producer.
Status: PARTIAL HISTORICAL CONTRACT RECOVERED / EXECUTABLE PRODUCER NOT RECOVERED / SIX-TF COVERAGE UNPROVEN.

## 1. Confirmed historical evidence

The repository contains commit:
- `3e429edc51915ccc1a36f8914bf7a447e9d4e282`
- Message: `audit(0008): real PIVOT_SEQUENCE_V2 integration pass`
- Date: 2026-08-15
- Audit file: `audits/MURPHY_0008_PF_B1_REAL_PIVOT_V2_INTEGRATION_AUDIT_V1.md`

That audit records the following upstream contract for `PIVOT_SEQUENCE_V2`:
- Source artifact family: `MARKET_STRUCTURE_GBPUSD_ALL_TF_V1`
- Two confirming bars on the same source timeframe.
- Pivot availability at the event row plus two bars.
- The pivot must not be available before its confirmation timestamp.
- 2025 was not used.

The audit reports a real H1 QA population:
- 17,789 H1 rows in the referenced PIVOT_SEQUENCE_V2 output.
- 15,266 pivot rows in the 2016–2024 subset.
- 7,731 LOW pivots.
- Every audited row had `availability_row - source_row = 2`.
- Every audited row had `confirmation_status = CONFIRMED_AFTER_2_BARS`.

The audit references H1 OHLC at:
`DMI_ADX_V1_OUTPUT/GBPUSD_H1_DMI_ADX_2016_2024.csv`.

## 2. What this evidence does not establish

The cited audit is an H1 integration audit. It does not establish:
- an executable pivot detector implementation or its exact source path;
- the complete pivot schema or producer code;
- verified output availability for M5, M15, M30, H4, and D1;
- consistent schema/semantics across all six timeframes;
- clock-policy authenticity or broker-time provenance;
- compatibility with the new V2 structure producer beyond the explicitly shared two-bar availability concept.

The historical report itself states that its PIVOT_SEQUENCE_V2 output was canonical upstream evidence available in a workspace snapshot. It does not include the pivot generator implementation in the audit commit.

## 3. Bounded GitHub-only search performed

Searches were run within `refaey11/AI-Trading-Assistant-Workspace` for:
- `PIVOT_SEQUENCE_V2`
- `pivot sequence`
- `MARKET_STRUCTURE_GBPUSD_ALL_TF_V1`
- `CONFIRMED_AFTER_2_BARS`
- `availability_row source_row`
- `confirmed pivot`
- `pivot producer`
- `market structure pivot`

Branch-name searches covered pivot, market-structure, PF-B1, Murphy, GBPUSD, and relevant feature/integration branch families. The historical branches `audit/murphy-0008-pf-b1-v1` and `feat/murphy-pf-b1-h1-contract-v1` were identified by branch search; the accessible commit evidence for the former is the H1 audit above.

No executable pivot detector or six-timeframe PIVOT_SEQUENCE_V2 output producer was recovered from the accessible GitHub search results. This is a bounded search conclusion, not proof that no artifact exists in any local workspace, external archive, or unindexed repository object.

## 4. Decision for MTF Producer V2

Do not fabricate or reverse-engineer the historical pivot detector from the two-bar confirmation metadata.

Keep the current V2 prototype input boundary as already-confirmed pivot events. Before any six-timeframe adapter:
1. recover the original producer or independently approve a new pivot detector contract;
2. verify the exact schema and confirmation/availability semantics separately for M5, M15, M30, H1, H4, and D1;
3. run deterministic golden fixtures and no-lookahead tests per timeframe;
4. preserve missing/unavailable states explicitly;
5. require trusted clock/provenance evidence before production eligibility.

No legacy field mapping, Decision Brain integration, direction generation, order path, 2025 tuning, or main-branch changes are authorized by this audit.

## 5. Related historical evidence

The later governance freeze commit `9a116ac99a5125639f3403fa2b06fa8d8d5b06a2` promotes minimal PF-B1/PF-H1 contracts for Murphy 0008 runtime integration. It requires confirmed pivot-derived candidates and an existing S/R role identity, but does not supply the canonical pivot detector or prove six-timeframe coverage. It must not be treated as proof of a six-timeframe producer.


## 6. Additional historical branch-tree and Murphy 0008 evidence (2026-11-19 continuation)

Two historical branch heads were inspected through their recursive Git trees:
- `fix/xauusd-confirmed-pivots-no-lookahead` at `10198e7a99a5e757d37c3771dfbf2a195b662afd` (tree `952b4a1f9efa353048ccd856a7017e6798376695`).
- `feat/murphy-pf-b1-h1-contract-v1` at `a966e1150415fb41ec01921e7ab8388f21b1cc9d` (tree `65f42a7702e7d4056a511d08ad2313fc43110b45`).

In both inspected trees, the pivot/market-structure-related paths were limited to four Murphy 0008 audit documents:
- `audits/MURPHY_0008_PF_B1_REAL_PIVOT_V2_INTEGRATION_AUDIT_V1.md`
- `audits/MURPHY_0008_PF_H1_SINGLE_PIVOT_BOUNDARY_PROPOSAL_V1.md`
- `audits/MURPHY_0008_SINGLE_PIVOT_PF_B1_CONTRACT_V1.md`
- `audits/MURPHY_0008_SINGLE_PIVOT_PF_B1_TEST_RESULTS_V1.md`

No executable pivot detector, canonical pivot output file, or six-timeframe structure producer appeared in either inspected branch tree. These are branch-head tree inspections, not an exhaustive scan of every historical Git object or external workspace.

The related Murphy 0008 documents provide additional *downstream contract evidence*, not the missing detector:
- The singleton PF-H1 freeze uses one confirmed PIVOT_SEQUENCE_V2 LOW pivot as an event-specific Support boundary, preserving pivot identity and forbidding clustering/tolerance for that 0008 validation path.
- The experimental PF-B1 contract uses the first completed D1 close below that same support as a candidate and the second consecutive completed D1 close below it as confirmation; retest observation starts only after confirmation.
- Its experimental D1 replay reports 344 confirmed LOW pivots in 2016–2024, 324 two-close break events, and 20 without such a sequence. The report explicitly says the raw authoritative `D1/GBPUSD_D1_STRUCTURE.csv` was absent from the reconstructed archive and the replay is not final authoritative QA.
- The separate real H1 integration audit reports two-bar pivot confirmation/availability and H1 population QA, but still does not contain the generator.

These facts strengthen evidence that historical pivot-derived outputs/contracts existed for particular Murphy validation paths. They do not establish that the underlying PIVOT_SEQUENCE_V2 detector is present in GitHub, that the old output schema is recoverable, or that the same producer was built and validated on M5/M15/M30/H1/H4/D1. Do not treat the Murphy 0008 singleton-support contract or D1 two-close break rule as the MTF V2 pivot detector specification.

## 7. Updated recovery decision

The original producer remains unrecovered from the inspected GitHub evidence. Keep the V2 prototype input boundary as already-confirmed pivot events. A new detector requires a separate explicit contract approval and per-timeframe golden fixtures; do not infer its left/right window, tie handling, equal-high/low policy, pivot alternation, or schema from the two-bar availability statement.
