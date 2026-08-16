from adapter_gate_0001_0002 import Candle, evaluate_hard_geometry


def test_bullish_engulfing_hard_geometry():
    assert evaluate_hard_geometry(
        "NISON_0001",
        Candle(1.10, 1.00),
        Candle(0.98, 1.12),
    ) is True


def test_bullish_engulfing_rejects_wrong_polarity():
    assert evaluate_hard_geometry(
        "NISON_0001",
        Candle(1.00, 1.10),
        Candle(0.98, 1.12),
    ) is False


def test_bearish_engulfing_hard_geometry():
    assert evaluate_hard_geometry(
        "NISON_0002",
        Candle(1.00, 1.10),
        Candle(1.12, 0.98),
    ) is True


def test_bearish_engulfing_rejects_incomplete_body_engulfment():
    assert evaluate_hard_geometry(
        "NISON_0002",
        Candle(1.00, 1.10),
        Candle(1.05, 0.98),
    ) is False
