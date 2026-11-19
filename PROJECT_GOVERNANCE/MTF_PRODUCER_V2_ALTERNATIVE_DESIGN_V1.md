# MTF Producer V2 — Alternative Semantic Producer Design V1

**Status:** DRAFT DESIGN ONLY — no feature formulas, runtime integration, or trading behavior are implemented or authorized by this document.

**Decision basis:** The bounded GitHub-only recovery search did not locate the original executable producer for the historical six-timeframe Trend Regime / MTF Trend Score fields. The historical output artifact family exists, but the original producer semantics remain unrecovered. This document defines a safe fallback path if source recovery is formally closed.

## 1. Purpose and identity

Design a new, independently versioned six-timeframe market-structure evidence producer for M5, M15, M30, H1, H4, and D1.

This is a **new semantic implementation**, not a reconstruction or parity replacement of the historical producer. It must never claim that its outputs reproduce the historical `trend_regime` or `mtf_trend_score` formulas.

The producer supplies auditable market-structure evidence to the Decision Brain integration boundary. It does not generate a trade by itself, does not replace Murphy's governed role, does not let Nison or TIZ generate direction, does not let Similarity determine direction, and does not bypass the Risk hard gate.

## 2. Reuse existing project components

Before implementation, reuse and compatibility-audit:
- Existing six-timeframe architecture and Dynamic MTF role contract.
- Existing raw MT5 capture V1/V1.2 and separately governed V1.3 clock/provenance work; do not rebuild capture.
- Existing strict `RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py` as the only point-in-time join boundary.
- Existing source/clock provenance contracts and fail-closed behavior.
- Existing Decision Brain and evidence adapters without changing frozen module semantics.

Do not create a parallel candle aggregator, timestamp normalizer, as-of join, risk layer, or directional decision engine.

## 3. Output namespace and legacy isolation

All new outputs must use a new versioned namespace, for example:
- `mtf_v2.<timeframe>.structure_state`
- `mtf_v2.<timeframe>.confirmed_swing_high`
- `mtf_v2.<timeframe>.confirmed_swing_low`
- `mtf_v2.<timeframe>.structure_break_event`
- `mtf_v2.<timeframe>.available_at`
- `mtf_v2.aggregate.context_summary`
- `mtf_v2.aggregate.conflict_state`

These are illustrative contract names, not approved formulas or final schema.

The V2 producer must **not** silently populate legacy fields:
- `M5_trend_regime`, `M15_trend_regime`, `M30_trend_regime`
- `H1_trend_regime`, `H4_trend_regime`, `D1_trend_regime`
- `mtf_trend_score`

No adapter may rename V2 values into these legacy fields until a separate compatibility decision proves semantic equivalence. If equivalence cannot be proven, Decision Brain integration must use a separately versioned evidence contract and explicit compatibility review.

## 4. Feature semantics that must be explicitly specified before coding

The design review must approve each item below before the producer emits values:

### 4.1 Swing / pivot semantics
- Candidate swing definition and left/right confirmation requirements.
- Whether confirmation requires completed bars only.
- Equal-high / equal-low handling and price precision/tick-size policy.
- Minimum separation, if any, and how it is justified without outcome fitting.
- Exact confirmation timestamp and `available_at` semantics.
- Invalidation and replacement rules for previously confirmed swings.

### 4.2 Structure state semantics
- Exact state vocabulary, including bullish, bearish, range/neutral, transition, and unavailable where applicable.
- Whether state requires a sequence of confirmed swing highs/lows or another explicit structural condition.
- Conflict handling when evidence is incomplete or timeframes disagree.
- State persistence and reset rules.
- No use of future bars or unfinished higher-timeframe candles.

### 4.3 Structure event semantics
- Exact definition of a break of structure (BOS) and change of character (CHOCH), if included.
- Whether a break is close-confirmed or wick-triggered.
- Event timestamp, event availability, duplicate suppression, and event expiry.
- Treatment of gaps, spread, and price precision.
- Events remain descriptive evidence and cannot independently create a trade direction.

### 4.4 Aggregate MTF context
- Explicit role for each timeframe, preserving the existing Dynamic MTF contract.
- Conflict representation rather than forced averaging.
- No hidden weighting or numeric score unless a separate, documented rationale and approval exist.
- No score inferred from the old -6..+6 archive range.

### 4.5 Missingness and warm-up
- Distinguish source unavailable, insufficient warm-up, stale, invalid, and conflicting evidence.
- Never zero-impute, neutral-impute, forward-fill future context, or convert missing evidence into a bearish/bullish state.
- Every output includes source lineage, producer version, timeframe, source bar identity, and availability timestamp.

## 5. Input and clock contract

The producer accepts only validated, closed raw bars from the existing capture/ingest boundary.

Required provenance includes:
- symbol and native timeframe;
- raw OHLC and separately typed volume fields;
- source/broker identity and capture version;
- original server/source timestamp plus documented clock domain;
- trusted observation/retrieval metadata where available;
- closed-bar confirmation;
- payload hash and source lineage.

Unknown or unapproved clock policy, naive timestamps, stale data, gaps that violate the approved contract, or unfinished bars must produce unavailable/NOT_EVALUABLE evidence. Do not infer timezone, DST, close time, or broker offset from observed data.

## 6. Validation plan

### Gate V2-A — Contract approval
- Freeze the schema, state vocabulary, pivot/event definitions, missingness semantics, and clock contract.
- Produce synthetic golden fixtures with hand-calculated expected results.
- Document invariants and counterexamples before implementation.

### Gate V2-B — Pure deterministic producer
- Implement in a separate module and branch.
- No network, MT5 terminal, order, or Decision Brain side effects.
- Repeated runs over identical ordered inputs must produce byte-stable outputs.
- Test pivot confirmation delay, unfinished bars, gaps, duplicate bars, equal highs/lows, invalidation, stale data, and multi-timeframe conflicts.

### Gate V2-C — Causality and invariants
- Prove no output is available before all required source bars close.
- Prove adding future bars cannot alter previously emitted historical outputs.
- Prove as-of queries never read future evidence.
- Prove missing inputs remain unavailable and cannot become neutral/bullish/bearish defaults.

### Gate V2-D — Historical development validation
- Use only approved 2016–2024 development data after timestamp provenance is established.
- The legacy MTF archive may be used only as a descriptive reference, not as a formula target or label source.
- No fitting to trade outcomes, no feature selection against 2025, and no post-hoc threshold optimization.
- Test across supported FX symbols; XAUUSD may be included but must not be the only instrument.

### Gate V2-E — Decision Brain compatibility
- First emit a versioned evidence package without changing the existing Brain.
- Audit how the Brain can consume this package without treating it as legacy fields.
- Murphy remains technical context; Nison confirmation/contradiction only; TIZ process gate only; Similarity historical evidence only; Risk remains a hard gate.
- No BUY/SELL automation and no live orders.

### Gate V2-F — MT5 Demo evidence
- Separate, later gate after deterministic and historical validation.
- Validate six timeframe closed-bar capture, source clock, restart/replay, and end-to-end evidence lineage.
- Demo observation only; no live execution authorization.

## 7. Data governance

- 2025 remains locked OOS and must not be accessed for design tuning, calibration, thresholds, feature selection, or iterative fitting.
- Use only the existing project-approved 2016–2024 development partition after its timestamp lineage is validated.
- Preserve all original MTF archives and historical outputs unchanged.
- Do not change `main`, merge PRs, or modify frozen modules without explicit approval.
- No formula, threshold, weighting, or directional policy is introduced by this design document.

## 8. Decision and stop conditions

The alternative producer may proceed only after:
1. The bounded GitHub-only original-source search is documented as exhausted for accessible repository sources.
2. Existing architecture, raw capture, Dynamic MTF, strict join, and Brain contracts pass a compatibility audit.
3. The user approves the V2 semantic contract before implementation.
4. The V2 contract explicitly accepts that it is not historically equivalent to the missing producer.

If the source recovery later succeeds, compare the source against this design before any implementation; do not merge two incompatible semantic paths.

**Current status:** DESIGN PROPOSAL ONLY. No producer code, feature values, runtime changes, backtests, or orders are created by this document.


## 9. Compatibility audit — existing components inspected (2026-11-19)

This section records a read-only inspection of the existing GitHub components. It is not a runtime approval.

| Existing component | Verified capability | V2 reuse decision | Gap / restriction |
| --- | --- | --- | --- |
| `RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py` | Strict backward as-of join; explicit timezone-aware timestamps only; exact seven legacy fields; rejects NaN/non-numeric and missing source values | Reuse its causality principles and tests as reference | **Not directly compatible** with `mtf_v2.*`: it hard-requires legacy numeric fields and has no generic evidence-envelope schema. Do not feed V2 fields through legacy aliases. |
| `compatibility/dynamic_mtf_binding_adapter_v1.py` | Six supported TF labels, role assignments, candidate allowlists, missing/unavailable rejection | Reuse only after V2 evidence has passed a trusted provenance boundary | It does not validate source timestamps, freshness, producer lineage, or evidence identity. |
| `compatibility/dynamic_mtf_runtime_resolver_v1.py` | Deterministic role candidate order, explicit upstream completeness booleans, preserves explicit CONFLICTED state, no direction generation | Reuse as downstream role-selection reference | Caller-supplied booleans are trusted; it does not verify V2 timestamps or producer lineage. Its context-role duplication behavior is documented in the 2026-11-18 compatibility review and remains unresolved. |
| `compatibility/dynamic_mtf_opportunity_ranker_v1.py` | Selects among execution candidates from upstream evidence and supplied direction | No direct V2 dependency | It accepts caller-supplied direction and is not a market-structure producer. |
| Existing MT5 raw capture V1/V1.2/V1.3 work | Captures closed raw bars for six native TFs and keeps tick/real volume distinct | Reuse; do not rebuild candle capture | Existing compatibility audit records missing distinct raw server bar label, close-availability field, retrieval clock evidence, and explicit timezone policy ID in the current capture schema. |
| Existing PIVOT_SEQUENCE_V2 evidence (Murphy 0008 integration audit) | Canonical pivot output is reported as two confirming bars; pivot availability is event row + 2 bars on the same source TF; no 2025 used in the cited H1 QA | Candidate upstream pivot source for V2, subject to source/module/schema verification for every TF | The inspected branch contains the integration audit, not the executable producer implementation. H1 audit evidence does not prove identical output coverage/schema for all six TFs. |
| `BACKTEST/mtf_source_contract_gate_v1.py` | Checks the seven legacy fields are numeric and timestamps parse | Do not use as V2 validator | It applies `pd.to_datetime(..., utc=True)` to legacy timestamps and does not implement the V2 evidence envelope or clock-provenance gate. |

### Compatibility decision

1. Keep the existing strict legacy join unchanged.
2. Define a separate V2 evidence envelope containing per-timeframe structure facts, source bar identity, producer/schema version, `available_at`, clock provenance, and explicit availability status.
3. A future V2 as-of adapter must validate the envelope and use backward-only joins on verified availability timestamps. It must not map V2 values into the seven legacy numeric fields.
4. Dynamic MTF role selection may consume only validated evidence summaries. The current resolver is not itself a provenance validator and must not be treated as one.
5. The raw capture layer is reusable but its remaining timestamp/provenance gaps stay blocking until a separately versioned capture contract closes them.

## 10. Proposed V2 semantic baseline — NEW semantics, not historical reconstruction

The following is a concrete proposal for review and synthetic testing. It is deliberately separate from the missing historical `trend_regime` / `mtf_trend_score` producer. No item below is attributed to Murphy as a literal numeric formula.

### 10.1 Confirmed pivots

- Prefer consuming the existing canonical PIVOT_SEQUENCE_V2 output rather than creating a second pivot detector.
- The inspected H1 integration audit reports a two-confirming-bar rule and availability at the pivot event row plus two bars on the same source timeframe.
- Before six-TF implementation, verify the executable producer, schema, version/hash, and identical confirmation/availability semantics for M5/M15/M30/H1/H4/D1. Until then, non-verified TFs are unavailable.
- A pivot may be consumed only at or after its own explicit `available_at`; never at its visual pivot bar.
- Equal-price pivots, tick-size normalization, duplicate pivot identity, and invalidation rules remain explicit contract questions. Do not silently round or merge levels.

### 10.2 Structure state

Use only confirmed swing pivots, ordered by source timeframe and availability:

- Candidate `BULLISH_STRUCTURE`: the latest two confirmed swing highs form a strict Higher High (HH), and the latest two confirmed swing lows form a strict Higher Low (HL).
- Candidate `BEARISH_STRUCTURE`: the latest two confirmed swing highs form a strict Lower High (LH), and the latest two confirmed swing lows form a strict Lower Low (LL).
- Candidate `RANGE_OR_MIXED`: both sides are sufficiently populated but the HH/HL or LH/LL pair is not jointly satisfied.
- `INSUFFICIENT_PIVOT_HISTORY`: fewer than two confirmed highs or fewer than two confirmed lows are available.
- `UNAVAILABLE`: source, clock, lineage, or closed-bar validation fails.

Strict comparisons use the source's declared price precision. If equal-price handling cannot be resolved from that precision contract, return `NOT_EVALUABLE` rather than inventing a tolerance.

These are evidence labels, not trade directions. A transition from one state to another must be timestamped and traceable to the exact newly available pivot identities.

### 10.3 BOS and CHOCH event candidates

- `BOS_UP`: while the prior established state is `BULLISH_STRUCTURE`, the completed close crosses from at/below to strictly above the latest confirmed swing high that was available before the break bar.
- `BOS_DOWN`: while the prior established state is `BEARISH_STRUCTURE`, the completed close crosses from at/above to strictly below the latest confirmed swing low that was available before the break bar.
- `CHOCH_DOWN`: while the prior established state is `BULLISH_STRUCTURE`, the completed close crosses from at/above to strictly below the latest confirmed swing low available before the break bar.
- `CHOCH_UP`: while the prior established state is `BEARISH_STRUCTURE`, the completed close crosses from at/below to strictly above the latest confirmed swing high available before the break bar.
- These four event types are mutually exclusive by the prior established state. A crossing is emitted once; remaining beyond the same boundary on later bars does not create repeated events.
- Wick-only breaches are recorded, if desired, as a separate descriptive observation; they do not satisfy these close-confirmed event definitions.
- Event `available_at` is the verified availability time of the completed break bar, and must be later than the pivot's own availability. No event may use a pivot that became confirmed on the same or a later bar unless its availability ordering is explicitly proven.
- Event de-duplication, gap handling, event expiry, and repeated closes beyond the same level require a separate deterministic policy before code. Until then, emit raw event identity/evidence or mark the derived event unavailable; do not invent an expiry window.

### 10.4 MTF context and conflicts

- Preserve all six per-timeframe states and events; do not collapse them into an averaged score.
- Dynamic roles remain selected by the existing role contract, not by a new V2 performance ranking.
- Aggregate summary is a categorical evidence object: selected role/timeframe IDs, each state, latest event IDs, availability statuses, and explicit conflict list.
- If active selected roles contain both bullish and bearish structure states, aggregate status is `CONFLICTED`. Do not cancel them numerically or select the majority.
- If all active roles are directionally consistent, report `CONSISTENT_BULLISH_STRUCTURE` or `CONSISTENT_BEARISH_STRUCTURE` as descriptive context only.
- Range/mixed, insufficient, or unavailable roles remain visible and are never converted to bullish/bearish defaults.
- No `mtf_trend_score`, hidden weighting, timeframe vote count, or numeric directional bias is introduced.

### 10.5 Availability and missingness

Every emitted item must carry: symbol, native timeframe, source bar/pivot/event identity, source payload hash, producer version, schema version, clock-policy identifier, source timestamp, verified `available_at`, and status.

Statuses must distinguish at least:
- `AVAILABLE`
- `INSUFFICIENT_HISTORY`
- `SOURCE_MISSING`
- `CLOCK_UNVERIFIED`
- `STALE`
- `INVALID_SOURCE`
- `CONFLICTED`

A consumer must not forward-fill unavailable values into a later event unless an explicit, separately approved freshness/persistence contract permits it. No zero/neutral imputation.

## 11. Synthetic golden-fixture plan (hand-authored; not market data)

The first fixture set must be deterministic, small, and independent of profitability outcomes:

| Fixture | Ordered evidence | Expected result | Invariant |
| --- | --- | --- | --- |
| F01 — pivot confirmation delay | Candidate pivot at bar i; confirmation arrives only after two subsequent completed bars | Pivot unavailable at i and i+1; available at i+2 only if canonical PIVOT_SEQUENCE_V2 contract is verified for that TF | No early pivot visibility |
| F02 — bullish sequence | Two confirmed highs HH and two confirmed lows HL, all available before evaluation time | `BULLISH_STRUCTURE` | Uses only confirmed, available pivots |
| F03 — bearish sequence | Two confirmed highs LH and two confirmed lows LL | `BEARISH_STRUCTURE` | Same deterministic rule in the opposite direction |
| F04 — mixed sequence | Highs form HH while lows fail HL, or vice versa | `RANGE_OR_MIXED` | No forced directional label |
| F05 — insufficient history | Fewer than two confirmed highs or lows | `INSUFFICIENT_PIVOT_HISTORY` | No guessed state |
| F06 — close-confirmed BOS | Close strictly exceeds an already available swing boundary | One BOS event at the break bar's verified availability | Wick-only touch is insufficient |
| F07 — CHOCH | Established bullish state followed by a completed close below the latest previously available confirmed swing low | `CHOCH_DOWN` | Event cannot precede pivot availability |
| F08 — wick-only breach | High/low crosses boundary but close returns inside | No BOS/CHOCH close-confirmed event | Wick is not silently treated as close |
| F09 — MTF disagreement | Selected roles contain both bullish and bearish states | `CONFLICTED`, with both source states retained | No averaging or majority vote |
| F10 — unavailable timeframe | One role lacks verified clock or source lineage | Role remains unavailable; aggregate reports missing evidence | No neutral fallback |
| F11 — future-bar perturbation | Append arbitrary future bars after an already emitted event | All prior outputs remain byte-identical | Historical outputs are immutable to future data |
| F12 — exact availability join | Event query time is before, equal to, and after an evidence `available_at` | Before: excluded; equal/after: eligible under explicit exact-match policy | Backward as-of only |

The fixture specification must include literal OHLC/pivot identities and expected timestamps in the next contract revision. The table above is the coverage plan, not a passing test report.

## 12. Approval boundary before producer implementation

The proposed semantic baseline is now concrete enough for review, but it is not yet frozen. Before executable producer code is added, the following must be resolved in a reviewed contract revision:

1. Verify PIVOT_SEQUENCE_V2 implementation and exact output contract for all six timeframes, or explicitly approve a new pivot detector as a separate component.
2. Approve the strict HH/HL and LH/LL state vocabulary, equal-price behavior, and price precision source.
3. Approve close-confirmed BOS/CHOCH definitions, event identity, duplicate suppression, and gap behavior.
4. Approve the V2 evidence-envelope schema and its independent provenance/as-of validator.
5. Confirm Dynamic MTF role selection consumes only validated evidence and resolve its documented context-role questions without changing the frozen resolver by assumption.

Until those items are closed, PR #139 remains documentation-only and no producer code, runtime wiring, backtest, live decision, or order is authorized.


## 13. User approval and isolated prototype implementation (2026-11-19)

The user explicitly approved the proposed V2 semantic baseline. Approval applies to the new, independently versioned semantics described in this document; it does not assert historical equivalence to the missing legacy producer.

An isolated deterministic prototype has now been added under `RUNTIME/MTF_PRODUCER_V2/`:
- `mtf_structure_producer_v2.py`: consumes completed OHLC bars and already-confirmed pivots; emits per-bar categorical structure evidence and close-crossing BOS/CHOCH event candidates.
- `test_mtf_structure_producer_v2.py`: synthetic tests for confirmation delay, HH/HL and LH/LL, mixed/equal pivots, insufficient history, BOS, CHOCH, wick-only rejection, crossing-only event emission, future-bar perturbation, MTF conflict, unvalidated provenance, unclosed bars, and invalid early confirmation.
- `README.md`: isolated prototype scope and limitations.
- `.github/workflows/mtf-producer-v2-tests.yml`: GitHub Actions workflow for the synthetic test suite.

Important implementation boundaries:
1. The prototype consumes pivot events; it does not implement or replace PIVOT_SEQUENCE_V2.
2. It enforces the minimum two-bar confirmation delay reported by the inspected H1 audit, but that does not prove the canonical pivot producer/schema for all six TFs.
3. All rows explicitly remain `PROVENANCE_UNVALIDATED`; a caller-supplied clock policy identifier is not treated as proof.
4. No market-data backtest, 2025 data, Decision Brain adapter, legacy-field alias, runtime wiring, trade direction, or order path is included.
5. The synthetic suite must pass in GitHub Actions before this prototype can be called test-verified. Even after passing, the six-TF producer and independent provenance/as-of validation gates remain open.
