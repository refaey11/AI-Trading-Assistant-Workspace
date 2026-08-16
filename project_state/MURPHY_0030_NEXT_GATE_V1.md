# Murphy 0030 — Next Gate V1

## Current gate
Compatibility/operator closure before historical QA.

## Evidence currently available
- P&F implementation tests exist for High/Low construction, reversal behavior, bullish support reference, stop reference, deterministic replay, and prefix no-lookahead behavior.
- The 39-rule queue and hybrid factory manifest are integrity-valid.

## Explicitly unresolved
- Source-faithful box-size policy.
- Semantic equivalence of the selected P&F construction to the canonical Murphy contract.
- External pypnf candidate remains compatibility evidence only; it is not certification.

## Prohibited shortcuts
- No ATR/%/pip box-size import unless separately source-bounded and approved.
- No historical optimization/tuning of box size.
- No 2025 data.
- No rule freeze from implementation tests alone.

## Gate order
1. Verify implementation behavior against canonical Murphy semantics C1-C4.
2. Close box-size governance from source evidence.
3. Close availability/no-lookahead compatibility.
4. Run deterministic replay/unit QA.
5. Run 2016–2024 historical QA.
6. Record provenance and governance evidence.
7. Freeze 0030 only if all required gates pass; otherwise mark BLOCKED/NOT_EVALUABLE with reason.

0031 must not become the official next rule before 0030 is FROZEN or explicitly BLOCKED.
