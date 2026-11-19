# MTF Seven Features Forensic Recovery Audit V1

**Audit date:** 2026-11-19  
**Status:** `BLOCKED_SOURCE_IMPLEMENTATION_NOT_RECOVERED`  
**Scope:** Read-only forensic recovery of the seven serialized MTF Decision Brain input fields.  
**Base:** PR #133 head `2c7f132e5825bcd7079e38f26246c07c45313bef`.

## Executive finding

The canonical GBPUSD M5 MTF archive is confirmed as a real, pinned historical artifact, but its producer implementation and semantic contract have not been recovered. The archive contains serialized outputs, not the source code that generated them. Observed value ranges and missing-value patterns are not sufficient to infer formulas.

**No feature formula is approved for implementation by this audit.** The existing strict join adapter and PR #133 lineage validator remain validation components only; neither is the producer.

## Evidence reviewed

1. Existing repository audit: `AUDITS/MTF_SOURCE_COMPATIBILITY_AUDIT_2026-11-16.md` (branch `mtf-source-audit-report-2026-11-16`).
2. Canonical archive identity recorded by that audit:
   - Dropbox path: `/MTF_ALIGNMENT_GBPUSD_V1.zip`
   - pinned revision: `01659665ff5a6d300000003796dcfe3`
   - size: 80,293,251 bytes
   - SHA-256: `f2149e7d3051ea0c5b205a82ae9e187b2eac292bafbac1cd2db512f0e902ed53`
   - acquisition/verification run: [43797854505](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43797854505)
3. Full-project archive source search recorded by the existing audit:
   - path: `/AI_Trading_Assistant_FULL_PROJECT_V1.zip`
   - pinned revision: `0165966394fea0c00000003796dcfe3`
   - size: 134,687,505 bytes
   - SHA-256: `f3f2b2452970a9a2afc13943a70f6c319bb0d14dc5cbd37a24d1cb184556ae26`
   - search run: [43798060902](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43798060902)
4. The source-search report found no six-timeframe producer-code candidate in the inspected full-project archive text/code scope. The canonical MTF archive itself contained no `.py`, `.ipynb`, or `.sql` producer files.
5. The older `MULTI_TIMEFRAME_READER_V1` package is documented as research-only H4/H1 and is not an authority for the six-timeframe M5/M15/M30/H1/H4/D1 producer.
6. PR #133 provides cryptographic lineage validation only. Its own scope explicitly says it is not wired to a producer and does not define formulas.

## Seven-field recovery matrix

| Field | Serialized evidence | Formula / semantic contract | Status |
|---|---|---|---|
| `M5_trend_regime` | Present in canonical 106-column schema; observed regime encoding family includes -1, 0, +1 | No authoritative producer code or definition of bearish/neutral/bullish conditions, thresholds, inputs, warm-up, or missing behavior recovered | **UNRESOLVED** |
| `M15_trend_regime` | Present; 26 blank cells in 2016–2024 profile | Same unresolved contract; blanks must not be replaced with zero | **UNRESOLVED** |
| `M30_trend_regime` | Present; 53 blank cells | Same unresolved contract; timeframe close/alignment and warm-up behavior unproven | **UNRESOLVED** |
| `H1_trend_regime` | Present; 107 blank cells | Same unresolved contract; timeframe close/alignment and warm-up behavior unproven | **UNRESOLVED** |
| `H4_trend_regime` | Present; 371 blank cells | Same unresolved contract; timeframe close/alignment and warm-up behavior unproven | **UNRESOLVED** |
| `D1_trend_regime` | Present; 1,955 blank cells | Same unresolved contract; timeframe close/alignment and warm-up behavior unproven | **UNRESOLVED** |
| `mtf_trend_score` | Present; observed serialized range -6 to +6 | No authoritative aggregation formula, weights, neutral handling, missing-value policy, or exact relationship to six regime fields recovered | **UNRESOLVED** |

**Important:** The seven fields above are the serialized Brain inputs. The audit also observed aggregate/context columns such as `mtf_bullish_count`, `mtf_bearish_count`, `mtf_neutral_count`, and `mtf_context`; they are not substituted for the seven Brain inputs and their semantics are not inferred here.

## Data facts that are established (2016–2024 only)

- Nine annual files, 2016 through 2024.
- 671,601 rows total.
- 106 columns per annual file; annual headers match.
- Declared base timeframe M5; declared aligned timeframes M5, M15, M30, H1, H4, D1.
- README declares higher-timeframe values are joined only after the source candle closes. This is a declared architecture statement, not independent proof of producer behavior.
- All serialized timestamps are naive: no timezone offset or timezone identifier.
- Observed regime values: -1, 0, +1.
- Observed `mtf_trend_score` range: -6 to +6.
- 2,512 blanks across the six timeframe regime fields: M15 26, M30 53, H1 107, H4 371, D1 1,955; M5 blanks were not reported in the audit summary.
- Annual-start clustering is consistent with higher-timeframe warm-up, but that interpretation is not proven by source code.

No market rows from 2025 or 2026 were used in this audit. The source audit explicitly states it inspected only 2016–2024 rows.

## Runtime defects already evidenced

The existing compatibility audit identified that `BACKTEST/DEV_BACKTEST_RUNNER_V1.py`:
- applies `pd.to_datetime(..., utc=True)` to naive source timestamps, silently assuming UTC;
- initializes the seven MTF inputs to `0.0`, turning missing evidence into neutral-looking values;
- reads legacy `trend` / `h4_trend` mappings rather than directly selecting the canonical seven fields;
- does not directly copy the canonical MTF fields into the Brain input row;
- expects an `atr` field not present in the inspected 106-column MTF schema.

Do not use that path for an authorized performance evaluation until its source contract is resolved. Do not patch around these defects by guessing.

## Required evidence to move a field out of UNRESOLVED

For each of the six regime fields:
1. Original source implementation or authoritative specification with exact formula/decision thresholds.
2. Exact input columns and their definitions, units, lookbacks, and timeframe.
3. Candle timestamp convention and close-boundary/as-of alignment semantics.
4. Warm-up period and missing-value behavior (including first valid output).
5. Lookahead prevention and whether only closed candles are used.
6. Deterministic expected outputs from known fixtures, including boundary cases.
7. Reproduction against a pinned subset of 2016–2024 serialized outputs, with discrepancies explained.

For `mtf_trend_score` additionally:
1. Exact aggregation formula and weights (if any).
2. Whether it is a direct sum, weighted sum, or another defined transformation.
3. Treatment of neutral, missing, and unavailable timeframe values.
4. Range constraints and exact score-to-input relationship.
5. Deterministic fixtures proving every possible contribution and boundary.

## Safe implementation decisions

- Keep every one of the seven fields **UNRESOLVED** until its own evidence is sufficient.
- Preserve blank source values as unavailable evidence; never impute zero.
- Do not interpret -1/0/+1 or -6..+6 beyond the observed serialized values.
- Do not infer timezone from naive timestamps or file boundaries.
- Do not infer missing-value behavior from annual-start clustering.
- Do not use Similarity 57D matrices, scaler/imputer metadata, or standardized features as replacements for these semantic Brain inputs.
- Reuse the existing strict `mtf_brain_input_join_v1.py` adapter after its source contracts are proven.
- Keep PR #133 as a reference lineage validator until a real producer schema is recovered.
- Do not open Stage C producer implementation from guessed formulas.
- Do not modify Murphy, Nison, TIZ, Similarity semantics, Risk, Decision Runtime, or 2025 OOS data.

## Exit criteria

This audit is complete as a forensic classification, not as feature recovery. The MTF producer remains blocked. The next implementation task is evidence acquisition for the missing producer specification/source. If no authoritative source can be recovered, request the original producer project/notebook/script or a signed-off formula specification from the project owner; do not fabricate a replacement under the label "recovered".

## Governance

- `main` untouched.
- No PR merged.
- No feature formulas implemented.
- No source data modified.
- No 2025 OOS data used.
- No backtest profitability claim or trading authorization.
- No live order execution.


## Addendum — historical lineage reconciliation (2026-11-19)

A further GitHub-only review located the earlier repository audit:
`AUDITS/MTF_MARKET_STRUCTURE_SIMILARITY_PRODUCER_LINEAGE_RECOVERY_2026-11-15.md`
on branch `audit/mtf-archive-producer-lineage`. This is important prior evidence and narrows the remaining work.

### What is already recovered and must not be rebuilt

- GBPUSD M1-to-M5/M15/M30/H1/H4/D1 candle aggregation was reconciled against existing output for 2016–2024 with 100% row/OHLC matching in the prior audit.
- The documented aggregation contract tested there is open=first, high=max, low=min, close=last, volume=sum, with M1 counts and volume-availability flags checked.
- This is candle aggregation lineage only. It does **not** establish the Market Structure feature formulas or the six-timeframe MTF regime/score producer.
- Existing five-symbol Market Structure and MTF Alignment output archives were recorded by the prior audit. Their output existence does not imply that their original executable feature builder was recovered.
- MTF Architecture V2 is a reader plan/specification, not the producer for the existing six-timeframe trend regimes/score.
- Similarity V2 (57D), Similarity V3 (71 features), Feature Engineering V2 (22 descriptive features), and Regime Engine V2 diagnostic scores are separate lineages. None is authorized as a replacement for the seven semantic MTF Brain inputs.

### Current code-level compatibility confirmation

The current PR #134 head was inspected directly (not inferred from the older audit branch):

1. `BACKTEST/DEV_BACKTEST_RUNNER_V1.py` still:
   - parses all timestamps using `pd.to_datetime(..., utc=True)`;
   - initializes all seven MTF Brain fields to `0.0`;
   - maps legacy `trend` / `h4_trend` labels instead of direct canonical seven-field mapping;
   - reads `atr` from the MTF row even though the audited canonical 106-column schema does not contain `atr`.
   This runner is **not authorized for a performance evaluation** until these issues and its upstream source contracts are repaired.

2. `BACKTEST/mtf_source_contract_gate_v1.py` also uses `utc=True` on source timestamps. It therefore cannot be treated as authoritative timezone-provenance validation for naive inputs.

3. The current `RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py` has a stricter timestamp parser that rejects naive timestamps and requires explicit timezone-aware values. This is the safer boundary, but it cannot make the source timestamps trustworthy by itself.

4. PR #133's producer-to-feature hash contract validates declared payload lineage; it does not recover or define the missing feature formulas.

### Corrected work breakdown

| Layer | Evidence/status | Decision |
|---|---|---|
| Raw M1 to six OHLCV timeframe candles (GBPUSD, 2016–2024) | Prior reconciliation reported 100% match | Closed; preserve, do not rebuild |
| Market Structure feature producer (per-TF regimes, pivots, breaks, candle features) | Original executable producer not recovered | Blocked |
| Six-TF MTF alignment/score producer | Serialized archive exists; exact producer and score semantics not recovered | Blocked |
| MTF timestamp provenance | Serialized timestamps are naive; authoritative clock policy unresolved | Blocked |
| Strict as-of join | Existing adapter rejects naive timestamps and missing fields | Reuse only after source contracts are proven |
| Similarity feature pipeline | Separate 57D/71D lineages; raw builder unresolved | Do not substitute for MTF |

### Immediate next engineering gate

The next valid implementation is **not** a replacement trend formula. It is a runner-safety remediation isolated from producer recovery:

- prohibit silent UTC localization of naive timestamps;
- preserve missing MTF fields as unavailable and return `NOT_EVALUABLE` / abstain rather than zero;
- stop consuming legacy `trend` / `h4_trend` aliases as if they were the canonical seven fields;
- remove the unsupported assumption that `atr` is present in the MTF archive; source ATR from its own independently verified contract or leave risk sizing not evaluable;
- require the strict clock-provenance gate before any MTF as-of join;
- add regression tests proving each failure mode remains fail-closed.

This remediation must not alter Decision Brain formulas or generate substitute MTF values. It is a separate safety patch and should be reviewed before any diagnostic backtest is rerun.

### Governance correction

The statement “candle producer not recovered” must be scoped precisely: the GBPUSD raw candle aggregation output is already reconciled for 2016–2024. The missing producer is the downstream Market Structure / MTF feature and score computation. 2025 remains locked and unused; no live trading or profitability claim is authorized.
