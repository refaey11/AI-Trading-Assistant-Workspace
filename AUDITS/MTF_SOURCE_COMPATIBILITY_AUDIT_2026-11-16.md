# MTF Source Compatibility Audit — 2026-11-16

## Status

**SOURCE ARTIFACT CONFIRMED / PRODUCER FORMULA AND TIMEZONE CONTRACT UNRESOLVED / BRAIN INPUT BLOCKED**

This is a read-only audit. No source rows, runtime logic, Decision Brain, risk settings, or OOS data were modified.

## Exact source evidence

### Canonical MTF artifact

- Dropbox path: `/MTF_ALIGNMENT_GBPUSD_V1.zip`
- Pinned revision: `01659665ff5a6d300000003796dcfe3`
- Size: `80,293,251` bytes
- Downloaded SHA256 in Gate A: `f2149e7d3051ea0c5b205a82ae9e187b2eac292bafbac1cd2db512f0e902ed53`
- Gate A source acquisition and hash verification: [run 43797854505](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43797854505)
- MTF read-only forensics artifact: [artifact 14195058191](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43797854505/artifacts/14195058191)

The archive contains the nine development-year files 2016–2024. They contain 671,601 rows in total, each annual file has 106 columns, and the annual headers are identical.

The source README declares:
- asset: GBPUSD;
- base timeframe: M5;
- aligned timeframes: M5, M15, M30, H1, H4, D1;
- higher-timeframe features are joined only after the source candle closes;
- purpose is market intelligence/market reading, not a strategy or indicator.

These README statements establish the declared architecture, not independent proof of the producer implementation or timestamp semantics.

### Producer search

The MTF archive itself contains no `.py`, `.ipynb`, or `.sql` producer files.

A second read-only search was run against the exact Dropbox full-project archive:
- path: `/AI_Trading_Assistant_FULL_PROJECT_V1.zip`
- pinned revision: `0165966394fea0c00000003796dcfe3`
- size: `134,687,505` bytes
- SHA256: `f3f2b2452970a9a2afc13943a70f6c319bb0d14dc5cbd37a24d1cb184556ae26`
- search run: [run 43798060902](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43798060902)
- report artifact: [artifact 14194444128](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43798060902/artifacts/14194444128)

That archive contains the older `MULTI_TIMEFRAME_READER_V1` package and MTF Architecture V2 documentation, but the search found no six-timeframe producer-code candidate. The older reader is separately documented as a research-only H4/H1 component and is not an authority for the six-timeframe artifact.

The search did not read CSV/HDF5/Parquet market rows and did not read or use 2025 data.

## Actual serialized data profile (2016–2024 only)

- Every timestamp in the 671,601 MTF rows is naive (no UTC offset/timezone).
- The archive README does not define the timezone, broker/server clock, DST policy, or epoch interpretation.
- The observed `trend_regime` values are `-1, 0, 1`.
- The observed `mtf_trend_score` values range from `-6` to `+6`.
- These are observed serialized values only. The producer formula and semantic encoding have not been recovered.

### Missing values

The full 2016–2024 scan found 2,512 blank cells across the seven Decision Brain input fields:

| Field | Blank cells |
|---|---:|
| M15_trend_regime | 26 |
| M30_trend_regime | 53 |
| H1_trend_regime | 107 |
| H4_trend_regime | 371 |
| D1_trend_regime | 1,955 |
| **Total** | **2,512** |

The blanks cluster at the beginnings of annual files. In 2020–2024, the per-year pattern is 3 M15, 6 M30, 12 H1, 48 H4, and 288 D1 blanks. This is consistent with a higher-timeframe warm-up boundary, but that interpretation is **not yet proven by producer code**.

No values were imputed, recoded, scaled, or rewritten. 2025 was not read; 2026 was not read.

## Runtime compatibility defects confirmed

The current `BACKTEST/DEV_BACKTEST_RUNNER_V1.py` does not faithfully consume this source contract:

1. Its shared `read_csv` applies `pd.to_datetime(..., utc=True)`, which silently treats naive source timestamps as UTC.
2. `build_row` initializes the seven MTF Brain inputs to `0.0`, which turns missing source evidence into neutral-looking values.
3. It looks for legacy `trend` and `h4_trend` fields and maps string tokens through a local `trend_map`; the canonical artifact instead has `M5_trend_regime`, `M15_trend_regime`, `M30_trend_regime`, `H1_trend_regime`, `H4_trend_regime`, `D1_trend_regime`, and `mtf_trend_score`.
4. The current `build_row` path does not directly copy the canonical MTF fields from the MTF row into the Brain input row.
5. The inspected 106-column MTF schema does not include an `atr` field, while the runner attempts to read `atr` from the MTF row.

The strict `RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py` adapter rejects naive timestamps and missing required numeric fields, which is safer, but it cannot pass the current source until the timezone and missing-value contracts are resolved.

## Required decisions before implementation

1. Recover authoritative timestamp provenance for the MTF archive and the other sources it must join to. Do not infer UTC from naive values or infer timezone from file boundaries.
2. Recover the producer schema/formula, especially the meaning of `-1/0/1`, the `-6..+6` aggregate score, and the missing-value policy.
3. Confirm whether annual-start blanks are expected warm-up gaps. If confirmed, preserve them as unavailable evidence and make affected events `NOT_EVALUABLE`/abstain, unless an already-governed prior-period as-of source is proven. Do not fill them with zero.
4. After the contract is proven, adapt the runner by direct field selection/rename only. No new encoding, imputation, scaling, or directional logic.
5. Re-run Gate A against the exact pinned sources. Only after Gate A passes and the remaining independent gates are reconciled may the project consider the next validation stage.

## Gate A result

The real Dropbox-backed Gate A run [43797854505](https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43797854505) completed source acquisition successfully and all deterministic unit tests passed. The input preflight remains **BLOCKED** on:
- MTF: 671,601 naive timestamps and 2,512 blank numeric values;
- Murphy: 32,400 naive timestamps of 87,225 rows.

H1, Nison, Market State, Historical Context, and Historical Outcome passed the input-shape/window preflight. This is not a full backtest authorization.

## Governance

- 2025 remains locked OOS and was not used.
- No Decision Brain V1 changes.
- No Murphy/Nison semantic changes.
- No Risk Engine changes.
- No auto BUY/SELL enablement.
- No full backtest or profitability claim.
- No PR merge authorized by this audit.


### Search-scope caveat

The full-project archive search inspected top-level source/documentation files and inventoried nested ZIP names; it did not recursively unpack the nested legacy reader ZIP. The repository's existing provenance blocker and reader audit identify that legacy reader as H4/H1-only and research-only. It is not evidence for the six-timeframe M5/M15/M30/H1/H4/D1 producer. The canonical MTF archive itself was directly inspected across all 2016-2024 annual data files and contained no producer code files.


## Cross-check against existing MTF lineage records

Two existing Dropbox records were also inspected:

- `MTF_57D_DEEP_LINEAGE_FINDINGS_2026-08-29.md` explicitly says raw producer lineage remains open. It distinguishes the Similarity V2 standardized 57D candidate/index matrix from the Decision Brain's semantic numeric MTF inputs. The 57D matrix, its scaler/imputer metadata, and its feature order must not be injected into the Brain as a substitute for the raw MTF fields.
- `MTF_BRAIN_INPUT_JOIN_EXECUTION_CHECKPOINT_2026-08-29.md` records the existing strict non-directional join adapter and its tests. The adapter uses backward `merge_asof`, rejects missing/duplicate/future-only inputs, and does not generate direction or risk. Its historical "MTF source provenance PASS/CLOSED" is now scoped to artifact identity and declared six-timeframe structure; it does not resolve the newly measured naive timestamp provenance or annual-start blanks.

The repository already contains `RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py`. The correct engineering path is to reuse and validate this existing strict adapter after source contracts are proven, not create a new MTF scoring layer or rebuild the 57D similarity matrix.
