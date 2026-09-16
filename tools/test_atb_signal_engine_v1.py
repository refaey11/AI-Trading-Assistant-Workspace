import pandas as pd

from atb_signal_engine_v1 import indicators, signal_row


def frame(direction: str) -> pd.DataFrame:
    n = 260
    close = pd.Series(range(n), dtype=float) + 100
    if direction == "down":
        close = pd.Series(range(n, 0, -1), dtype=float) + 100
    return pd.DataFrame({"time": pd.date_range("2020-01-01", periods=n, freq="h"),
                         "open": close, "high": close + 0.5, "low": close - 0.5, "close": close})


def test_indicators_no_lookahead_columns():
    x = indicators(frame("up"))
    assert {"ema50", "ema200", "atr", "rsi", "prior_high", "prior_low", "atr_pctile"} <= set(x.columns)
    assert x.loc[200, "prior_high"] < x.loc[201, "close"]


def test_signal_is_bounded():
    x = indicators(frame("up"))
    result = signal_row(x.iloc[-1])
    assert result["signal"] in {"BUY", "SELL", "NO_TRADE"}
    assert result["model_version"] == "ATB_V1"
