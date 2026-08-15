# Murphy 0025–0026 — Deterministic Replay V1

Date: 2026-08-15
Status: PASS / HISTORICAL QA CONTINUES

## Scope
Independent replay against the extracted Four-Week Lookback H1 artifact and weekly reference for 2016–2024.

## Results
- H1 rows: 55,192
- Rows with Four-Week reference: 54,825
- 0025 row-level PASS: 6,024
- 0026 row-level PASS: 5,718
- 2025 rows used: 0
- Deterministic checks: 5/5 PASS

## Exact operators
- 0025: current high >= preceding four completed ISO weeks high → bullish evidence.
- 0026: current low <= preceding four completed ISO weeks low → bearish evidence.
- No fixed-bar substitution.
- Current ISO week is excluded from the Four-Week reference.

## Important finding
The precomputed H1 boolean columns are not treated as the authoritative row-level evaluator output. The evaluator compares current H1 high/low directly with the weekly Four-Week reference. This avoids weekly-event propagation being mistaken for the exact trigger timestamp.

## Next gates
- Rule-specific deterministic test suite in repository CI.
- Full historical evaluator replay and result reconciliation.
- Availability/no-lookahead audit.
- Backup, problems/solutions, and freeze only after all gates pass.
