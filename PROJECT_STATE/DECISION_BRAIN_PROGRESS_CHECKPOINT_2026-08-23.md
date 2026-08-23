# AI Trading Assistant — Decision Brain
## Project Progress Checkpoint — 2026-08-23

### Governance / frozen boundaries
- 2025 remains OOS and must never be tuned/calibrated from 2025 outcomes.
- Murphy supplies technical context / market structure.
- Steve Nison supplies candlestick confirmation/context and cannot generate direction.
- Trading in the Zone (TIZ) supplies process/psychology discipline only and is direction-neutral.
- Similarity Memory is historical evidence only and cannot be the sole decision maker.
- Risk is a hard execution gate.
- Unknown/unverified evidence remains fail-closed / NOT_EVALUABLE unless an explicitly isolated OOS evaluation policy permits unverified TIZ.

### Nison work completed
- Verified 44/44 Nison runtime rules in the frozen allowlist.
- Connected governed Nison runtimes to the 2025 producer boundary and merged to main.
- Resolved the CANDLE_RULE_0036 missing-trend fail-closed issue without inventing evidence.
- Full Nison runtime groups and Nison 2025 production CI checks passed.
- Nison role remains confirmation/contradiction only.

### TIZ work completed
- Historical attempt to require an authoritative psychological producer was recognized as semantically unsafe because private psychological states cannot be reconstructed from OHLC alone.
- Formalized TIZ runtime boundary as a process/evidence interface.
- Canonical three-book mode remains fail-closed when authoritative TIZ evidence is unavailable.
- Isolated 2025 OOS optional mode permits continuation with an explicit unverified-TIZ flag; it does not create direction or override Murphy/Nison/Risk.
- TIZ boundary resolution was merged to main after full CI pass.
- Added isolated optional-TIZ execution adapter and CircleCI gate; all observed checks for that change passed.

### Risk work completed
- Governed Risk Execution Runtime V1 was merged after CI pass.
- Risk remains a hard gate; stop/TP mechanics stay in Risk/Execution boundaries.

### Decision Brain rule boundary
- Frozen allowlist currently verifies 78 runtime rules: 34 Murphy + 44 Nison.
- Murphy_0008 remains explicitly blocked because an approved deterministic definition for “decisively broken” is absent from canonical freeze evidence.
- Therefore the corrected runtime-verified count is 78, not 79.

### 78-rule Decision-Event Stream work
- The previous 2025 assembler was only a partial boundary and hardcoded missing Nison/TIZ/Risk evidence, causing the preflight to return MISSING_AUTHORITATIVE_INPUT.
- PR #43 created a governed full 78-rule OOS Decision-Event Stream boundary.
- Boundary semantics: emit all 78 rule slots per timestamp; copy only existing runtime outputs; missing output remains NOT_EVALUABLE / NO_2025_OUTPUT; no invented direction, psychology, risk, SL/TP, thresholds, or 2025 tuning.
- PR #43 passed the full CI matrix and has merge commit `0601d7fc58e613f8d5110af4c4e7394d99b9871f`.
- GitHub metadata still showed the PR state as open despite a merge commit; treat the merge commit as the technical checkpoint and re-verify branch/main state before relying on metadata alone.

### Existing OOS diagnostic — NOT final
- Existing core profitability diagnostic is evaluation-only, not an official baseline and not the canonical three-book result.
- It evaluated 2,688 eligible timestamps from the partial Murphy stream: 1,411 BUY and 1,277 SELL.
- Results: TP 858, SL 1,550, Timeout 280, Total +166R, Profit Factor 1.1071, TP hit rate 31.92%, max sequential outcome drawdown -40R.
- It is explicitly invalid as the final three-book profitability result because the stream lacked authoritative Nison evidence and did not cover the full 78-rule Decision Brain runtime.

### Current next gate
1. Verify the 78-rule stream on actual 2025 inputs, producing explicit coverage counts per rule and timestamp.
2. Identify which rule outputs are genuinely available versus NOT_EVALUABLE / NO_2025_OUTPUT.
3. Do not manufacture missing evidence merely to increase coverage.
4. Only after the event stream has sufficient authoritative inputs, build/run the frozen 2025 OOS Decision-Event Stream and evaluate profitability.
5. Never promote the isolated core diagnostic to the official baseline.

### Key recent commits / PRs
- `fc0e5f52f2e2ab8930ce6f3b2849d76d06a73abd` — merged governed Nison 2025 producer boundary.
- `c8bac0f80ff58d44c9f2163be13c946570b5b10d` — merged TIZ runtime boundary resolution V2.
- `73b430a7cbc899ed2cc35f15b1ad9d31ec182891` — added isolated optional-TIZ execution CI verification.
- `f41f1ce2281c45c278133e9d26d52a41f652a047` — merged Risk Execution Runtime V1.
- `0601d7fc58e613f8d5110af4c4e7394d99b9871f` — PR #43 merge commit for governed full 78-rule Decision-Event Stream boundary.
- PR #42 — TIZ runtime boundary resolution (merged).
- PR #43 — governed full 78-rule Decision-Event Stream boundary (passed CI; merge metadata observed).

### Audit rule for future work
After every meaningful milestone: update this checkpoint in GitHub and create/update the corresponding Dropbox project checkpoint. Then continue from the recorded state; do not rely on chat history alone.
