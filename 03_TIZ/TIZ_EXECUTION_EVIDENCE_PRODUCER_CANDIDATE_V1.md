# TIZ Execution Evidence Producer Candidate V1

Status: CANDIDATE / NOT AUTHORITATIVE / NOT FROZEN

This producer records explicit plan-vs-actual execution evidence needed by TIZ 0005 and 0006.

0005 fields:
- loss_exit_plan
- actual_exit_reason
- exit_reason_matches_plan
- loss_event_occurred

0006 fields:
- profit_taking_plan
- actual_profit_action
- profit_action_matches_plan
- profit_taking_event_occurred

Every field carries value, availability, timestamp, provenance and state_semantics.

Non-negotiables:
- no psychological thresholds are invented;
- mechanical SL/TP hits are not substituted for adherence;
- TIZ direction remains NEUTRAL;
- missing evidence remains NOT_EVALUABLE;
- 2025 remains OOS;
- production promotion requires historical QA and provenance validation.
