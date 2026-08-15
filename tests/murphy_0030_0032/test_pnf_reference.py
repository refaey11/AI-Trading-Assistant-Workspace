import pytest

from src.murphy_0030_0032.pnf_reference import PNFConfig, PNFReferenceEngine


def test_x_column_checks_high_before_low():
    e = PNFReferenceEngine(PNFConfig(box_pct=0.01, anchor_price=100))
    e.seed("X", 100, "t0")
    assert e.process_bar("t1", 101.5, 98.0) == "CONTINUE_X"
    assert e.current.direction == "X"


def test_x_column_reverses_only_after_high_cannot_continue():
    e = PNFReferenceEngine(PNFConfig(box_pct=0.01, anchor_price=100))
    e.seed("X", 100, "t0")
    assert e.process_bar("t1", 100.5, 97.0) == "REVERSAL_O"
    assert e.current.direction == "O"


def test_o_column_checks_low_before_high():
    e = PNFReferenceEngine(PNFConfig(box_pct=0.01, anchor_price=100))
    e.seed("O", 100, "t0")
    assert e.process_bar("t1", 103.0, 98.0) == "CONTINUE_O"
    assert e.current.direction == "O"


def test_o_column_reverses_only_after_low_cannot_continue():
    e = PNFReferenceEngine(PNFConfig(box_pct=0.01, anchor_price=100))
    e.seed("O", 100, "t0")
    assert e.process_bar("t1", 103.1, 100.5) == "REVERSAL_X"
    assert e.current.direction == "X"


def test_deterministic_replay():
    bars = [("t1", 101.2, 100.2), ("t2", 102.5, 100.8), ("t3", 102.0, 98.0)]

    def run():
        e = PNFReferenceEngine(PNFConfig(box_pct=0.01, anchor_price=100))
        e.seed("X", 100, "t0")
        for row in bars:
            e.process_bar(*row)
        return [(c.direction, tuple(sorted(c.boxes)), c.start_timestamp, c.end_timestamp)
                for c in e.columns]

    assert run() == run()


def test_invalid_ohlc_is_rejected():
    e = PNFReferenceEngine(PNFConfig(box_pct=0.01, anchor_price=100))
    e.seed("X", 100, "t0")
    with pytest.raises(ValueError):
        e.process_bar("t1", 99.0, 100.0)
