# MTF Pivot V2 Semantic Oracle — Coverage Review

Date: 2026-11-21

Status: TEST-ONLY COVERAGE AUDIT / NO PRODUCTION AUTHORIZATION

Parent work: PR #141 reference behavior contract; PR #142 semantic oracle.

## 1. Scope

Reviewed the current synthetic oracle and its unit tests against:
`PROJECT_GOVERNANCE/MTF_V2_PIVOT_DETECTOR_REFERENCE_BEHAVIOR_CONTRACT_V1.md`.

This is a source/test review only. No market data was opened. No 2025/2026 data was accessed. No production detector, source identity, timestamp, or L/R configuration was generated.

## 2. Current automated coverage

GitHub Actions on PR #142 head `f29a4f54e7ab88a0a9856d49091ae8a20b2468a4`:
- `synthetic-tests`: PASS, 62 package tests total.
- `histdata-archive-forensics`: PASS, limited to annual 2016-2019 and 2021-2024 archives.
- `smoke`: PASS.

The semantic-oracle test module contains 30 tests. It currently exercises:
- strict isolated HIGH and LOW candidate classification;
- equal HIGH/LOW plateau rejection on both left and right comparison sides;
- same-bar dual HIGH/LOW candidate retention;
- pending left/right context;
- explicit L/R inputs and final-right-bar availability;
- causality under future-bar perturbation;
- gap rejection at the left and right boundaries and within the window;
- explicit continuity-evidence shape;
- trusted-precision boolean gate;
- unfinished bars, malformed OHLC range, boolean OHLC, NaN, and infinity rejection;
- duplicate source-bar IDs inside the evaluated window;
- non-monotonic or duplicate availability tokens;
- integer/type validation for candidate index and L/R;
- deterministic equality for repeated synthetic evaluation;
- six labeled, distinct synthetic cases.

## 3. Contract coverage classification

| Contract area | Current status | Limitation |
| --- | --- | --- |
| Strict extrema and tie policy | Synthetic semantic coverage | Not validated against a production detector |
| Same-bar dual candidates | Synthetic semantic coverage | Intrabar ordering intentionally unresolved |
| Confirmation causality | Partial synthetic coverage | Availability is an integer token, not authenticated time |
| OHLC and completion validation | Partial synthetic coverage | No provider/schema lineage validation |
| Continuity and gaps | Partial synthetic coverage | Caller-supplied booleans are not evidence authentication or a session calendar |
| Six timeframe labels | Matrix coverage only | Oracle has no timeframe parameter/state store; this does not prove production cross-TF isolation |
| L/R configurability | Synthetic API coverage | No numeric production settings selected |
| Source-bar identity | Shape/duplicate checks only | IDs are synthetic strings; no native-ID proof or source namespace |
| Warm-start | BLOCKED / NOT IMPLEMENTED | Requires approved payload, provenance and availability acceptance contract |
| Event lifecycle | OUT OF SCOPE / UNRESOLVED | Expiry, invalidation, supersession, recross and dedup rules not approved |
| Canonical replay bytes and pivot identity | BLOCKED | Config fingerprint and final serialization contract not frozen |
| Property-based testing | NOT IMPLEMENTED | Current tests are fixed deterministic fixtures |
| Production clock/provenance | NOT IMPLEMENTED | No clock authentication or provider lineage |

## 4. Important interpretation

The passing test workflow proves only that the current synthetic oracle and package tests behave as asserted for the included fixtures. It does not prove:
- a production pivot detector exists or is correct;
- six-timeframe runtime isolation;
- upstream source identity, timestamp truth, or session continuity;
- warm-start safety or event lifecycle correctness;
- profitability, market validity, or Decision Brain readiness.

## 5. Required blockers before implementation

1. Approve the exact source-bar event/provenance input schema and source-clock trust boundary.
2. Resolve session/gap evidence and warm-start acceptance policy.
3. Resolve event lifecycle policy separately.
4. Freeze status vocabulary, canonical output serialization, and configuration fingerprint.
5. Approve explicit per-timeframe L/R configuration values without using 2025 for tuning.
6. Add true timeframe-keyed isolation tests and property-based semantic invariants after the above interfaces are fixed.

## 6. Governance

- PR #142 remains Draft and targets PR #141's specification branch.
- No merge, no main-branch modification.
- No production detector or Decision Brain integration.
- No live trading, BUY/SELL, or order execution.
- No 2025/2026 data access, tuning, calibration, feature selection, or performance evaluation.
