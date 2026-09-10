from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import pandas as pd

TF_RULES = {'M5': '5min', 'M15': '15min', 'M30': '30min', 'H1': '1h', 'H4': '4h', 'D1': '1D'}


def parse_timestamp(values: pd.Series, dayfirst: bool = False) -> pd.Series:
    return pd.to_datetime(
        values.astype(str).str.strip(), errors='coerce', utc=True,
        format='mixed', dayfirst=dayfirst,
    )


def normalise_frame(raw: pd.DataFrame) -> pd.DataFrame:
    raw = raw.dropna(how='all').copy()
    if raw.empty:
        return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])

    first = ' '.join(str(x).strip().lower() for x in raw.iloc[0].tolist())
    if any(token in first for token in ('date', 'datetime', '<date>', '<datetime>', 'time')):
        raw = raw.iloc[1:].copy()
    if raw.empty:
        return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])

    candidates: list[tuple[pd.Series, pd.DataFrame, str]] = []
    # Combined datetime first: datetime,open,high,low,close[,volume]
    if raw.shape[1] >= 5:
        ts = parse_timestamp(raw.iloc[:, 0])
        vals = raw.iloc[:, 1:5].copy()
        candidates.append((ts, vals, 'datetime_ohlc'))
    # Separate date/time: date,time,open,high,low,close[,volume]
    if raw.shape[1] >= 6:
        ts = parse_timestamp(raw.iloc[:, 0].astype(str) + ' ' + raw.iloc[:, 1].astype(str))
        vals = raw.iloc[:, 2:6].copy()
        candidates.append((ts, vals, 'date_time_ohlc'))
    # Some files have a combined timestamp plus an extra non-price column before OHLC.
    if raw.shape[1] >= 6:
        for start in range(1, min(raw.shape[1] - 3, 4)):
            ts = parse_timestamp(raw.iloc[:, 0])
            vals = raw.iloc[:, start:start + 4].copy()
            candidates.append((ts, vals, f'datetime_offset_{start}'))

    best = None
    best_score = -1
    for ts, vals, layout in candidates:
        if vals.shape[1] != 4:
            continue
        numeric = vals.apply(lambda col: pd.to_numeric(
            col.astype(str).str.strip().str.replace(',', '', regex=False), errors='coerce'))
        score = int(ts.notna().sum()) + int(numeric.notna().all(axis=1).sum())
        if score > best_score:
            best = (ts, numeric, layout)
            best_score = score

    if best is None:
        return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])

    timestamp, values, _layout = best
    values.columns = ['open', 'high', 'low', 'close']
    result = values.assign(timestamp=timestamp)[['timestamp', 'open', 'high', 'low', 'close']]
    result = result.dropna(subset=['timestamp', 'open', 'high', 'low', 'close'])
    return result


def load_m1(path: Path) -> tuple[pd.DataFrame, dict]:
    frames = []
    diagnostics = {
        'files': [], 'rows_read': 0, 'rows_valid': 0,
        'min_timestamp': None, 'max_timestamp': None, 'years': {}, 'layouts': {},
    }

    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist()
                 if name.lower().endswith(('.csv', '.txt', '.dat'))]
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

    result = (pd.concat(frames, ignore_index=True).sort_values('timestamp')
              .drop_duplicates('timestamp').set_index('timestamp'))
    diagnostics['min_timestamp'] = result.index.min().isoformat()
    diagnostics['max_timestamp'] = result.index.max().isoformat()
    diagnostics['years'] = {str(int(year)): int(count)
                            for year, count in result.index.year.value_counts().sort_index().items()}
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
        bars = (m1.resample(rule, label='right', closed='right')
                .agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
                .dropna())
        regime = bars['close'].diff().map(lambda value: 1.0 if value > 0 else (-1.0 if value < 0 else 0.0))
        out[f'{timeframe}_trend_regime'] = regime.reindex(out.index, method='ffill')

    fields = [f'{timeframe}_trend_regime' for timeframe in TF_RULES]
    out['mtf_trend_score'] = out[fields].sum(axis=1)
    out = out.reset_index().rename(columns={'index': 'timestamp'})
    out = out[(out['timestamp'].dt.year >= 2016) & (out['timestamp'].dt.year <= 2024)]
    out = out.dropna().reset_index(drop=True)

    report = {**diagnostics, 'derived_timeframes': list(TF_RULES),
              'imputation_applied': False, 'scaling_applied': False,
              'categorical_translation_applied': False,
              'warmup_policy': 'global continuous resample then drop incomplete rows',
              'output_rows': len(out), 'status': 'PASS' if not out.empty else 'FAIL'}
    Path(args.report).write_text(json.dumps(report, indent=2), encoding='utf-8')
    if out.empty:
        raise SystemExit('M1_SOURCE_NO_2016_2024_ROWS')
    Path(args.output).write_text(out.to_csv(index=False), encoding='utf-8')
    print('CANONICAL_MTF_FROM_M1_PASS', len(out))


if __name__ == '__main__':
    main()
