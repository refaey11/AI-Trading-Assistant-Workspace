from __future__ import annotations
import argparse, json, zipfile
from pathlib import Path
import pandas as pd

TF_RULES = {'M5':'5min','M15':'15min','M30':'30min','H1':'1h','H4':'4h','D1':'1D'}

def parse_timestamp(date_col: pd.Series, time_col: pd.Series) -> pd.Series:
    text = date_col.astype(str).str.strip() + ' ' + time_col.astype(str).str.strip()
    parsed = pd.to_datetime(text, errors='coerce', utc=True, format='mixed', dayfirst=False)
    missing = parsed.isna()
    if missing.any():
        parsed.loc[missing] = pd.to_datetime(text.loc[missing], errors='coerce', utc=True, format='mixed', dayfirst=True)
    return parsed

def load_m1(path: Path) -> tuple[pd.DataFrame, dict]:
    frames = []
    diagnostics = {'files': [], 'rows_read': 0, 'rows_valid': 0, 'min_timestamp': None, 'max_timestamp': None, 'years': {}}
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(('.csv', '.txt'))]
        if not names: raise SystemExit('M1_SOURCE_NO_CSV_IN_ZIP')
        for name in names:
            with z.open(name) as fh:
                raw = pd.read_csv(fh, sep=None, engine='python', header=None)
            diagnostics['files'].append(name); diagnostics['rows_read'] += len(raw)
            if raw.shape[1] < 6: continue
            raw = raw.iloc[:, :6]; raw.columns = ['date','time','open','high','low','close']
            if str(raw.iloc[0, 0]).strip().lower() in {'date','<date>','datetime','<datetime>'}: raw = raw.iloc[1:]
            raw['timestamp'] = parse_timestamp(raw['date'], raw['time'])
            for c in ['open','high','low','close']:
                raw[c] = pd.to_numeric(raw[c].astype(str).str.replace(',', '', regex=False), errors='coerce')
            valid = raw.dropna(subset=['timestamp','open','high','low','close'])[['timestamp','open','high','low','close']]
            diagnostics['rows_valid'] += len(valid); frames.append(valid)
    if not frames: raise SystemExit('M1_SOURCE_NO_VALID_ROWS')
    result = pd.concat(frames, ignore_index=True).sort_values('timestamp').drop_duplicates('timestamp').set_index('timestamp')
    if not result.empty:
        diagnostics['min_timestamp'] = result.index.min().isoformat(); diagnostics['max_timestamp'] = result.index.max().isoformat()
        diagnostics['years'] = {str(int(k)): int(v) for k,v in result.index.year.value_counts().sort_index().items()}
    return result, diagnostics

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--input', required=True); ap.add_argument('--output', required=True); ap.add_argument('--report', required=True); a = ap.parse_args()
    m1, diagnostics = load_m1(Path(a.input)); out = pd.DataFrame(index=m1.index)
    for tf, rule in TF_RULES.items():
        bars = m1.resample(rule, label='right', closed='right').agg({'open':'first','high':'max','low':'min','close':'last'}).dropna()
        regime = bars.close.diff().map(lambda x: 1.0 if x > 0 else (-1.0 if x < 0 else 0.0))
        out[f'{tf}_trend_regime'] = regime.reindex(out.index, method='ffill')
    fields = [f'{tf}_trend_regime' for tf in TF_RULES]; out['mtf_trend_score'] = out[fields].sum(axis=1)
    out = out.reset_index().rename(columns={'index':'timestamp'}); out = out[(out.timestamp.dt.year >= 2016) & (out.timestamp.dt.year <= 2024)].dropna().reset_index(drop=True)
    report = {**diagnostics, 'derived_timeframes': list(TF_RULES), 'imputation_applied': False, 'scaling_applied': False, 'categorical_translation_applied': False, 'warmup_policy': 'global continuous resample then drop incomplete rows', 'output_rows': len(out), 'status': 'PASS' if not out.empty else 'FAIL'}
    Path(a.report).write_text(json.dumps(report, indent=2), encoding='utf-8')
    if out.empty: raise SystemExit('M1_SOURCE_NO_2016_2024_ROWS')
    Path(a.output).write_text(out.to_csv(index=False), encoding='utf-8'); print('CANONICAL_MTF_FROM_M1_PASS', len(out))

if __name__ == '__main__': main()
