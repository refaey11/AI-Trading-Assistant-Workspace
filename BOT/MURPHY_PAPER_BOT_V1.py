from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

def load(path, required):
    d=pd.read_csv(path,low_memory=False); miss=sorted(required-set(d.columns))
    if miss: raise ValueError(f'{path}: missing {miss}')
    d['timestamp']=pd.to_datetime(d['timestamp'],utc=True,errors='coerce')
    if d.timestamp.isna().any(): raise ValueError(f'{path}: bad timestamps')
    return d.sort_values('timestamp').reset_index(drop=True)

def atr20(b):
    prev=b.close.shift(1)
    tr=pd.concat([(b.high-b.low),(b.high-prev).abs(),(b.low-prev).abs()],axis=1).max(axis=1)
    return tr.rolling(20,min_periods=20).mean()

def outcome(b,i,side,entry,atr,rr=2.0,stop_mult=.75,max_bars=48):
    risk=atr*stop_mult; sl=entry-risk if side=='BUY' else entry+risk; tp=entry+risk*rr if side=='BUY' else entry-risk*rr
    end=min(len(b),i+1+max_bars)
    for j in range(i+1,end):
        x=b.iloc[j]; h=float(x.high); l=float(x.low)
        hit_sl=l<=sl if side=='BUY' else h>=sl; hit_tp=h>=tp if side=='BUY' else l<=tp
        if hit_sl and hit_tp: return ('AMBIGUOUS',None,x.timestamp,sl,tp)
        if hit_tp: return ('TP',rr,x.timestamp,sl,tp)
        if hit_sl: return ('SL',-1.0,x.timestamp,sl,tp)
    return ('TIME_EXIT',None,b.iloc[end-1].timestamp if end>i+1 else None,sl,tp)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--bars',type=Path,required=True); p.add_argument('--signals',type=Path,required=True); p.add_argument('--out-dir',type=Path,required=True); p.add_argument('--pair',required=True)
    a=p.parse_args(); b=load(a.bars,{'timestamp','open','high','low','close'}); s=load(a.signals,{'timestamp','status','direction','source_rule_id'})
    s=s[(s.timestamp.dt.year==2025)&s.status.astype(str).str.upper().eq('PASS')&s.direction.astype(str).str.upper().isin(['BULLISH','BEARISH'])].copy()
    b['atr20']=atr20(b); rows=[]
    for _,r in s.iterrows():
        ix=b.index[b.timestamp==r.timestamp]
        if len(ix)==0: continue
        i=int(ix[0]);
        if i+1>=len(b) or pd.isna(b.iloc[i].atr20): continue
        side='BUY' if str(r.direction).upper()=='BULLISH' else 'SELL'; entry=float(b.iloc[i+1].open); res=outcome(b,i+1,side,entry,float(b.iloc[i].atr20))
        rows.append({'pair':a.pair,'signal_timestamp':r.timestamp,'source_rule_id':r.source_rule_id,'direction':r.direction,'entry_timestamp':b.iloc[i+1].timestamp,'entry':entry,'atr20':float(b.iloc[i].atr20),'outcome':res[0],'r_multiple':res[1],'exit_timestamp':res[2],'stop_loss':res[3],'take_profit':res[4]})
    a.out_dir.mkdir(parents=True,exist_ok=True); d=pd.DataFrame(rows); d.to_csv(a.out_dir/'murphy_paper_trades_2025.csv',index=False)
    v=d[d.r_multiple.notna()] if not d.empty else d; wins=int((v.r_multiple>0).sum()) if not v.empty else 0; losses=int((v.r_multiple<0).sum()) if not v.empty else 0; gw=float(v.loc[v.r_multiple>0,'r_multiple'].sum()) if not v.empty else 0.; gl=float(-v.loc[v.r_multiple<0,'r_multiple'].sum()) if not v.empty else 0.; eq=v.r_multiple.cumsum() if not v.empty else pd.Series(dtype=float)
    m={'pair':a.pair,'window':'2025-only','signals':int(len(s)),'trades':int(len(d)),'resolved':int(len(v)),'wins':wins,'losses':losses,'win_rate':wins/len(v) if len(v) else None,'profit_factor':gw/gl if gl else None,'expectancy_R':float(v.r_multiple.mean()) if len(v) else None,'total_R':float(v.r_multiple.sum()) if len(v) else 0.,'max_drawdown_R':float((eq-eq.cummax()).min()) if not eq.empty else 0.,'rr':2.0,'atr_stop':0.75,'future_data_used':False,'tuning_applied':False,'live_execution':False}
    (a.out_dir/'metrics.json').write_text(json.dumps(m,indent=2,default=str),encoding='utf-8'); print(json.dumps(m,indent=2))
if __name__=='__main__': main()
