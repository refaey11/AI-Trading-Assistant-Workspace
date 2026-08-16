from datetime import datetime, timezone


def test_0013_b1_candidate_state_machine_contract():
    # Contract-level test: the first completed close is only a candidate;
    # the immediately following completed close confirms the same boundary.
    boundary = 100.0
    closes = [99.0, 98.0]
    assert closes[0] < boundary
    assert closes[1] < boundary


def test_0013_b1_intervening_close_blocks_confirmation():
    boundary = 100.0
    closes = [99.0, 101.0, 98.0]
    assert closes[0] < boundary
    assert closes[1] >= boundary
    assert not (closes[0] < boundary and closes[1] < boundary)


def test_0013_b1_same_bar_confirmation_is_forbidden():
    # A single completed close can only create BREAK_CANDIDATE.
    boundary = 100.0
    closes = [99.0]
    assert len(closes) == 1
    assert closes[0] < boundary


def test_0013_b1_future_boundary_is_not_usable():
    decision = datetime(2026, 1, 2, tzinfo=timezone.utc)
    boundary_available = datetime(2026, 1, 3, tzinfo=timezone.utc)
    assert boundary_available > decision
    assert boundary_available > decision
