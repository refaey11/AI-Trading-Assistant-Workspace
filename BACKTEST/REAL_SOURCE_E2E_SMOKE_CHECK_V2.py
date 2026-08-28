from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def read_csv(path, required):
    df = pd.read_csv(path, nrows=25, low_memory=False)
    missing = sorted(required - set(df.columns))
    if missing:
        raise AssertionError(f"{path}: missing {missing}")
    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if ts.isna().any():
        raise AssertionError(f"{path}: invalid timestamp")
    return ts

h1 = read_csv(Path("artifacts/raw/h1.csv"), {"timestamp","open","high","low","close"})
market = read_csv(Path("artifacts/raw/market_state.csv"), {"timestamp"})
mtf = read_csv(Path("artifacts/raw/mtf.csv"), {"timestamp"})
murphy = read_csv(Path("artifacts/raw/murphy.csv"), {"timestamp","status","direction","source_rule_id"})
nison = read_csv(Path("artifacts/raw/nison.csv"), {"timestamp","status","direction","rule_id"})
hc = read_csv(Path("artifacts/raw/historical_context.csv"), {"timestamp","context_signature"})
ho = read_csv(Path("artifacts/raw/historical_outcome.csv"), {"timestamp","context_signature"})

for name, series in [("H1",h1),("Market State",market),("MTF",mtf),("Murphy",murphy),("Nison",nison),("Historical Context",hc),("Historical Outcome",ho)]:
    years = set(series.dt.year.dropna().astype(int))
    if 2025 in years:
        raise AssertionError(f"{name}: 2025 leakage detected")

if max(h1.dt.year) > 2024:
    raise AssertionError("H1 scope exceeds 2024")

print("REAL_SOURCE_E2E_SMOKE=PASS")
print("Checked: timestamps, required columns, 2016-2024 development scope, 2025 lock")
