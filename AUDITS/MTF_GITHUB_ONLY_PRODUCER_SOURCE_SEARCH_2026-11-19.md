# MTF GitHub-Only Producer Source Search — 2026-11-19

**Status:** READ-ONLY SOURCE DISCOVERY UPDATE  
**Base evidence:** PR #134 / commit `e3f6d87101ebb464ab17aaba333bc40b6c1ab599`  
**Scope:** GitHub repository branches, Git trees, and GitHub code search only.

## 1. Question

Can the original executable Market Structure / six-timeframe MTF feature producer be recovered from the repository itself, including older branches, without inferring formulas from serialized outputs?

The required producer must explain the six per-timeframe `trend_regime` fields and the exact `mtf_trend_score` semantics, including inputs, thresholds, timeframe close availability, warm-up, missing values, and timestamp lineage.

## 2. GitHub-only search performed

### Branch trees inspected

The following branch heads were inspected through Git refs and recursive Git trees:

- `mtf-producer-search-2026-11-16`
- `audit/mtf-archive-producer-lineage`
- `mtf-source-audit-report-2026-11-16`
- `feature/mtf-producer-v1-contract`
- `feature/mtf-producer-v1-design`
- `audit/mtf-seven-features-forensic-recovery-v1`
- `build/decision-runtime-v1`
- `decision-brain-stable-2026-09-05`
- `canonical-decision-pipeline-v1`
- `feat/mtf-runtime-resolver-v1`
- `fix/mtf-import-clean-2026-08-30`
- `feature/edge-discovery-ledger-v1`
- `feature/mt5-forex-only-capture-v1-1`
- `feature/mt5-raw-capture-v1`
- `bot-v1-integration-2026-09-16`
- `current-stack-dev-backtest-2016-2024-v5-1`

Across the inspected trees, no executable file path matching a Market Structure / trend-regime / pivot / break-of-structure / swing / fractal / six-timeframe MTF feature producer was found. Existing files found by name are readers, source adapters, validators, lineage contracts, timestamp gates, audits, or design documents—not the missing feature producer.

### GitHub code search

Repository-scoped code searches were run for:

- `trend_regime`
- `mtf_trend_score`
- `"market structure"`
- `pivot`

The connected GitHub code-search endpoint returned no indexed results for these queries. This is a negative search result, not proof that no source exists anywhere in the repository's full historical object graph.

## 3. Existing evidence reconciled

The prior read-only audit `AUDITS/MTF_MARKET_STRUCTURE_SIMILARITY_PRODUCER_LINEAGE_RECOVERY_2026-11-15.md` records that:

- GBPUSD M1-to-M5/M15/M30/H1/H4/D1 candle aggregation for 2016–2024 was reconciled against existing outputs at 100% for the audited OHLC/row/volume checks. This layer is closed and must not be rebuilt.
- Five-symbol Market Structure and MTF Alignment output archives exist.
- The original executable downstream Market Structure and six-timeframe MTF feature producer was not present in the inspected archive inventories.
- MTF Architecture V2 is a reader/design specification, not proof of the original six-timeframe producer formulas.
- Similarity 57D, Similarity 71D, Feature Engineering V2, and Regime Engine V2 are distinct feature lineages and are not substitutes for the seven Decision Brain MTF fields.

PR #134 already records the seven fields as UNRESOLVED. This update does not change that status.

## 4. Search boundary and limitation

An older repository workflow named `.github/workflows/mtf-producer-source-search-2026-11-16.yml` downloads a pinned project archive through Dropbox before searching it. That workflow was inspected but was **not executed** as part of this GitHub-only work. No Dropbox connector, Dropbox API, or external file source was used here.

The earlier PR #134 audit records a prior pinned-archive search and its reported result. This update treats that as existing repository evidence, not as a newly reproduced GitHub-only search.

The current search is therefore a bounded repository-branch/code-index search. It is not an exhaustive proof over every historical Git object, every unindexed file, or the original external execution environment.

## 5. Existing safety remediation — no duplicate patch

PR #135 already contains the isolated development-runner fail-closed remediation:

- rejects naive timestamps rather than localizing them to UTC;
- requires the seven canonical MTF fields;
- preserves raw field values rather than recoding legacy aliases;
- returns NOT_EVALUABLE / abstains for missing or invalid MTF inputs rather than substituting zero;
- removes the unsupported assumption that ATR exists in the MTF archive.

PR #135 remains a Draft and is not merged. This search update does not duplicate or alter that code.

PR #136 separately rejects unverified naive timestamps in the six-timeframe raw-source adapter. It remains a Draft and is not merged.

## 6. Decision

**Producer recovery remains BLOCKED. No authoritative feature producer or formula contract was recovered from the GitHub search performed here.**

Do not:
- infer the six regime formulas from observed `-1/0/+1` values;
- infer `mtf_trend_score` from its observed `-6..+6` range or correlations;
- substitute the old H1/H4 research reader, Similarity features, or Regime V2 scores;
- impute missing values or relabel naive timestamps as UTC;
- rebuild the already-reconciled GBPUSD candle aggregation layer.

The correct next source-recovery input is the original project notebook/script or execution workspace that generated the Market Structure and MTF Alignment archives, or a formally approved exact formula specification with deterministic fixtures. Until that evidence is available, keep all seven fields UNRESOLVED / NOT_EVALUABLE and keep downstream performance evaluation blocked.

## 7. Governance

- `main` untouched.
- This branch is audit-only; no runtime or source data changes.
- No feature formulas, thresholds, weights, or encodings invented.
- 2025 remains locked OOS and unused.
- No PR merge, no live trading, and no order execution authorized.
