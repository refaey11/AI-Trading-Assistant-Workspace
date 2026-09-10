from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import pandas as pd

TF_RULES = {'M5': '5min', 'M15': '15min', 'M30': '30min', 'H1': '1h', 'H4': '4h', 'D1': '1D'}


def parse_timestamp(date_col: pd.Series, time_col: pd.Series | None = None) -> pd.Series:
    if time_col is None:
        text = date_col.astype(str).str.strip()
    else:
        text = date_col.astype(str).str.strip() + ' ' + time_col.astype(str).str.strip()
    parsed = pd.to_datetime(text, errors='coerce', utc=True, format='mixed', dayfirst=False)
    missing = parsed.isna()
    if missing.any():
        parsed.loc[missing] = pd.to_datetime(
            text.loc[missing], errors='coerce', utc=True, format='mixed', dayfirst=True
        )
    return parsed


def normalise_frame(raw: pd.DataFrame) -> pd.DataFrame:
    raw = raw.dropna(how='all').copy()
    if raw.empty:
        return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])

    # Remove a possible header row regardless of capitalization or angle brackets.
    first = ' '.join(str(x).strip().lower() for x in raw.iloc[0].tolist())
    if any(token in first for token in ('date', 'datetime', '<date>', '<datetime>')):
        raw = raw.iloc[1:].copy()

    # Supported layouts:
    # 1) date,time,open,high,low,close[,volume]
    # 2) datetime,open,high,low,close[,volume]
    # 3) MT-style: date,time,open,high,low,close,volume,spread,...
    if raw.shape[1] >= 6:
        timestamp = parse_timestamp(raw.iloc[:, 0], raw.iloc[:, 1])
        values = raw.iloc[:, 2:6].copy()
    elif raw.shape[1] >= 5:
        timestamp = parse_timestamp(raw.iloc[:, 0])
        values = raw.iloc[:, 1:5].copy()
    else:
        return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])

    values.columns = ['open', 'high', 'low', 'close']
    for column in values.columns:
        values[column] = pd.to_numeric(
            values[column].astype(str).str.strip().str.replace(',', '', regex=False),
            errors='coerce',
        )

    result = values.assign(timestamp=timestamp)[['timestamp', 'open', 'high', 'low', 'close']]
    return result.dropna(subset=['timestamp', 'open', 'high', 'low', 'close'])


def load_m1(path: Path) -> tuple[pd.DataFrame, dict]:
    frames = []
    diagnostics = {
        'files': [],
        'rows_read': 0,
        'rows_valid': 0,
        'min_timestamp': None,
        'max_timestamp': None,
        'years': {},
        'layouts': {},
    }

    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if name.lower().endswith(('.csv', '.txt', '.dat'))]
        if not names:
            raise SystemExit('M1_SOURCE_NO_CSV_IN_ZIP')

        for name in names:
            with archive.open(name) as handle:
                raw = pd.read_csv(handle, sep=None, engine='python', header=None, on_bad_lines='skip')
            diagnostics['files'].append(name)
            diagnostics['rows_read'] += len(raw)
            diagnostics['layouts'][name] = int(raw.shape[1])
            valid = normalise_frame(raw)
            diagnostics['rows_valid'] += len(valid)
            if not valid.empty:
                frames.append(valid)

    if not frames:
        raise SystemExit('M1_SOURCE_NO_VALID_ROWS')

    result = (
        pd.concat(frames, ignore_index=True)
        .sort_values('timestamp')
        .drop_duplicates('timestamp')
        .set_index('timestamp')
    )
    diagnostics['min_timestamp'] = result.index.min().isoformat()
    diagnostics['max_timestamp'] = result.index.max().isoformat()
    diagnostics['years'] = {
        str(int(year)): int(count)
        for year, count in result.index.year.value_counts().sort_index().items()
    }
    return result, diagnostics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()

    m1, diagnostics = load_m1(Path(args.input))
    out = pd.DataFrame(index=m1.index)
    for timeframe, rule in TF_RULES.items():
        bars = (
            m1.resample(rule, label='right', closed='right')
            .agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
            .dropna()
        )
        regime = bars['close'].diff().map(lambda value: 1.0 if value > 0 else (-1.0 if value < 0 else 0.0))
        out[f'{timeframe}_trend_regime'] = regime.reindex(out.index, method='ffill')

    fields = [f'{timeframe}_trend_regime' for timeframe in TF_RULES]
    out['mtf_trend_score'] = out[fields].sum(axis=1)
    out = out.reset_index().rename(columns={'index': 'timestamp'})
    out = out[(out['timestamp'].dt.year >= 2016) & (out['timestamp'].dt.year <= 2024)]
    out = out.dropna().reset_index(drop=True)

    report = {
        **diagnostics,
        'derived_timeframes': list(TF_RULES),
        'imputation_applied': False,
        'scaling_applied': False,
        'categorical_translation_applied': False,
        'warmup_policy': 'global continuous resample then drop incomplete rows',
        'output_rows': len(out),
        'status': 'PASS' if not out.empty else 'FAIL',
    }
    Path(args.report).write_text(json.dumps(report, indent=2), encoding='utf-8')
    if out.empty:
        raise SystemExit('M1_SOURCE_NO_2016_2024_ROWS')
    Path(args.output).write_text(out.to_csv(index=False), encoding='utf-8')
    print('CANONICAL_MTF_FROM_M1_PASS', len(out))


if __name__ == '__main__':
    main()
