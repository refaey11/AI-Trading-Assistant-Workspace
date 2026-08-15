import pytest

from src.murphy_0030_0032.pnf_3box_log_reference import (
    PNF3BoxLogReference,
    PNFBar,
    PNFBootstrapAmbiguity,
)


def test_bootstrap_waits_for_first_significant_direction():
    engine = PNF3BoxLogReference(box_pct=0.01)
    bars = [
        PNFBar("2020-01-01", 100.0, 101.0, 99.0, 100.0),
        PNFBar("2020-01-02", 100.0, 100.5, 99.5, 100.0),
        PNFBar("2020-01-03", 100.0, 102.2, 99.8, 102.0),
    ]
    columns = engine.build(bars)
    assert columns
    assert columns[0].kind == "X"
    assert columns[0].first_timestamp == "2020-01-03"


def test_bootstrap_down_direction():
    engine = PNF3BoxLogReference(box_pct=0.01)
    bars = [
        PNFBar("2020-01-01", 100.0, 101.0, 99.0, 100.0),
        PNFBar("2020-01-02", 100.0, 100.5, 99.5, 100.0),
        PNFBar("2020-01-03", 100.0, 100.2, 97.7, 98.0),
    ]
    columns = engine.build(bars)
    assert columns
    assert columns[0].kind == "O"
    assert columns[0].first_timestamp == "2020-01-03"


def test_bootstrap_same_bar_dual_trigger_is_not_silently_resolved():
    engine = PNF3BoxLogReference(box_pct=0.01)
    bars = [
        PNFBar("2020-01-01", 100.0, 101.0, 99.0, 100.0),
        PNFBar("2020-01-02", 100.0, 102.2, 97.7, 100.0),
    ]
    with pytest.raises(PNFBootstrapAmbiguity):
        engine.build(bars)


def test_high_low_priority_after_bootstrap():
    engine = PNF3BoxLogReference(box_pct=0.01)
    bars = [
        PNFBar("2020-01-01", 100.0, 101.0, 99.0, 100.0),
        PNFBar("2020-01-02", 100.0, 102.2, 100.0, 102.0),
        PNFBar("2020-01-03", 102.0, 103.5, 102.0, 103.0),
    ]
    columns = engine.build(bars)
    assert columns[0].kind == "X"
    assert len(columns) == 1
    assert columns[0].last_timestamp == "2020-01-03"
