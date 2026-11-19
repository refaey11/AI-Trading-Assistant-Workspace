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
