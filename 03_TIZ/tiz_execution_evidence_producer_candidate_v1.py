"""TIZ execution evidence producer candidate.

Records plan-vs-actual evidence without inventing psychological semantics.
Candidate only: it does not promote the TIZ producer or generate direction.
"""


def build_evidence(*, loss_exit_plan=None, actual_exit_reason=None,
                   profit_taking_plan=None, actual_profit_action=None,
                   loss_event_occurred=False,
                   profit_taking_event_occurred=False,
                   timestamp=None, provenance="execution_record_producer_v1"):
    def envelope(value):
        return {
            "value": value,
            "availability": value is not None,
            "timestamp": timestamp,
            "provenance": provenance,
            "state_semantics": "explicit_execution_record",
        }

    return {
        "loss_exit_plan": envelope(loss_exit_plan),
        "actual_exit_reason": envelope(actual_exit_reason),
        "exit_reason_matches_plan": envelope(
            None if loss_exit_plan is None or actual_exit_reason is None
            else loss_exit_plan == actual_exit_reason),
        "loss_event_occurred": envelope(loss_event_occurred),
        "profit_taking_plan": envelope(profit_taking_plan),
        "actual_profit_action": envelope(actual_profit_action),
        "profit_action_matches_plan": envelope(
            None if profit_taking_plan is None or actual_profit_action is None
            else profit_taking_plan == actual_profit_action),
        "profit_taking_event_occurred": envelope(profit_taking_event_occurred),
        "direction": "NEUTRAL",
    }
