from __future__ import annotations
import argparse, json, zipfile
from pathlib import Path
import pandas as pd

TF_RULES = {'M5':'5min','M15':'15min','M30':'30min','H1':'1h','H4':'4h','D1':'1D'}

def load_m1(path: Path) -> pd.DataFrame:
    files=[]
    if path.suffix.lower()=='.zip':
        with zipfile.ZipFile(path) as z:
            names=[n for n in z.namelist() if n.lower().endswith(('.csv','.txt'))]
            if not names: raise SystemExit('M1_SOURCE_NO_CSV_IN_ZIP')
            for n in names:
                with z.open(n) as f:
                    files.append(pd.read_csv(f, sep=None, engine='python', header=None))
    else:
        files=[pd.read_csv(path, sep=None, engine='python', header=None)]
    raw=pd.concat(files, ignore_index=True)
    if raw.shape[1] < 5: raise SystemExit('M1_SOURCE_TOO_FEW_COLUMNS')
    raw=raw.iloc[:,:6]
    raw.columns=['date','time','open','high','low','close'] if raw.shape[1]==6 else ['date','time','open','high','low','close'][:raw.shape[1]]
    if 'close' not in raw: raise SystemExit('M1_SOURCE_MISSING_CLOSE')
    raw['timestamp']=pd.to_datetime(raw['date'].astype(str)+' '+raw['time'].astype(str), errors='coerce', utc=True)
    for c in ['open','high','low','close']: raw[c]=pd.to_numeric(raw[c], errors='coerce')
    raw=raw.dropna(subset=['timestamp','open','high','low','close']).sort_values('timestamp')
    raw=raw.drop_duplicates('timestamp')
    return raw.set_index('timestamp')[['open','high','low','close']]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',required=True); ap.add_argument('--report',required=True); a=ap.parse_args()
    m1=load_m1(Path(a.input)); frames=[]
    for tf, rule in TF_RULES.items():
        x=m1.resample(rule, label='right', closed='right').agg({'open':'first','high':'max','low':'min','close':'last'}).dropna()
        x[f'{tf}_trend_regime']=(x.close.diff().gt(0).astype(float))
        x=x.rename(columns={'close':f'{tf}_close'})
        frames.append(x[[f'{tf}_trend_regime']])
    out=pd.concat(frames,axis=1).dropna().reset_index().rename(columns={'index':'timestamp'})
    out['mtf_trend_score']=out[[f'{tf}_trend_regime' for tf in TF_RULES]].sum(axis=1)
    out=out[(out.timestamp.dt.year>=2016)&(out.timestamp.dt.year<=2024)]
    if out.empty: raise SystemExit('M1_SOURCE_NO_2016_2024_ROWS')
    Path(a.output).write_text(out.to_csv(index=False),encoding='utf-8')
    Path(a.report).write_text(json.dumps({'status':'PASS','source':'raw_M1','derived_timeframes':list(TF_RULES),'imputation_applied':False,'scaling_applied':False,'categorical_translation_applied':False,'warmup_policy':'drop_rows_without_all_six_timeframes_after_global_resample'},indent=2))
    print('CANONICAL_MTF_FROM_M1_PASS',len(out))
if __name__=='__main__': main()
