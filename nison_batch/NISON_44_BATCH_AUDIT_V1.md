# Nison 44-Rule Batch Audit V1

Built from the integrated rule registry plus the Steve Nison Master KB extracted locally, including the Formation Rules files for the candle patterns.

## Batch result after source-level scan
- Total rules: 44
- BATCH_READY_CANDIDATE: 7
- SOURCE_LOCK_REVIEW: 31
- CONCEPT_GATE: 6

The earlier registry-only classification was too optimistic. The source-level scan found qualitative terms such as `near`, `long`, `small`, `strong`, `ideally`, `slightly`, `approximately`, `similar`, `gradually`, and `clear`. These are kept as blockers rather than being converted into invented numeric thresholds.

## Shared primitives
- trend_context
- confirmation_window
- candle_sequence
- ohlc_relationships
- gap_window
- volume_context
- sr_context

## Batch-ready candidates
- CANDLE_RULE_0012 | Abandoned Baby | existing trend + three-candle sequence + isolated doji + two gaps
- CANDLE_RULE_0021 | Three Mountains | three peaks + resistance test + bearish confirmation evidence
- CANDLE_RULE_0023 | Three Buddha Tops | three peaks + middle peak highest + outer peaks lower
- CANDLE_RULE_0024 | Three Buddha Bottoms | three bottoms + middle bottom lowest + outer bottoms higher
- CANDLE_RULE_0034 | Separating Lines | existing uptrend + equal opens + black then white candle
- CANDLE_RULE_0035 | Tasuki Gap | existing trend + gap/window + retracement candle remains inside window + window not closed
- CANDLE_RULE_0038 | Windows | existing trend + gap + open window + support/resistance context

These are candidates for evaluator generation, not Frozen rules yet.

## Source-lock review
The remaining 31 pattern rules need canonical handling for qualitative descriptors before deterministic evaluation. Examples include:
- 0001-0004: `small`, `large/stronger`, and related formation-strength wording.
- 0005-0007: `long`, `near`, `slightly`, `well into`.
- 0008-0011: `long`, `small`, `strong`, `ideally/preferably`, `deeply`.
- 0013-0019: `long`, `small`, `near`, `significantly`, `clear` and similar language.
- 0020-0022: `approximately/equal` style wording where present in the source.
- 0025-0033: rounded/gradual/long/small/consolidation/stabilization and similar descriptive terms.
- 0036-0037: `clear`, `approximately`, and `similar body size` language.

## Concept gate
0039-0044 are not ordinary candle-pattern recognizers. They represent higher-level confirmation/confluence concepts and therefore need context/evidence evaluators rather than a simple candle-shape detector.

## Execution policy
- No threshold is invented from backtest outcomes.
- Nison remains confirmation-only and cannot create LONG/SHORT direction.
- Existing evaluators/artifacts are reused before any rebuild.
- BATCH_READY_CANDIDATE -> OPERATOR_READY -> EVALUATOR_READY -> UNIT_TESTED -> HISTORICAL_QA -> AVAILABILITY/NO_LOOKAHEAD -> FREEZE.
- A blocker in one rule does not stop independent rules.
- 2025 stays OOS and is excluded from tuning/selection.
