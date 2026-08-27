from compatibility.dynamic_mtf_opportunity_ranker_v1 import select_best_opportunity


def _complete(direction="BUY"):
    return {
        "context_complete": True,
        "structure_complete": True,
        "setup_complete": True,
        "confirmation_complete": True,
        "risk_feasible": True,
        "contradicted": False,
        "direction": direction,
    }


def test_selects_highest_existing_execution_timeframe_on_equal_quality():
    base = _complete()
    result = select_best_opportunity({"D1": {}, "H4": {}, "H1": {}, "M30": base, "M15": base, "M5": base})
    assert result.status == "PASS"
    assert result.selected_timeframe == "M30"
    assert result.selected_direction == "BUY"
    assert len(result.all_verdicts) == 6


def test_rejects_contradicted_and_incomplete_candidates():
    result = select_best_opportunity({
        "D1": {}, "H4": {}, "H1": {},
        "M30": {**_complete(), "risk_feasible": False},
        "M15": {**_complete(), "contradicted": True},
        "M5": {**_complete(), "setup_complete": False},
    })
    assert result.status == "NO_TRADE"
    assert result.selected_timeframe is None


def test_never_uses_performance_or_2025_fields_for_selection():
    result = select_best_opportunity({"M30": {
        **_complete(),
        "historical_pf": 999.0,
        "year": 2025,
    }})
    assert result.status == "PASS"
    assert result.selected_timeframe == "M30"
    assert all("2025" not in reason for reason in result.selection_reasons)
