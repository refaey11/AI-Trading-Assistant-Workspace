# Murphy Freeze Candidates 0021–0023 / 0028–0029 — QA Gate V1

Date: 2026-08-12

## Evidence reviewed

### 0021–0023
Existing contract: `MURPHY_0021_0023_EVALUATOR_V1`
Status: `IMPLEMENTED_AND_UNIT_TESTED`.

Operationalization:
- price rising/falling = current completed close vs previous completed close;
- volume rising = existing `volume_direction == UP`;
- OI rising = existing CFTC futures `oi_direction == UP`;
- no thresholds added;
- no proxy OI;
- runtime/Dynamic MTF timeframe accepted by evaluator;
- 2025_used=false.

Unit tests preserved:
- 0021 bullish, bearish, no confirmation = pass;
- 0022 pass, wrong OI, missing OI = pass;
- 0023 pass, wrong price = pass.

Historical artifacts preserved:
- `MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`
- `MURPHY_0021_0023_HISTORICAL_SUMMARY_V1.csv`

### 0028–0029
Existing evaluator contract: `MURPHY_0027_0029_EVALUATOR_V1`.
Status: `0028_0029_IMPLEMENTED; 0027_BLOCKED_PENDING_EXACT_REGIME_OPERATOR`.

0028:
- PASS only on confirmed BEARISH divergence at HIGH pivot.

0029:
- PASS only on confirmed BULLISH divergence at LOW pivot.

Evidence alignment:
- existing Pivot Sequence V2;
- existing RSI-14;
- existing confirmed divergence artifacts;
- availability timestamp is used for no-lookahead alignment;
- 2025_used=false.

Unit tests preserved for 0028 and 0029:
- correct divergence;
- wrong divergence;
- missing evidence.
All recorded pass=true.

## Freeze decision

These four rules are **FREEZE CANDIDATES / QA-PASS ARTIFACTS**, but this artifact does not falsely promote them to Production Frozen. The project handoff explicitly states that evaluator-file existence is not semantic freeze and that the final freeze requires the full rule evidence chain.

### Remaining gate before official freeze

1. Verify exact source semantics against the authoritative Murphy source rows.
2. Verify Rule Adapter compatibility without changing evaluator semantics.
3. Confirm historical QA/provenance is accepted under the official freeze gate.
4. Record the rules in the official Murphy freeze manifest.

No new threshold, proxy, timeframe, or evaluator logic is introduced here.

## Exclusions

- 0027 remains BLOCKED pending exact trend-vs-range operator.
- 0003–0004 remain NOT FROZEN due provenance/semantic reconciliation.
- 0006–0007 remain pending source-lock/operational reaction evidence.

## OOS control

2025 remains untouched and is not used for tuning or implementation selection.
