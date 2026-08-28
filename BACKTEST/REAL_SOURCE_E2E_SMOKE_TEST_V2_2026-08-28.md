# Real-Source E2E Smoke Test V2 — 2026-08-28

Branch: `backtest-only-2026-08-28`

Purpose: validate the governed source flow before any full 2016–2024 backtest.

Required path:
H1 → Market State → Dynamic MTF → Murphy 34 → Nison 44 → Historical Context Memory → Historical Outcome Memory → Similarity V2 → Context-Aware Retrieval V2 → TIZ process boundary → Risk/Execution boundary → Knowledge/Decision Handoff → Decision Brain V1.

Governance:
- 2016–2024 development scope only.
- 2025 remains OOS-locked.
- Nison is confirmation/contradiction only.
- Historical Context/Outcome Memory, Similarity, and Retrieval are evidence-only.
- TIZ is process-only and may be `NOT_EVALUABLE` when process evidence is absent; it cannot generate direction.
- Risk is a hard gate and requires real upstream execution inputs; no synthetic SL/TP/ATR.
- Decision Brain V1 source/semantics remain unchanged.
- No full backtest is authorized by this smoke-test artifact.

Pass criteria:
1. Every required source is present and timestamp/as-of aligned.
2. No future leakage is observed.
3. Handoff sees the evidence bundle.
4. Memory/Similarity/Retrieval/Nison/TIZ do not generate independent direction.
5. Risk is not hardcoded PASS and remains fail-closed without required execution inputs.
6. Decision Brain V1 is called through the existing boundary without source modification.
7. No 2025 rows enter the development evidence package.

A PASS here is a wiring/integration result only; it is not a profitability result.
