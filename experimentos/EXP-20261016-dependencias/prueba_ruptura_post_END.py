import json,sys,math,statistics
sys.path.insert(0,'tools')
from evaluador_C import redondeo_pine
tv=json.load(open('experimentos/EXP-20261016-dependencias/NQ1_1m_2026-10-12_13.json'))['bars']
idx={t:i for i,t in enumerate(tv['t'])}
m=json.load(open('master_all_C_cases.json'))
rows=[]
for c in m['cases']:
    if c['C_measurement_kind']!='Lite_decimal_verified' or c['source_seconds']!=60: continue
    n=c['bars']; C=c['C_Lite']; e=idx[c['END_unix']]; s=idx[c['START_unix']]
    H=tv['h'][e]; L=tv['l'][e]
    def first(cond):
        for j in range(e+1,min(e+240,len(tv['t']))):
            if cond(j): return j
    bh=first(lambda j: tv['h'][j]>H); bl=first(lambda j: tv['l'][j]<L)
    ch=first(lambda j: tv['c'][j]>H); cl=first(lambda j: tv['c'][j]<L)
    rows.append(dict(id=c['id'],n=n,C=C,s=s,e=e,bh=bh,bl=bl,ch=ch,cl=cl))
long=[r for r in rows if r['n']>=21]; short=[r for r in rows if r['n']<21]
print('casos 1m:',len(rows),'largos',len(long))
def test(name,f,rs):
    ok=0; errs=[]
    for r in rs:
        p=f(r)
        if p is None: continue
        if r['n']>=21: hit=redondeo_pine(p)==round(r['C'])
        else: hit=abs(p-r['C'])<1e-6
        ok+=hit; errs.append(abs(p-r['C']))
    print(f"{name:<55} {ok}/{len(rs)}  mediana err {statistics.median(errs):.2f}")
for key,lab in [('bh','primera H>H_END'),('ch','primer cierre>H_END'),('bl','primera L<L_END'),('cl','primer cierre<L_END')]:
    def brk(r,key=key): return r[key]
    test(f'largo round((t_ruptura-START)/18.3) [{lab}]', lambda r,k=key: None if r[k] is None else (r[k]-r['s'])*60/18.3, long)
    test(f'largo corto-ley con n hasta ruptura [{lab}]', lambda r,k=key: None if r[k] is None else (r[k]-r['s']+1)*60*10/183, long)
    test(f'largo corto-ley n hasta ruptura-1 [{lab}]', lambda r,k=key: None if r[k] is None else (r[k]-r['s'])*60*10/183, long)
# show a sweep
for r in sorted([r for r in rows if r['id'].startswith(('20261012_190400','20261012_190000_19','20261012_060000'))],key=lambda r:(r['id'][:15],r['n'])):
    print(r['id'],'n',r['n'],'C',round(r['C'],2),'k_bh',None if r['bh'] is None else r['bh']-r['e'],'k_ch',None if r['ch'] is None else r['ch']-r['e'],'k_bl',None if r['bl'] is None else r['bl']-r['e'])
