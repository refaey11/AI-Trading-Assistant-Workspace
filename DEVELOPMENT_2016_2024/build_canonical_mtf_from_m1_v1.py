from __future__ import annotations
import argparse, json, zipfile
from pathlib import Path
import pandas as pd

TF_RULES = {'M5':'5min','M15':'15min','M30':'30min','H1':'1h','H4':'4h','D1':'1D'}

def load_m1(path: Path) -> pd.DataFrame:
    frames=[]
    with zipfile.ZipFile(path) as z:
        names=[n for n in z.namelist() if n.lower().endswith(('.csv','.txt'))]
        if not names: raise SystemExit('M1_SOURCE_NO_CSV_IN_ZIP')
        for name in names:
            with z.open(name) as fh: raw=pd.read_csv(fh, sep=None, engine='python', header=None)
            if raw.shape[1] < 6: continue
            raw=raw.iloc[:,:6]; raw.columns=['date','time','open','high','low','close']
            if str(raw.iloc[0,0]).lower() in {'date','<date>'}: raw=raw.iloc[1:]
            raw['timestamp']=pd.to_datetime(raw['date'].astype(str)+' '+raw['time'].astype(str), errors='coerce', utc=True)
            for c in ['open','high','low','close']: raw[c]=pd.to_numeric(raw[c], errors='coerce')
            frames.append(raw.dropna(subset=['timestamp','open','high','low','close'])[['timestamp','open','high','low','close']])
    if not frames: raise SystemExit('M1_SOURCE_NO_VALID_ROWS')
    return pd.concat(frames, ignore_index=True).sort_values('timestamp').drop_duplicates('timestamp').set_index('timestamp')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',required=True); ap.add_argument('--report',required=True); a=ap.parse_args()
    m1=load_m1(Path(a.input)); out=pd.DataFrame(index=m1.index)
    for tf, rule in TF_RULES.items():
        bars=m1.resample(rule, label='right', closed='right').agg({'open':'first','high':'max','low':'min','close':'last'}).dropna()
        regime=bars.close.diff().map(lambda x: 1.0 if x>0 else (-1.0 if x<0 else 0.0))
        out[f'{tf}_trend_regime']=regime.reindex(out.index, method='ffill')
    fields=[f'{tf}_trend_regime' for tf in TF_RULES]
    out['mtf_trend_score']=out[fields].sum(axis=1)
    out=out.reset_index().rename(columns={'index':'timestamp'})
    out=out[(out.timestamp.dt.year>=2016)&(out.timestamp.dt.year<=2024)].dropna().reset_index(drop=True)
    if out.empty: raise SystemExit('M1_SOURCE_NO_2016_2024_ROWS')
    Path(a.output).write_text(out.to_csv(index=False),encoding='utf-8')
    Path(a.report).write_text(json.dumps({'status':'PASS','source':'raw_M1','derived_timeframes':list(TF_RULES),'imputation_applied':False,'scaling_applied':False,'categorical_translation_applied':False,'warmup_policy':'global_continuous_resample_then_drop_incomplete_rows'},indent=2),encoding='utf-8')
    print('CANONICAL_MTF_FROM_M1_PASS',len(out))
if __name__=='__main__': main()
