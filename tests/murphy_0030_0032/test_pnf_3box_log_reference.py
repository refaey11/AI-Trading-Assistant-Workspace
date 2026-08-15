from src.murphy_0030_0032.pnf_3box_log_reference import PNF3BoxLogReference, PNFBar


def bars(*rows):
    return [PNFBar(*r) for r in rows]


def test_x_high_first_and_three_box_reversal():
    engine = PNF3BoxLogReference(box_pct=0.01)
    result = engine.build(bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 97, 100),
    ))
    assert [c.kind for c in result] == ["X", "O"]
    assert len(result[1].boxes) == 3


def test_o_low_first_and_three_box_reversal():
    engine = PNF3BoxLogReference(box_pct=0.01)
    result = engine.build(bars(
        ("2024-01-01", 100, 101, 99, 99),
        ("2024-01-02", 99, 100, 96, 97),
        ("2024-01-03", 97, 104, 96, 103),
    ))
    assert [c.kind for c in result] == ["O", "X"]
    assert len(result[1].boxes) == 3


def test_deterministic_replay():
    data = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 97, 100),
        ("2024-01-04", 100, 100, 94, 95),
    )
    a = PNF3BoxLogReference(0.01).build(data)
    b = PNF3BoxLogReference(0.01).build(data)
    assert [(c.kind, c.boxes) for c in a] == [(c.kind, c.boxes) for c in b]


def test_future_suffix_does_not_change_existing_prefix():
    prefix = bars(
        ("2024-01-01", 100, 101, 99, 101),
        ("2024-01-02", 101, 104, 100, 103),
        ("2024-01-03", 103, 104, 97, 100),
    )
    suffix = bars(
        ("2024-01-04", 100, 100, 94, 95),
        ("2024-01-05", 95, 99, 95, 98),
    )
    p = PNF3BoxLogReference(0.01).build(prefix)
    f = PNF3BoxReference(0.01).build(prefix + suffix) if False else PNF3BoxLogReference(0.01).build(prefix + suffix)
    assert [(c.kind, c.boxes) for c in p] == [(c.kind, c.boxes) for c in f[:len(p)]]
