from pathlib import Path
import json, sys, pandas as pd
root=Path(sys.argv[1])
h1=next(root.glob('unpacked/h1/GBPUSD_H1_2016_2025_MASTER.csv'))
market=root/'source/market_state.csv'; nison=root/'source/nison.csv'
def tsset(p):
    d=pd.read_csv(p,usecols=['timestamp'],low_memory=False)
    return set(pd.to_datetime(d.timestamp,utc=True,errors='coerce',format='mixed').dropna())
h1s=tsset(h1); markets=tsset(market)
mur=[]
for p in sorted((root/'unpacked/murphy').rglob('*.csv')):
    try: c=set(pd.read_csv(p,nrows=0,low_memory=False).columns)
    except Exception: continue
    if {'timestamp','status','direction','source_rule_id'}.issubset(c): mur.append(p)
if not mur: raise SystemExit('BLOCKED_NO_CANONICAL_MURPHY_SOURCE')
murphy=next((p for p in mur if p.name=='MURPHY_2016_2024_FULL_EVIDENCE.csv'),mur[0])
md=pd.read_csv(murphy,usecols=['timestamp','status','direction','source_rule_id'],low_memory=False)
md.timestamp=pd.to_datetime(md.timestamp,utc=True,errors='coerce',format='mixed')
md.status=md.status.astype('string').str.upper().str.strip(); md.direction=md.direction.astype('string').str.upper().str.strip().replace({'BULLISH':'BUY','BEARISH':'SELL'})
mc=md[md.status.eq('PASS') & md.direction.isin({'BUY','SELL'})].groupby('timestamp').size(); ms=set(mc[mc.eq(1)].index)
cols=set(pd.read_csv(nison,nrows=0,low_memory=False).columns); rule='source_rule_id' if 'source_rule_id' in cols else ('rule_id' if 'rule_id' in cols else None)
if not rule: raise SystemExit('BLOCKED_NISON_RULE_ID_COLUMN')
nd=pd.read_csv(nison,usecols=['timestamp',rule],low_memory=False); nd.timestamp=pd.to_datetime(nd.timestamp,utc=True,errors='coerce',format='mixed'); nd[rule]=nd[rule].astype('string').str.strip()
exp={f'NISON_{i:04d}' for i in range(1,45)}; ns=[]
for t,g in nd.groupby('timestamp',sort=True):
    ids={x.strip() for v in g[rule].dropna() for x in str(v).split('|') if x.strip()}
    if len(g)==44 and ids==exp: ns.append(t)
need={'timestamp','mtf_trend_score','M5_trend_regime','M15_trend_regime','M30_trend_regime','H1_trend_regime','H4_trend_regime','D1_trend_regime'}
mtf=next((p for p in sorted((root/'unpacked/mtf').rglob('*.csv')) if need.issubset(set(pd.read_csv(p,nrows=0,low_memory=False).columns))),None)
if mtf is None: raise SystemExit('BLOCKED_NO_SIX_TF_MTF_SOURCE')
mtfs=tsset(mtf)
sim_files=[p for p in sorted((root/'unpacked/similarity').rglob('*.json')) if 'SIMILAR' in p.name.upper() or 'CONTEXT' in p.name.upper()]
vals=[]
if sim_files:
    data=json.loads(sim_files[0].read_text(encoding='utf-8'))
    for item in data if isinstance(data,list) else []:
        for r in item.get('similar_contexts',[]) if isinstance(item,dict) else []:
            if isinstance(r,dict) and r.get('timestamp'):
                try: vals.append(pd.Timestamp(r['timestamp'],tz='UTC'))
                except Exception: pass
if not vals: raise SystemExit('BLOCKED_NO_SIMILARITY_HISTORICAL_TIMESTAMP')
common=sorted(h1s & markets & mtfs & ms & set(ns)); common=[t for t in common if 2016<=t.year<=2024 and t>=min(vals)]
if not common: raise SystemExit('BLOCKED_NO_SOURCE_BACKED_EVENT_MEETS_ALL_GATES')
value=common[0].isoformat().replace('+00:00','Z'); print('DISCOVERED_EVENT_TS',value); Path('/tmp/gate3c_event_ts').write_text(value)
