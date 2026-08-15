from src.murphy_0030_0032.pnf_3box_reference import (
    PNF3BoxReference,
    PNFBar,
    bullish_support_reference,
    stop_reference,
)


def bars(*rows):
    return [PNFBar(*r) for r in rows]


def signature(columns):
    return [(c.kind, tuple(c.boxes)) for c in columns]


def test_x_column_checks_high_before_low():
    result = PNF3BoxReference(1.0).build(bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
    ))
    assert [c.kind for c in result] == ["X"]
    assert result[0].boxes[-1] == 104


def test_x_column_reverses_only_after_high_cannot_continue():
    result = PNF3BoxReference(1.0).build(bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 99, 100),
    ))
    assert [c.kind for c in result] == ["X", "O"]
    assert result[1].boxes == [103, 102, 101]


def test_o_column_checks_low_before_high():
    result = PNF3BoxReference(1.0).build(bars(
        ("2024-01-01", 100, 101, 99, 99),
        ("2024-01-02", 99, 100, 96, 97),
        ("2024-01-03", 97, 98, 94, 95),
    ))
    assert [c.kind for c in result] == ["O"]
    assert result[0].boxes[-1] == 94


def test_o_column_reverses_only_after_low_cannot_continue():
    result = PNF3BoxReference(1.0).build(bars(
        ("2024-01-01", 100, 101, 99, 99),
        ("2024-01-02", 99, 100, 96, 97),
        ("2024-01-03", 97, 100, 96, 99),
    ))
    assert [c.kind for c in result] == ["O", "X"]
    assert result[1].boxes == [97, 98, 99]


def test_bullish_support_uses_lowest_o_column_base():
    columns = PNF3BoxReference(1.0).build(bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 99, 100),
    ))
    support = bullish_support_reference(columns)
    assert support["direction"] == "UP"
    assert support["origin_price"] == 101
    assert support["box_step_per_column"] == 1


def test_stop_references_previous_opposite_column_without_offset():
    columns = PNF3BoxReference(1.0).build(bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 99, 100),
        ("2024-01-04", 100, 100, 94, 95),
        ("2024-01-05", 95, 99, 95, 98),
    ))
    bull = stop_reference(columns, "BULLISH")
    bear = stop_reference(columns, "BEARISH")
    assert bull["reference_column"] == "O"
    assert bull["placement_relation"] == "BELOW"
    assert bear["reference_column"] == "X"
    assert bear["placement_relation"] == "ABOVE"


def test_replay_is_deterministic():
    data = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 99, 100),
        ("2024-01-04", 100, 100, 94, 95),
        ("2024-01-05", 95, 99, 95, 98),
    )
    assert signature(PNF3BoxReference(1.0).build(data)) == signature(PNF3BoxReference(1.0).build(data))


def test_prefix_replay_is_stable_at_the_prefix_boundary():
    data = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 99, 100),
        ("2024-01-04", 100, 100, 94, 95),
        ("2024-01-05", 95, 99, 95, 98),
    )
    prefix = data[:3]
    assert signature(PNF3BoxReference(1.0).build(prefix)) == signature(PNF3BoxReference(1.0).build(prefix))
