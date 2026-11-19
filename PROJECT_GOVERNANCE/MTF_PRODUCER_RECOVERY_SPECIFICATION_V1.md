# MTF Producer Recovery Specification V1

**Status:** SPECIFICATION ONLY — NOT AN IMPLEMENTATION  
**Date:** 2026-11-19  
**Base evidence:** PR #137 historical source-search audit and the 2026-08-21/2026-08-29 MTF evidence records  
**Governance:** 2025 remains protected OOS. No source/runtime changes, no inferred formulas, no live execution.

## 1. Purpose

Define the minimum evidence required to recover or faithfully reproduce the original six-timeframe MTF feature producer consumed by the Decision Brain. This document does not authorize implementation, formula selection, data fitting, calibration, or runtime activation.

The existing MTF Alignment artifact is evidenced as a serialized six-timeframe input dataset. Its existence and as-of alignment evidence do not establish the exact algorithms that produced its numeric feature values.

## 2. Architecture boundaries

Keep these distinct:

1. **Full MTF Reader architecture:** W1, D1, H4, H1, M30, M15, M5, with top-down context and explicit timeframe roles.
2. **Six-timeframe alignment/feature layer:** M5, M15, M30, H1, H4, D1.
3. **Decision Brain numeric input contract:** consumes source-backed fields; it must not invent encodings or silently impute missing values.
4. **Dynamic MTF binding:** selects/assigns timeframe roles according to its recovered contract; it is not itself proof of the feature calculations.
5. **Similarity/Memory:** historical evidence only; never the sole decision maker.

Murphy supplies technical context/market structure. Nison supplies candlestick confirmation only. Trading in the Zone is a psychology/process gate only and cannot generate direction. Risk remains a hard gate.

## 3. Seven canonical fields under recovery

The following seven fields remain **UNRESOLVED / NOT_EVALUABLE** for numeric producer semantics until the evidence requirements in this specification are met:

- `M5_trend_regime`
- `M15_trend_regime`
- `M30_trend_regime`
- `H1_trend_regime`
- `H4_trend_regime`
- `D1_trend_regime`
- `mtf_trend_score`

Observed serialized values (including categorical values such as -1/0/+1 and score ranges) are observations only. They do not establish the formula, thresholds, lookback, aggregation, warm-up, or missing-data behavior.

The broader archived schema also exposes structure/pivot/BOS, distance, candlestick/context, and aggregate count fields. Their presence in a CSV schema is not proof that their producer semantics are recovered.

## 4. Evidence required before producer implementation

### 4.1 Authoritative source and version
- Recover the original executable producer source, or a formally approved complete algorithm specification.
- Record repository/path, immutable commit or artifact revision, source hash, producer version, dependencies, and execution environment.
- Establish that the recovered producer generated the exact archived dataset family being used as the reference.
- Do not substitute reader adapters, as-of joiners, schema normalizers, Similarity feature builders, XAUUSD-only pivot prototypes, or downstream consumers for the original producer.

### 4.2 Raw input contract
For every timeframe, specify:
- symbol identity and canonical symbol mapping;
- raw OHLCV field names, numeric precision, and volume type/availability semantics;
- candle open/close timestamp convention and timezone provenance;
- source broker/feed and immutable input snapshot identity;
- handling of gaps, duplicates, out-of-order bars, and incomplete candles.

### 4.3 Per-field calculation semantics
For each of the seven fields, provide:
- exact formula or deterministic algorithm;
- all parameters, thresholds, lookbacks, tie-breaking rules, and boundary conditions;
- required warm-up length and first valid output rule;
- null/NaN/missing-input behavior;
- whether the value is categorical, ordinal, or continuous, and its documented domain;
- deterministic behavior across repeated runs.

For `mtf_trend_score`, explicitly document its aggregation inputs, weighting, normalization, handling of unavailable timeframes, and whether it is computed from the six regime fields or from another independent evidence set. Do not infer that it is a sum, average, or vote count from observed ranges.

### 4.4 Time and causality
- Define whether each feature is calculated only from completed source candles.
- Define exact as-of join semantics for each target M5 observation.
- Prove that higher-timeframe features become available only after the source candle close.
- Preserve timestamp offsets and broker-server clock provenance; normalize to UTC only under an evidenced mapping.
- No naive timestamps, guessed timezone offsets, or DST inference.
- Tests must include boundary timestamps around HTF close, missing bars, duplicate bars, and future-bar injection.

### 4.5 Golden fixtures and reproducibility
- Obtain a small, immutable set of original raw inputs and corresponding original producer outputs from the same producer version.
- Include normal, boundary, warm-up, missing-data, gap, and contradictory-timeframe cases.
- Store fixture hashes and provenance.
- Require exact categorical matches and documented numeric tolerances for continuous outputs.
- A fixture created by a new implementation is not an authoritative golden fixture.
- Reproduce archived outputs on permitted development data without tuning to protected OOS data.

### 4.6 Missingness and warm-up
- Explain the observed early-file blanks per timeframe and field.
- Distinguish warm-up, source gaps, unavailable inputs, and producer errors.
- Never replace missing MTF values with zero, neutral, or a fabricated direction.
- Until semantics are established, affected rows must remain NOT_EVALUABLE and fail closed.

## 5. Validation gates

| Gate | Required proof | Failure result |
|---|---|---|
| P0 — Source identity | Immutable original source or approved complete algorithm spec | BLOCKED |
| P1 — Input provenance | Raw OHLCV, symbol, time and volume lineage | BLOCKED |
| P2 — Formula semantics | All seven field algorithms and missing/warm-up rules | NOT_EVALUABLE |
| P3 — Golden parity | Reproducible parity against original fixtures | BLOCKED |
| P4 — Causality | Completed-bar/as-of/no-future-leak tests | BLOCKED |
| P5 — Integration compatibility | Exact field mapping into existing Brain contract, no defaults | BLOCKED |
| P6 — Governed E2E | Timestamped canonical event through existing Brain, TIZ boundary and Risk path | NOT PASSED |

A schema check, alignment pass, reader pass, adapter pass, or successful unit test of an adapter cannot independently close P0–P6.

## 6. Explicit exclusions

- No new trend-regime formula or score formula is proposed here.
- No numeric encoding is inferred from observed output values.
- No zero-imputation or neutral fallback is permitted.
- No ATR-in-MTF assumption is permitted without source evidence.
- No change to Decision Brain direction logic is authorized.
- No BUY/SELL generation, order placement, or live trading is authorized.
- No 2025 data may be used for training, tuning, calibration, thresholds, feature selection, or iterative fitting.
- Do not rebuild the already-audited candle aggregation or existing MTF architecture from scratch.

## 7. Current evidence interpretation

The historical evidence establishes that:
- an MTF Alignment GBPUSD artifact family exists with M5/M15/M30/H1/H4/D1 schema and serialized trend/structure/context fields;
- source metadata describes higher-timeframe joins after source candle close;
- the complete MTF Reader architecture separately includes W1;
- Dynamic MTF binding and selection contract artifacts were recovered in the reconstructed workspace evidence;
- runtime alignment evidence and numeric producer semantics are separate gates.

The GitHub-only source search recorded in PR #137 did not recover the original executable numeric producer or authoritative formula semantics. References in old audit records to a recovered dataset or a closed alignment gate must not be reinterpreted as proof of recovered producer code.

## 8. Approval required to proceed

Implementation may begin only after an authorized source/algorithm and its provenance are identified, compatibility-audited against the existing Brain contract, and golden fixtures are available. Any implementation proposal must be isolated on a feature branch and remain Draft until explicit user approval. No changes to `main` or merges are part of this specification.


## 9. Expanded Decision Brain input scope and Similarity V2 recovery route

A further historical compatibility audit was inspected after this specification was drafted. It clarifies that the seven fields above are only the unresolved six-TF trend/score subset, not the complete Decision Brain market-input contract.

The recovered `DECISION_BRAIN_V1_SPEC.json` declares these additional inputs:

- MTF context: `mtf_bullish_count`, `mtf_bearish_count`, `mtf_neutral_count`, `mtf_context_code` in addition to `mtf_trend_score`.
- Volatility: `M5_volatility_regime`, `M15_volatility_regime`, `M30_volatility_regime`, `H1_volatility_regime`, `H4_volatility_regime`, `D1_volatility_regime`.
- Volume: `*_relative_volume_20` and `*_volume_regime`, conditionally active only when `volume_available=true`; unavailable volume is not zero.
- Historical memory: Similarity V2 is evidence only, not a directional source.

Accordingly, P5 compatibility must audit the complete actual input contract and not close on the seven trend/score fields alone. Each additional field requires its own authoritative producer lineage, semantics, availability, and timestamp proof. No field may be synthesized merely because it is named in the Brain specification.

### Similarity V2 is a separate recovery lead, not an assumed MTF producer

The 2026-08-29 MTF-to-Brain compatibility record explicitly directs recovery of the exact producer or serialized feature matrix used for the Similarity V2 57D representation, including:
- exact feature order and schema/version;
- current/query vector producer lineage;
- raw-to-feature mapping;
- missing-value handling, imputation and scaling;
- source timestamps and as-of lineage;
- proof whether any of those 57 dimensions map to the Decision Brain's required fields.

The GitHub branch inspected contains the Similarity V2 evidence-only boundary and compatibility audit, but does not contain the named historical run JSON artifacts or the original Similarity V2 archive/feature-matrix producer. The boundary preserves top_k=20 and blocks 2025/future retrieval; it is not a vector producer and cannot prove current-query feature generation.

Do not assume the 57D vector is identical to the Brain input contract, or that any dimension can be renamed into a trend-regime field without exact mapping evidence. Similarity remains historical memory only and must never influence direction through a predicted-return shortcut.

### Additional integration constraints recovered

The historical Decision Brain compatibility audit also records that the existing Brain implementation does not itself provide complete volatility, knowledge, Nison, TIZ, and Risk integration. The correct approach remains a narrow compatibility boundary around existing components, not rebuilding them. Nison is confirmation/contradiction only; TIZ is process-only and cannot generate direction; Risk remains a hard gate; missing authoritative evidence must remain NOT_EVALUABLE.

The full MTF Reader architecture includes W1, but W1 is not part of the six-TF serialized alignment vector. Preserve that distinction in all mappings and tests.


## 10. Expanded historical lineage recovery findings (2026-11-15 / 2026-11-16)

A read-only lineage audit on the historical `audit/mtf-archive-producer-lineage` branch and the `mtf-source-audit-report-2026-11-16` branch adds the following source-backed corrections and boundaries.

### 10.1 Candle aggregation is already closed for GBPUSD 2016–2024

The raw GBPUSD M1 master was reconciled against the existing `MULTI_TF_MARKET_DATA_V1.zip` output for M5, M15, M30, H1, H4, and D1. The audit records 100% agreement for OHLC, M1 row counts, volume-availability flags, and available-volume sums, with no missing or extra output bars. Do not rebuild this conversion.

### 10.2 Existing output archives are not producer source

The historical audit records separate Market Structure and MTF Alignment output archives for EURUSD, GBPUSD, USDJPY, USDCAD, and XAUUSD. It explicitly states that the executable feature-producer source was not present in the recovered archive inventory.

The MTF Architecture V2 files (`MTF_READER_SPEC_V2.json`, `READER_LOGIC.md`, `DATA_REQUIREMENTS.md`, `NEXT_STEP.md`) describe a seven-timeframe reader and intended roles/features. They are architecture/specification material, not executable proof of the existing six-timeframe numeric producer or its formulas.

### 10.3 Existing adapters are consumers/validators, not producers

The audited components have distinct non-generative responsibilities:
- `MTF_SIX_TF_SOURCE_ADAPTER_V1.py`: validates/loads existing MTF files.
- `mtf_brain_input_join_v1.py`: performs strict point-in-time/as-of joining of already-produced fields.
- Dynamic MTF binding/resolver: validates/selects explicit timeframe roles.
- Market pipeline evidence adapter: normalizes existing outputs into governed evidence.
- Similarity V2 boundary: enforces evidence-only retrieval policy.

None of these is evidence of the missing Market Structure feature producer or the six-TF `mtf_trend_score` producer. Reuse them only within their existing contracts; do not relabel them as producers.

### 10.4 Similarity 57D is explicitly separate from Decision Brain semantic MTF fields

The 2026-11-15 lineage audit states that Similarity V2's standardized 57D candidate/index representation has a distinct feature lineage. It records a feature order and persisted scaler/imputer metadata in a separate historical audit, but the exact raw/current-query vector producer lineage remains open.

Therefore:
- The 57D standardized matrix is not the six-TF Brain input vector.
- Do not inject standardized Similarity dimensions into Brain fields.
- Do not rename any of the 57 dimensions into `*_trend_regime`, `mtf_trend_score`, volatility, or volume fields without exact raw-field mapping and producer proof.
- The Similarity current/query raw-vector builder and its full preprocessing lineage remain a separate recovery task.
- Similarity V3's 71-feature schema and referenced `v3_shared_builder.py` are also separate; the builder was not located in the audited inventories.
- Feature Engineering V2's 22 descriptive/memory features and Regime Engine V2's diagnostic scores are not substitutes for the six-TF MTF producer.

### 10.5 Serialized MTF artifact has unresolved timestamp and missingness contracts

The 2026-11-16 source compatibility audit records:
- 671,601 rows across 2016–2024, nine annual files, 106 columns with identical headers.
- All serialized timestamps are naive; source README does not define timezone, broker/server clock, DST, or epoch interpretation.
- Observed regime values `-1, 0, 1` and `mtf_trend_score` range `-6..+6`; these observations do not prove encoding or formula.
- 2,512 blank cells across the seven Brain trend/score fields. The audit counts 26 M15, 53 M30, 107 H1, 371 H4, and 1,955 D1 blanks. The repeated annual-start pattern is consistent with HTF warm-up, but remains unproven without producer semantics.
- The archive itself contains no `.py`, `.ipynb`, or `.sql` producer files.
- A separate full-project archive search found the older H4/H1 research-only reader and MTF Architecture V2 docs, but no six-timeframe producer-code candidate in the inspected top-level source/documentation scope. Nested legacy ZIP contents were not recursively unpacked in that pass.

These findings reinforce P1/P2/P4 blockers. No naive timestamp may be treated as UTC, no warm-up assumption may be promoted to fact, and no blank may be replaced with zero/neutral.

### 10.6 Runner compatibility must be re-audited against the active branch

The 2026-11-16 historical audit identified defects in the runner version it inspected: naive timestamps coerced to UTC, MTF fields defaulted to zero, legacy trend-token mapping, failure to copy canonical MTF fields directly, and an unsupported ATR lookup from the MTF schema. The strict as-of join adapter is safer but cannot pass this source while timestamp provenance and missingness remain unresolved.

Before any future runner wiring, compare the exact active branch/commit with these findings and prove the defects are absent. Do not assume a historical runner finding describes the current head, and do not bypass the strict join adapter.

## 11. Reconciled recovery status after the expanded search

**Recovered / confirmed**
- GBPUSD M1-to-six-timeframe candle aggregation output for 2016–2024 is reconciled; do not rebuild it.
- Five-symbol Market Structure and MTF Alignment serialized output archives are recorded as existing.
- MTF Architecture V2 and Dynamic MTF binding contracts are specification/architecture sources.
- Strict source adapter, as-of join, role resolver, and Similarity evidence boundary exist as separate non-generative components.

**Not recovered / still blocked**
- Executable Market Structure feature producer (including trend/pivot/BOS/candle features).
- Executable six-timeframe alignment numeric producer and exact `mtf_trend_score` formula.
- Authoritative timezone/broker-clock mapping for naive MTF timestamps.
- Proven warm-up/missing-value semantics for the 2,512 blank Brain-field cells.
- Exact raw/current-query Similarity V2 57D vector producer, despite the separately documented feature order and scaler/imputer metadata.
- Similarity V3 shared builder source.

**Next safe action**
Recover the original producer from the source execution environment that generated the serialized archives, or recover the exact pre-standardized feature matrix together with its authoritative manifest, raw-field mapping, imputer/scaler artifacts, and golden fixtures. Do not reverse-engineer approximate formulas from output columns, substitute Regime V2 or Similarity dimensions, or rebuild the existing candle aggregation.

Until source provenance and semantics are proven, affected Brain inputs remain `NOT_EVALUABLE`; full canonical backtest/E2E cannot be declared ready from schema, archive identity, alignment, or adapter tests alone.


## 12. GitHub Actions archive-search artifact verification (2026-11-19)

The GitHub Actions run `43798060902` and its retained artifact `14194444128` were fetched from GitHub and inspected read-only.

Artifact facts:
- Workflow conclusion: SUCCESS.
- Exact full-project archive identity recorded in the artifact: 134,687,505 bytes; SHA-256 `f3f2b2452970a9a2afc13943a70f6c319bb0d14dc5cbd37a24d1cb184556ae26`.
- ZIP entries inventoried: 67.
- Producer-code candidates: ZERO.
- Unread text candidates: ZERO.
- Search scope: source-code/documentation text only; no CSV/Parquet/HDF5/Feather/XLSX market data rows were read; 2025 was not read or used.
- The inventory includes the nested `AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1.zip` and MTF Architecture V2 documentation. The nested reader ZIP was inventoried by name but was not recursively unpacked by this search.

Interpretation: this successful workflow proves only that the bounded archive text search completed and found no producer candidate in its declared scope. It does not prove that every nested archive or the original producer execution environment was exhaustively inspected. The nested reader remains a separately documented H4/H1 research-only component, not the six-timeframe producer.

The Gate A artifact `14195058191` was also fetched from GitHub. Its machine-readable preflight confirms:
- MTF: 671,601 rows; all 671,601 timestamps naive; 2,512 invalid/blank values across required trend/score fields; status BLOCKED.
- Murphy: 87,225 rows; 32,400 naive timestamps; status BLOCKED.
- H1, Market State, Historical Context, Historical Outcome, and Nison passed their respective source input preflight checks.
- The full governed backtest authorization flag is false; 2025 remains locked and unused.

These artifacts reinforce that successful archive search and successful annual-file assembly are not source-producer approval, and that the current MTF-to-Brain input path remains blocked by unresolved provenance/missingness.

## 13. GitHub-only search boundary and archive-search coverage limitation (2026-11-19)

A further read-only inspection of the historical mtf-producer-search-2026-11-16 branch identified an important limitation in the prior archive-search workflow.

### 13.1 Historical workflow dependency

The workflow .github/workflows/mtf-producer-source-search-2026-11-16.yml downloads /AI_Trading_Assistant_FULL_PROJECT_V1.zip using a DROPBOX_ACCESS_TOKEN GitHub Actions secret before running the source-search script. Its historical run 43798060902 completed successfully, and the job log metadata confirms the Dropbox download step ran successfully.

This is historical provenance only. The current recovery work is constrained to GitHub repository content and GitHub Actions metadata already available in GitHub. Do not rerun this workflow, request/use Dropbox credentials, or retrieve the original archive through Dropbox as part of the GitHub-only recovery path.

### 13.2 Search implementation coverage

The checked-in BACKTEST/MTF_PRODUCER_SOURCE_ARCHIVE_SEARCH_V1.py:
- inventories ZIP entries and searches eligible text/code files;
- does not recursively open nested ZIP archives;
- does not inspect non-text binary members as producer source;
- skips eligible text files larger than its 2 MiB limit and records them as unread candidates;
- reports source-code candidates based on lexical term matches only, not producer authority.

Therefore, the prior zero-candidate result is bounded to the files actually inspected. It is not an exhaustive proof that every nested archive or binary payload lacks source code. The nested AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1.zip was inventoried by name but not recursively inspected by that workflow.

### 13.3 GitHub-only follow-up scope

Continue with GitHub-hosted evidence only:
1. inspect repository trees and commits for tracked archive objects, manifests, source snapshots, notebooks, and producer-related code across relevant historical branches;
2. inspect any GitHub-hosted nested archive only if it is actually present as a repository object and can be accessed through GitHub;
3. inspect existing GitHub Actions logs/artifacts as historical evidence, while clearly preserving their recorded source provenance;
4. keep Similarity 57D current/query vector lineage separate from MTF numeric producer recovery.

If the required archive/source exists only in Dropbox or an unavailable external execution environment, record that as an external source dependency and stop. Do not silently cross the GitHub-only boundary.

### 13.4 Current conclusion

The original six-timeframe MTF numeric producer remains NOT RECOVERED. The previous successful archive-search workflow is not a basis for closing the search because it used an external Dropbox download and did not recursively inspect nested ZIP contents. No formula reconstruction, replacement producer, imputation, or runtime change is authorized by this finding.
