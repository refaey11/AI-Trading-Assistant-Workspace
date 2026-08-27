from compatibility.dynamic_mtf_runtime_resolver_v1 import resolve_mtf_event


def test_resolves_complete_chain_without_performance_fields():
    evidence = {
        "D1": {"context_complete": True, "alignment_state": "ALIGNED"},
        "H4": {"context_complete": True, "structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": True, "alignment_state": "ALIGNED"},
        "H1": {"context_complete": True, "structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": True, "alignment_state": "ALIGNED"},
        "M30": {"structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": True, "alignment_state": "ALIGNED"},
        "M15": {"structure_complete": False, "setup_complete": False, "confirmation_complete": False, "risk_feasible": False, "alignment_state": "ALIGNED"},
        "M5": {"structure_complete": False, "setup_complete": False, "confirmation_complete": False, "risk_feasible": False, "alignment_state": "ALIGNED"},
    }
    result = resolve_mtf_event(timeframe_evidence=evidence)
    assert result.status == "PASS"
    assert result.selected_execution_timeframe == "M30"
    assert result.macro_timeframe == "D1"
    assert result.context_timeframes_used[:2] == ("D1", "D1")
    assert result.setup_timeframe == "H4"
    assert result.confirmation_timeframes_used == ("H1",)
    assert result.alignment_state == "ALIGNED"


def test_fails_closed_without_risk_feasibility():
    evidence = {
        "D1": {"context_complete": True},
        "H4": {"context_complete": True, "structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": False},
        "H1": {"context_complete": True, "structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": False},
        "M30": {"structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": False},
        "M15": {"structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": False},
        "M5": {"structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": False},
    }
    result = resolve_mtf_event(timeframe_evidence=evidence)
    assert result.status == "NOT_EVALUABLE"
    assert result.selected_execution_timeframe is None


def test_explicit_conflict_remains_visible():
    evidence = {
        "D1": {"context_complete": True, "alignment_state": "CONFLICTED"},
        "H4": {"context_complete": True, "structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": True, "alignment_state": "CONFLICTED"},
        "H1": {"context_complete": True, "structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": True, "alignment_state": "CONFLICTED"},
        "M30": {"structure_complete": True, "setup_complete": True, "confirmation_complete": True, "risk_feasible": True, "alignment_state": "CONFLICTED"},
    }
    result = resolve_mtf_event(timeframe_evidence=evidence)
    assert result.status == "PASS"
    assert result.alignment_state == "CONFLICTED"
