# CI Critical Path Audit — 2026-08-30

## Finding
The repository has two materially different CircleCI configurations:

1. `main` contains a broad legacy CI configuration with many independent workflows, including `nison_development_2016_2024_v1`.
2. `governed-backtest-run-2026-08-29` contains a dedicated governed configuration whose critical path is `build_and_test -> governed_backtest_only -> Governed E2E Gate -> 2016-2024 backtest`.

The failing job seen in recent screenshots, `nison_development_2016_2024_v1`, is a legacy/main workflow. Its `Recover Murphy historical artifact from Dropbox project package` step searches a package for several historical Murphy filenames and exits 1 when no candidate is found. This is not the canonical Governed Gate failure.

## Canonical governed path
The governed branch config contains only:
- `build_and_test`
- `governed_backtest_only`

`governed_backtest_only` runs:
- canonical E2E contract test
- governed smoke preflight
- governed source acquisition
- frozen scope / 2025 lock check
- GOVERNED INTEGRATION GATE V3
- only after the gate, optional 2016–2024 Decision Brain backtest

2025 remains locked/OOS.

## Current known runtime blocker
The latest supplied CI evidence (`build_182_step_106_container_0.txt`) showed:
`NameError: name 'pd' is not defined`
inside `_normalize_regime` in `CIRCLECI_ACQUIRE_GOVERNED_SOURCES.py`.
That was fixed by adding the pandas import.

## Required operating rule
Do not use the legacy `main` Nison/Murphy workflows as the acceptance criterion for the Decision Brain governed path.
Use the dedicated governed branch configuration and evaluate only its governed execution status for Gate 3 / backtest readiness.

## Safety rules
- Do not change Murphy semantics.
- Do not change Nison semantics.
- Do not modify Decision Brain V1.
- Do not modify Memory semantics.
- Do not use 2025 for tuning/calibration/selection.
- Do not run the expensive 2016–2024 backtest until governed integration is proven.
- Do not treat a legacy workflow failure as a governed Gate failure.

## Current project status
The project is intact. The main CI configuration contains legacy noise, while the dedicated governed branch is the intended canonical path for the present Decision Brain integration/backtest work.
