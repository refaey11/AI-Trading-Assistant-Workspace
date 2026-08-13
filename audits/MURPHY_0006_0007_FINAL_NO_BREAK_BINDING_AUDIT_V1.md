# Murphy 0006–0007 Final No-Break Binding Audit V1

Date: 2026-08-13
Status: SOURCE SEMANTICS CONFIRMED / PRODUCTION BINDING NOT AUTHORIZED

## Scope
Compared the newly supplied `Archive1.zip` Chapter 4 knowledge artifacts against:
- MASTER_CANDIDATE_RULES_V1.json
- INTEGRATED_RULE_REGISTRY_V1.json
- MURPHY_0010 rule record
- existing 0006/0007 deterministic operator contract
- existing confirmation/evidence layer
- existing Geometry/Pivot contracts

## Archive1 findings
Chapter 4 trendline notes explicitly state:
- uptrend line connects successive reaction lows;
- downtrend line connects successive reaction highs;
- two points create a tentative line;
- confirmed trendline requires a 3rd successful touch and reaction without breaking;
- trendlines should enclose the daily price range;
- price filter example: 3% closing penetration for major trends and 1% for short-term;
- time filter: 2 consecutive trading-day closes beyond the trendline to confirm a valid breakout.

The JSON artifact states `price_filter = 3% closing price penetration` and `time_filter = 2 consecutive daily closes beyond trendline`.
The SQL artifact states valid breakouts require a price filter (3% rule) OR a time filter (2-day closing rule).

## Project rule records
MURPHY_0006 and MURPHY_0007 both contain:
- two-point tentative trendline;
- third successful touch and reaction confirms the trendline;
- empty `confirmation` field.

MURPHY_0010 contains only the generic requirement that a price or time filter be used before accepting a trendline break as meaningful; its exact rule record does not select a single filter for all contexts.

## Binding conclusion
Archive1 strengthens the provenance for the existence and meaning of the 3%/2-day trendline break filters. It does NOT provide an explicit rule-level statement saying `MURPHY_0006` or `MURPHY_0007` must use 3%, 1%, or 2-day as the production no-break operator.

Therefore:
- `3%` = source-backed general trendline filter, not 0006/0007-specific binding.
- `1%` = source-backed short-term example, not 0006/0007-specific binding.
- `2 consecutive daily closes` = source-backed time filter, but still not explicitly bound by the 0006/0007 rule record.

The project contract explicitly prohibits silently selecting one of these for 0006/0007. Making that selection would be a project design decision, not a pure source extraction.

## Successful-touch / reaction
Archive1 confirms the qualitative semantics but does not define a numeric touch tolerance or reaction magnitude/duration. Existing candidate evidence therefore remains observation/candidate evidence only.

## Production decision
Do NOT freeze 0006/0007 PASS/FAIL from Archive1 alone.
Current safe state remains:
- source semantics: CLOSED
- rule mapping: working/source-reconciled
- pivot/geometry availability: CLOSED
- candidate evidence/QA: CLOSED
- successful-touch deterministic operator: OPEN
- successful-reaction deterministic operator: OPEN
- no-break rule-level binding: OPEN
- production evaluator: NOT_YET_EVALUABLE

## Closest source-safe implementation candidate
If the project explicitly authorizes one source-backed break policy, the smallest candidate is the Murphy time-filter policy: two consecutive daily closes beyond the trendline constitute a meaningful break; absence of such a confirmed break preserves the line. This is a proposed binding, NOT an already frozen rule.

Do not implement this proposal as production without an explicit binding decision recorded in the project contract.

2025 remains OOS.
