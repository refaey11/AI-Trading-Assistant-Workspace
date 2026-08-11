# Murphy 0008–0009 Compatibility Gate V1

Date: 2026-08-12

## Scope

Advance the project beyond the 0006–0007 bottleneck without inventing new operators or rebuilding existing components.

## Registry status

The existing Murphy Rule Workspace Status lists:
- MURPHY_0008: PARTIAL — “A support level is decisively broken to the downside.”
- MURPHY_0009: PARTIAL — “A resistance level is decisively broken to the upside.”
- Both currently have no dedicated evaluator artifact.

## Existing source terminology

The supplied Western technical source defines:
- Support Level: an area where buyers are expected to appear in greater numbers.
- Resistance Level: a level where an increase in sellers is expected.
- Time Filter: a requirement that prices remain above or below certain levels for a period of time to confirm that an important technical area has been broken.

The project must preserve these source terms and must not convert “decisively broken” into an invented numeric threshold.

## Existing infrastructure

The project already contains Pivot Sequence V2, Trendline Geometry V1, and other market-structure components. Existing components must be compatibility-audited before any adapter is added.

## Gate decision

**0008/0009: SOURCE SEMANTICS PARTIAL / OPERATOR NOT YET CLOSED**

The registry wording is sufficient to identify the target event, but the currently retrieved project artifacts do not establish the exact operational definition of “decisively broken” for the evaluator.

Do not invent:
- ATR distance
- percentage distance
- candle-count confirmation
- close-vs-wick rule
- lookback
- new support/resistance construction rule

## Dependency: MURPHY_0010

MURPHY_0010 is separately recorded as: “A price or time filter is used before accepting the break as meaningful.” Its presence means the 0008/0009 break event and the 0010 confirmation/filter semantics must remain separate until their source contracts are verified.

## Next action

Recover the authoritative Rule Registry/source records for 0008, 0009, and 0010, then compatibility-audit them against existing support/resistance and time-filter artifacts. If the exact operator is already represented upstream, write only the missing evaluator adapter and tests. Otherwise keep the rule PARTIAL/NOT_EVALUABLE and continue to the next rule group.

2025 remains OOS and is not used for tuning or implementation selection.
