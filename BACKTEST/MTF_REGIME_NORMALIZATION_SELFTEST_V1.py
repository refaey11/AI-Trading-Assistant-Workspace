from __future__ import annotations

import pandas as pd
from pathlib import Path

# Import the real source module without executing its Dropbox download main().
from CIRCLECI_ACQUIRE_GOVERNED_SOURCES import _normalize_regime


def main() -> int:
    df = pd.DataFrame({
        "M5_trend_regime": ["BULL_TREND", "BEARISH", 0.0, "NEUTRAL"],
    })
    _normalize_regime(df, "M5_trend_regime", Path("preflight"))
    assert df["M5_trend_regime"].tolist() == [1.0, -1.0, 0.0, 0.0]
    assert df["M5_trend_regime_source"].tolist() == ["BULL_TREND", "BEARISH", "0.0", "NEUTRAL"]
    print("MTF_REGIME_NORMALIZATION_SELFTEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
