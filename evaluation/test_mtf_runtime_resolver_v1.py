from evaluation.mtf_runtime_resolver_v1 import resolve_mtf


def test_resolves_single_valid_candidate():
    event = {
        "holding_horizon": "30-120 minutes",
        "timeframes": {
            "D1": {"available": True, "context_complete": True},
            "H4": {"available": True, "context_complete": True},
            "H1": {
                "available": True,
                "context_complete": True,
                "confirmation_complete": True,
                "setup_complete": False,
                "risk_feasible": True,
                "higher_timeframe_conflict": False,
            },
            "M30": {
                "available": True,
                "setup_complete": True,
                "confirmation_complete": True,
                "risk_feasible": True,
                "higher_timeframe_conflict": False,
            },
            "M15": {"available": True},
            "M5": {"available": True},
        },
    }
    out = resolve_mtf(event)
    assert out.status == "RESOLVED"
    assert out.selected_execution_timeframe == "M30"
    assert "D1" in out.context_timeframes_used
    assert "H1" in out.confirmation_timeframes_used


def test_fails_closed_on_multiple_valid_candidates():
    base = {
        "available": True,
        "setup_complete": True,
        "confirmation_complete": True,
        "risk_feasible": True,
        "higher_timeframe_conflict": False,
    }
    event = {"timeframes": {tf: dict(base) for tf in ("M5", "M15", "M30", "H1", "H4", "D1")}}
    out = resolve_mtf(event)
    assert out.status == "NO_TRADE_MTF_AMBIGUOUS"
    assert out.selected_execution_timeframe is None


def test_fails_closed_on_no_candidate():
    event = {"timeframes": {"M5": {"available": True}}}
    out = resolve_mtf(event)
    assert out.status == "NO_TRADE_NO_VALID_EXECUTION_CANDIDATE"
    assert out.selected_execution_timeframe is None
