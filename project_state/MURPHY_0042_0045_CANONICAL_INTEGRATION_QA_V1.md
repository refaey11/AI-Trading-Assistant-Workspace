# MURPHY 0042–0045 — CANONICAL INTEGRATION QA V1
Date: 2026-08-17

## Purpose
Close the remaining integration/portfolio-QA gate for Murphy 0042–0045 without rebuilding the existing adapter.

## Compatibility decision
The existing implementation is already isolated in `risk_engine/murphy_0042_0045_risk_adapter.py` and defines the authoritative adapter boundary for these four portfolio-risk constraints. No second risk implementation is introduced.

The adapter preserves source-derived semantics and explicitly refuses to infer PASS from missing or unknown evidence. Existing evaluator, gate, and boundary tests are reused.

## Integration QA added
New test: `tests/risk_engine/test_murphy_0042_0045_integration.py`

Coverage:
- all four portfolio limits pass at the existing operational boundaries;
- authoritative PASS evidence reaches the canonical gate as `pass` for all four rules;
- a 0042 boundary breach remains a hard `fail`;
- NOT_EVALUABLE and UNKNOWN remain `needs_review` and never become PASS.

No new numeric thresholds, operators, lookbacks, proxies, or trading signals were introduced.

## CI gate
Workflow: `.github/workflows/murphy-0042-0045-risk-tests.yml`

The workflow now executes the evaluator tests, gate-adapter tests, and canonical integration tests together on the existing 0042–0045 runner.

## Governance boundary
These rules remain portfolio-level risk/NO_TRADE constraints, not BUY/SELL generators. Murphy direction and Nison confirmation are unchanged.

2025 remains OOS and is not used for tuning, selection, calibration, optimization, or status decisions.

## Freeze decision
The previously documented implementation, boundary QA, gate-contract QA, and CI evidence are retained. This document closes the previously identified integration/portfolio-QA gap at the repository's canonical risk-adapter boundary.

STATUS: PRODUCTION FREEZE CANDIDATE -> FROZEN / CLOSED after registry update
