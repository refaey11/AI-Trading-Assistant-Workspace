# Murphy 0025–0026 — Full Historical Replay V1

Date: 2026-08-15
Status: FULL HISTORICAL REPLAY PASS / AVAILABILITY PENDING

## Scope
2016–2024 H1 historical artifact using the authoritative weekly Four-Week reference.

## Results
- H1 rows replayed: 55,192
- Rows with four-week reference: 54,825
- 0025 PASS: 6,024
- 0025 FAIL: 48,801
- 0025 NOT_EVALUABLE: 367
- 0026 PASS: 5,718
- 0026 FAIL: 49,107
- 0026 NOT_EVALUABLE: 367
- 2025+ rows in historical scope: 0
- Evaluator invariants: 8/8 PASS

## Operators
0025: current high >= preceding four completed ISO weeks high -> BULLISH on PASS.
0026: current low <= preceding four completed ISO weeks low -> BEARISH on PASS.

Missing reference never produces PASS. The current week is not used to construct its own reference. No fixed-bar substitution is used.

## Remaining gate
Availability / no-lookahead must be independently checked before any freeze decision. This replay does not grant Production Freeze.
