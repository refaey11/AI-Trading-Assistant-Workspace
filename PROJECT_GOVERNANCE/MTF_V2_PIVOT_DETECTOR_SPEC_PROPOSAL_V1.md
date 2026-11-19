# MTF Producer V2 — Pivot Detector Specification Proposal V1

**Status:** REVIEW PROPOSAL ONLY — NOT APPROVED POLICY — NO DETECTOR IMPLEMENTATION.

Date: 2026-11-19  
Parent design: PR #139, MTF Producer V2 alternative semantics  
Scope: independently versioned confirmed swing/pivot detection for M5, M15, M30, H1, H4, D1.

## 1. Purpose and non-goals

This proposal defines the decisions required before a new pivot detector can be implemented. It does not reconstruct historical `PIVOT_SEQUENCE_V2`, does not claim parity with legacy `trend_regime` / `mtf_trend_score`, and does not alter the already-approved V2 HH/HL, LH/LL, BOS/CHOCH semantics.

The detector must emit evidence only. It cannot generate trade direction, BUY/SELL, entries, SL/TP, or orders. It cannot replace Murphy's governed role or bypass the Risk hard gate.

## 2. Existing evidence and compatibility boundary

- The historical Murphy 0008 H1 audit reports a pivot availability delay of two same-timeframe bars and an H1 QA population.
- That audit does not provide the executable detector, complete schema, or proof of identical behavior on M5/M15/M30/H4/D1.
- The current V2 prototype consumes caller-supplied confirmed pivots. It is not a detector.
- The prototype currently enforces a two-bar minimum delay. That implementation detail must not be promoted into a universal six-timeframe detector rule without approval and evidence.
- Reuse the existing completed OHLC source, capture, timestamp/provenance and evidence-envelope work. Do not build a second candle aggregator or timestamp normalizer.

## 3. Proposed detector input boundary

A detector invocation is scoped to exactly one `symbol` and one native source timeframe. It receives ordered source bars that have passed upstream OHLC, completion, identity, and provenance checks.

Required source facts:
- symbol and native timeframe;
- stable source-bar identity and sequence index;
- open, high, low, close;
- bar open/close timestamps and verified availability evidence;
- source payload hash and producer/schema version;
- explicit source-gap and missingness status.

No detector may infer broker timezone, DST, tick size, missing bars, or session calendars. If required source facts are absent or untrusted, output must be `NOT_EVALUABLE` / unavailable rather than guessed.

## 4. Swing candidate definition — decision required

A common candidate definition is a local extremum over a left and right neighborhood. The exact neighborhood and tie policy are unresolved.

### 4.1 Left/right lookback

Options for review:
- **A — symmetric window:** candidate bar i is compared with L completed bars to its left and R completed bars to its right, with L and R configured explicitly.
- **B — asymmetric window:** independent left/right windows per timeframe.
- **C — canonical-source reuse:** consume the original pivot producer if its executable implementation and six-TF contract are recovered; do not implement a replacement detector.

No numeric L/R values are selected in this proposal. In particular, the H1 historical two-bar availability fact is not proof that R=2 is the right detector rule for every timeframe.

### 4.2 High/low candidate comparisons

For a swing high, the candidate high is compared with neighboring highs; for a swing low, candidate low is compared with neighboring lows. The contract must specify strict versus non-strict comparisons and must define how equal prices are treated. A detector must not silently round prices or introduce a tolerance.

### 4.3 Equal highs and equal lows

Choose and test one explicit policy:
- reject the entire equal-price plateau as ambiguous;
- select the first bar in the plateau;
- select the last bar in the plateau;
- select a uniquely defined center bar;
- emit a plateau object rather than a single pivot.

No option is selected here. The selected rule must be deterministic under replay and must preserve source precision.

### 4.4 Same-bar dual candidate

A wide-range bar can be a candidate high and low under some window definitions. Decide whether to:
- allow two distinct pivots from the same source bar;
- reject both as ambiguous;
- retain both but mark their ordering unavailable.

Do not infer intrabar sequence from OHLC.

## 5. Confirmation and availability — decision required

A pivot must never be visible on its visual source bar merely because it is later recognized as an extremum.

Candidate availability rule for a chosen right-window R:
- the candidate at source index i remains pending until all required right-side bars have completed;
- it becomes eligible only after the final required right-side bar is completed and its verified availability is established;
- its `available_at` must be the actual verified availability of that confirming bar, not a fabricated timestamp;
- it must not be consumed before that availability instant.

This is a proposed causal pattern, not an approved numeric delay. Confirm whether confirmation is strictly based on completed bars and whether any additional validation is required. If the canonical producer is recovered, its exact confirmation semantics take precedence only after compatibility review.

## 6. Pivot ordering, separation, and alternation — decision required

The detector must not silently impose a minimum bar distance, minimum price distance, or alternating HIGH/LOW sequence.

Options:
- retain every independently confirmed pivot;
- require a minimum source-bar separation;
- require alternating HIGH/LOW pivots with an explicit replacement rule;
- expose all confirmed pivots and defer any selection to a separately governed consumer.

No minimum separation, alternation, clustering, or replacement rule is selected. Any such rule needs a source-based rationale and synthetic fixtures; it must not be fitted to profitability or 2025 outcomes.

## 7. Price precision and identity — decision required

- Preserve source price precision exactly; do not use arbitrary decimal rounding.
- A tick-size/price-precision contract must be supplied by trusted instrument metadata before equality or comparison normalization is applied.
- If precision metadata is unavailable, do not invent a tolerance; mark equality-sensitive cases `NOT_EVALUABLE`.
- Pivot identity must be deterministic and unique within symbol/timeframe/source lineage. Proposed identity ingredients are source-bar identity, pivot kind, detector version, and configuration fingerprint. The final encoding is unresolved.

## 8. Gaps, warm-up, and window boundaries — decision required

This proposal does not define session-gap handling, feed-outage behavior, pivot expiry, invalidation, or event deduplication; those remain separately governed by the event lifecycle review.

The detector contract must decide:
- whether a source gap blocks confirmation, resets pending candidates, or preserves them with explicit continuity evidence;
- whether pre-window bars may be supplied as warm-up context;
- whether a pre-window pivot may seed the first output row, and what source/availability proof is required;
- how many warm-up bars are required once L/R are approved;
- how truncated beginning/end windows are represented.

No gap may be silently treated as a normal adjacent bar. No pre-window pivot may be accepted without its original source identity and verified availability.

## 9. Six-timeframe policy

The detector must be independently evaluated for each native timeframe:
- M5
- M15
- M30
- H1
- H4
- D1

Do not assume one parameter set, confirmation delay, session-gap policy, or coverage level applies to all six. Each timeframe needs an explicit configuration/version and separate golden fixtures. A missing or unverified timeframe remains unavailable; it must not be synthesized from another timeframe.

W1 remains part of the wider Dynamic MTF role architecture but is not part of this six-timeframe serialized producer contract.

## 10. Proposed output contract (field proposal, not frozen schema)

Each confirmed pivot should carry at least:
- `symbol`, `timeframe`;
- `pivot_id`, `pivot_kind` (HIGH/LOW), `pivot_price`;
- `source_bar_id`, `source_bar_index`, `source_bar_time`;
- `confirmation_bar_id`, `confirmation_bar_index`;
- `available_at` with explicit offset and verified provenance reference;
- `detector_version`, `schema_version`, `configuration_fingerprint`;
- `source_payload_sha256`, `availability_status`.

Candidate statuses include `PENDING`, `CONFIRMED`, `NOT_EVALUABLE`, and `UNAVAILABLE`; final vocabulary and transition rules require approval. Rejected candidates should be auditable without being exposed as confirmed pivots.

## 11. Required synthetic golden fixtures

After policy approval, create deterministic literal fixtures separately for each of the six timeframes. At minimum:
1. isolated swing high;
2. isolated swing low;
3. candidate before right-side confirmation;
4. candidate confirmed only after all required right bars complete;
5. equal-high plateau;
6. equal-low plateau;
7. same-bar dual high/low candidate;
8. strict versus non-strict boundary equality;
9. consecutive candidate extrema and minimum-separation behavior;
10. alternating and non-alternating pivot sequences;
11. missing bar inside the confirmation window;
12. expected weekend/session closure versus unexplained feed gap;
13. truncated warm-up and pre-window seed pivot;
14. invalid OHLC / unfinished bar;
15. future-bar perturbation leaves all earlier outputs unchanged;
16. replaying identical source and configuration yields byte-identical pivot IDs and outputs.

Every fixture must assert exact source identity, confirmation index/time, availability time, status, and expected pivot IDs. These are planned tests, not passing results.

## 12. Approval checklist — no implementation until resolved

The user/reviewer must explicitly approve:
1. canonical producer reuse versus new detector;
2. left/right window model and per-timeframe values;
3. strict/non-strict comparison behavior;
4. equal-high/equal-low policy;
5. same-bar dual-candidate policy;
6. completed-bar confirmation and exact availability rule;
7. minimum separation and alternation/replacement behavior;
8. price precision source and equality handling;
9. source-gap behavior and warm-up/pre-window policy;
10. final output schema and deterministic identity.

Until then:
- no detector code or formula is authorized;
- no universal two-bar delay is assumed;
- no legacy field mapping or Decision Brain integration;
- no backtest tuning, no 2025 data, no live trading, no order path;
- PR remains Draft and unmerged; no main-branch changes.

## 13. Explicit unresolved questions for review

Please review the ten approval items in Section 12. If you want the safest first implementation path, the key architectural choice is whether to keep searching for the canonical producer or formally approve an independently versioned detector. All numeric and tie-handling choices remain open until separately approved.


## 14. User direction and conservative implementation recommendations (2026-11-19)

The user has agreed to proceed with an independently versioned MTF Pivot Detector V2. This approves the architectural path only. It does not approve numeric windows or the unresolved detection policies below.

The following are recommendations for explicit review, not frozen rules:

| Topic | Conservative recommendation | Why it is proposed | Approval still required |
| --- | --- | --- | --- |
| Detector architecture | New independent V2 detector; keep legacy PIVOT_SEQUENCE_V2 namespace untouched | Original executable producer and six-TF contract remain unrecovered | Architectural path approved by user; implementation still waits on detailed contract |
| Window model | Symmetric left/right windows, with explicit per-timeframe configuration | Easier to reason about and test causally; avoids hidden asymmetry | Yes; numeric L/R values for each timeframe remain open |
| Extremum comparison | Strict comparison against neighboring highs/lows | Avoids silently resolving ties as unique pivots | Yes |
| Equal-price plateau | Mark ambiguous plateau NOT_EVALUABLE rather than arbitrarily selecting first/last/center | Avoids invented ordering and hidden tie-breaking | Yes |
| Same-bar high and low | Preserve both candidate observations but mark sequence/order unresolved; do not infer intrabar path | OHLC cannot reveal which extreme occurred first | Yes |
| Confirmation | Completed right-side bars only; availability is the verified availability of the final required confirming bar | Prevents look-ahead and visual-pivot-time leakage | Yes; confirm this rule and the selected R values |
| Separation / alternation | No minimum distance, no forced alternation, no clustering; expose independently confirmed pivots | Avoids introducing ungrounded filtering or replacement behavior | Yes |
| Price precision | Use trusted instrument metadata; no arbitrary rounding/tolerance; otherwise equality-sensitive cases NOT_EVALUABLE | Avoids false equality or separation | Yes |
| Data gaps | A gap inside the confirmation window blocks confirmation unless upstream source/session evidence explicitly proves continuity | Prevents treating missing data as ordinary adjacent bars | Yes |
| Warm-up | Allow pre-window context only with original source identity, verified availability and full provenance; never synthesize a seed pivot | Supports deterministic replay without look-ahead | Yes |
| Output identity | Deterministic ID from symbol, timeframe, source-bar identity, pivot kind, detector version and configuration fingerprint | Reproducible lineage and auditability | Yes; exact serialization/hash contract |

### Recommended implementation sequence after approval

1. Freeze the detector contract and six per-timeframe configurations.
2. Write literal synthetic golden fixtures before detector code.
3. Implement a pure deterministic detector isolated from the existing structure producer.
4. Run no-lookahead, future-perturbation, gap, tie, warm-start and replay-determinism tests.
5. Validate each timeframe independently; an unverified timeframe remains unavailable.
6. Only then consider a separate compatibility adapter review. No Decision Brain integration is implied.

No detector implementation is authorized by this recommendation table. The two-bar H1 historical report remains H1-only evidence and is not generalized to the other five timeframes.
