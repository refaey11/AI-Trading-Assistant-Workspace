from compatibility.dynamic_mtf_binding_adapter_v1 import bind_dynamic_mtf


def test_valid_explicit_role_assignment_passes_without_direction():
    r = bind_dynamic_mtf(
        available_timeframes=["M5", "M15", "M30", "H1", "H4", "D1"],
        role_assignments={
            "macro_context": "D1",
            "context": "H4",
            "setup": "H1",
            "confirmation": "M30",
            "execution": "M15",
        },
        evidence_trace=["D1 trend", "H4 context", "H1 setup"],
    )
    assert r.status == "PASS"
    assert r.alignment_state == "ALIGNED"
    assert r.final_trade_decision is None


def test_missing_role_evidence_fails_closed():
    r = bind_dynamic_mtf(
        available_timeframes=["M5", "M15", "M30", "H1", "H4", "D1"],
        role_assignments={"macro_context": "D1"},
    )
    assert r.status == "NOT_EVALUABLE"


def test_forbidden_timeframe_fails_closed():
    r = bind_dynamic_mtf(
        available_timeframes=["M5", "M15", "M30", "H1", "H4", "D1"],
        role_assignments={
            "macro_context": "D1",
            "context": "H4",
            "setup": "H2",
            "confirmation": "M30",
            "execution": "M15",
        },
    )
    assert r.status == "NOT_EVALUABLE"


def test_lower_timeframe_cannot_override_higher_context_order():
    r = bind_dynamic_mtf(
        available_timeframes=["M5", "M15", "M30", "H1", "H4", "D1"],
        role_assignments={
            "macro_context": "H4",
            "context": "D1",
            "setup": "H1",
            "confirmation": "M30",
            "execution": "M15",
        },
    )
    assert r.status == "NOT_EVALUABLE"
    assert r.alignment_state == "CONFLICTED"
