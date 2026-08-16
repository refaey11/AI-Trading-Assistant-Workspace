# MURPHY 0030 — External P&F Compatibility Harness V1

Date: 2026-08-16
Status: HARNESS SPECIFICATION / NOT A PASS
Branch: feature/murphy-hybrid-rule-factory-v1

## Objective

Compatibility-test the discovered external P&F implementation candidate against the already source-locked Murphy 0030 semantics before integration. This harness must not choose a box-size policy and must not use historical profitability to select implementation parameters.

## Source-locked semantics under test

- P&F 3-box reversal method.
- High/Low construction path.
- 45-degree bullish support line for the 3-box chart.
- Bullish context while price remains above the bullish support line.
- P&F trendline is structural context; it is not itself a trading signal.

## Candidate implementation

The current project audit identified `pnf-chart-system` / `pypnf` as an external implementation candidate supporting HighLow construction, configurable box size, reversal=3, X/O columns, and bullish-support context.

This harness does NOT assume the candidate is compatible merely because those features exist.

## Compatibility gates

### C1 — Construction semantics
Verify that the candidate's 3-box High/Low construction agrees with the project's source-bounded D1 construction policy for representative synthetic OHLC sequences.

Required evidence:
- column direction;
- continuation behavior;
- 3-box reversal behavior;
- deterministic output;
- no use of future bars.

### C2 — Trendline semantics
Verify that the candidate's bullish-support output corresponds to the source semantics: 45-degree upward support line under the lowest O-column structure.

No alternate slope/tolerance is to be introduced by the harness.

### C3 — Availability / no-lookahead
For each emitted state/event, record the earliest timestamp at which all required OHLC information was available. A later bar mutation must not alter an earlier emitted state when replayed on the earlier prefix.

### C4 — Determinism
Identical input prefix + identical explicit configuration must produce byte-equivalent normalized structural output.

### C5 — Box-size neutrality
The harness accepts an externally supplied box-size policy as configuration. It must never search, optimize, rank, or select box sizes from historical outcomes.

Until governance approves a project box-size policy, production status remains `NOT_EVALUABLE` even if C1–C4 pass.

## Required test fixtures

1. Synthetic X continuation with simultaneous intrabar low movement.
2. Synthetic 3-box reversal from X to O.
3. Synthetic O continuation with simultaneous intrabar high movement.
4. Synthetic 3-box reversal from O to X.
5. Bullish-support line remains below price.
6. Bullish-support breach.
7. Prefix replay invariance.
8. Future-suffix mutation invariance.
9. Missing/invalid configuration returns a fail-closed state.
10. Repeated identical replay produces identical normalized output.

## Acceptance rule

The result is one of:

- `COMPATIBLE_CANDIDATE` — all semantic/availability/determinism checks pass, but production still waits for approved box-size policy and remaining governance gates.
- `INCOMPATIBLE` — one or more source semantics cannot be matched without changing the candidate's behavior or inventing unsupported assumptions.
- `NOT_EVALUABLE` — required input/provenance/policy is missing.

No result may be upgraded to `FROZEN` by this harness.

## Historical boundary

This harness is structural compatibility testing. Historical QA is a separate downstream gate and must use 2016–2024. 2025 is OOS and must not be used for tuning, selection, calibration, or optimization.

## Integration rule

If the candidate passes, create only the smallest project adapter needed to normalize its output into the project's canonical evidence/provenance schema. Do not rebuild the P&F engine.

If it fails, document the smallest incompatible behavior and keep 0030 `NOT_EVALUABLE` or `BLOCKED` as appropriate.
