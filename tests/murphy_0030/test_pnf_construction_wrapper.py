from src.murphy_0030.pnf_construction_wrapper import PnFState, decide_high_low, freeze_box_size


def test_x_column_high_continuation_has_priority_over_low():
    state = PnFState("X", 100.0, 96.0)
    d = decide_high_low(high=101.0, low=90.0, state=state, box_size=1.0)
    assert d.action == "continue"
    assert d.target_column == "X"
    assert d.price == 101.0


def test_x_column_low_reversal_only_if_high_does_not_continue():
    state = PnFState("X", 100.0, 96.0)
    d = decide_high_low(high=100.0, low=97.0, state=state, box_size=1.0)
    assert d.action == "reverse"
    assert d.target_column == "O"
    assert d.price == 97.0


def test_o_column_low_continuation_has_priority_over_high():
    state = PnFState("O", 100.0, 96.0)
    d = decide_high_low(high=110.0, low=95.0, state=state, box_size=1.0)
    assert d.action == "continue"
    assert d.target_column == "O"
    assert d.price == 95.0


def test_o_column_high_reversal_only_if_low_does_not_continue():
    state = PnFState("O", 100.0, 96.0)
    d = decide_high_low(high=99.0, low=96.0, state=state, box_size=1.0)
    assert d.action == "reverse"
    assert d.target_column == "X"
    assert d.price == 99.0


def test_box_size_is_frozen_for_a_bar_reference():
    assert freeze_box_size(100.0, 0.5) == 0.5
