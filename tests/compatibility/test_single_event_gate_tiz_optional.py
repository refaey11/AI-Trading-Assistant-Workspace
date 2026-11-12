from RUNTIME.DECISION_RUNTIME_V1.single_event_gate import validate_single_event


def _event():
    return {
        "symbol": "GBPUSD",
        "as_of": "2024-01-08T10:00:00Z",
        "market": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture"},
        "murphy": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture"},
        "nison": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture"},
        "memory": {"as_of": "2024-01-08T10:00:00Z", "provenance": "fixture"},
        "decision": {"direction": "NO_TRADE"},
        "risk": {"status": "BLOCK"},
        "trade_plan": None,
    }


def test_single_event_contract_does_not_require_tiz():
    result = validate_single_event(_event())
    assert result.passed is True
    assert not any("tiz" in failure.lower() for failure in result.failures)


def test_tiz_metadata_state_does_not_change_single_event_validation():
    absent = validate_single_event(_event())
    failed = _event()
    failed["tiz"] = {"status": "FAIL"}
    not_evaluable = _event()
    not_evaluable["tiz"] = {"status": "NOT_EVALUABLE"}
    assert validate_single_event(failed).passed is True
    assert validate_single_event(not_evaluable).passed is True
    assert validate_single_event(failed).failures == absent.failures
    assert validate_single_event(not_evaluable).failures == absent.failures
