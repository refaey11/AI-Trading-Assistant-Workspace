from tiz_execution_evidence_producer_candidate_v1 import build_evidence


def test_plan_vs_actual_matches_and_stays_neutral():
    e = build_evidence(
        loss_exit_plan="invalidation",
        actual_exit_reason="invalidation",
        profit_taking_plan="planned_target",
        actual_profit_action="planned_target",
        loss_event_occurred=True,
        profit_taking_event_occurred=False,
        timestamp="2026-08-19T00:00:00Z",
    )
    assert e["exit_reason_matches_plan"]["value"] is True
    assert e["profit_action_matches_plan"]["value"] is True
    assert e["direction"] == "NEUTRAL"


def test_missing_plan_is_not_invented():
    e = build_evidence(actual_exit_reason="manual", timestamp="2026-08-19T00:00:00Z")
    assert e["exit_reason_matches_plan"]["value"] is None
    assert e["exit_reason_matches_plan"]["availability"] is False
