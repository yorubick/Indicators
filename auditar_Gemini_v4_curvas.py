"""Emulación offline del motor de curvas v4 con velas cerradas nativas.

No compila/instala Pine ni demuestra semántica intravela/multifuente.
"""
import json,math,csv
from analizar_C_fuente_vs_grafico import ROOT
from auditar_Gemini_v4 import extract_function,translate_pine_engine
from auditar_Gemini_hibrido import BASE

def read(name):
    with (ROOT/'manual'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))[:-1]

def simulate(case,C):
    prov=case['provenance'];prefix=prov['id'];a,b=[read(f'{prefix}_{s}.csv') for s in prov['pair']]
    ad={int(r['time']):r for r in a};bd={int(r['time']):r for r in b}
    for row in case['OHLC']:assert all(float(bd[row['time']][k])==row[k] for k in ['open','high','low','close'])
    assert all(ad[t][k]==bd[t][k] for t in set(ad)&set(bd) for k in BASE)
    end=case['OHLC'][-1];H=max(r['high'] for r in case['OHLC']);L=min(r['low'] for r in case['OHLC']);dt=case['dt']
    alpha={k:2/((factor*C/dt if k.startswith('Lane') else max(1,math.floor(factor*C/dt+.5)))+1) for k,factor in BASE.items()}
    bull={k:end['low'] for k in BASE};bear={k:end['high'] for k in BASE};side=None
    stats={f:{'compared_values':0,'max_error':0.,'visibility_mismatches':0,'first_visible_values':{},'first_mismatch':None,'max_error_witness':None,
              'before_first_gap_values':0,'before_first_gap_max_error':0.,'first_gap_time':None} for f in ['Lite','Character']}
    previous=end['time'];gap_seen=False
    for t,r in sorted(bd.items()):
        if t<=end['time']:continue
        if t>end['time']+10800:break
        if t-previous!=dt:
            if not gap_seen:
                for st in stats.values():st['first_gap_time']=t
            gap_seen=True
        previous=t
        for k in BASE:
            bull[k]+=alpha[k]*(float(r['close'])-bull[k]);bear[k]+=alpha[k]*(float(r['close'])-bear[k])
        if side is None:
            if float(r['close'])>H:side='bull'
            elif float(r['close'])<L:side='bear'
        for k in BASE:
            st=stats['Lite' if k.startswith('Lane') else 'Character'];visible=side is not None
            st['visibility_mismatches']+=bool(r[k])!=visible
            if r[k] and visible:
                value=(bull if side=='bull' else bear)[k];error=abs(value-float(r[k]));st['compared_values']+=1
                witness={'time':t,'column':k,'predicted':value,'observed':float(r[k]),'error':error,
                         'other_seed_branch_error':abs((bear if side=='bull' else bull)[k]-float(r[k])),
                         'Bull_delivery_active':r.get('Bull delivery active'),'Bear_delivery_active':r.get('Bear delivery active')}
                if error>1e-7 and st['first_mismatch'] is None:st['first_mismatch']=witness
                if error>st['max_error']:st['max_error']=error;st['max_error_witness']=witness
                if not gap_seen:
                    st['before_first_gap_values']+=1;st['before_first_gap_max_error']=max(st['before_first_gap_max_error'],error)
                if k not in st['first_visible_values']:st['first_visible_values'][k]={'time':t,'predicted':value,'observed':float(r[k]),'error':error}
    return stats

def main():
    text=(ROOT/'pine/Gemini_v4_recibido.pine').read_text(encoding='utf-8-sig')
    for token in ['s_bull_l3a := end_low','s_bear_l3a := end_high','if close > rng_high','else if close < rng_low','if time > end_time','89.0 / (1.0/3.0)']:
        assert token in text
    pine=translate_pine_engine();cases=json.loads((ROOT/'C_matriz_frontera15s.json').read_text())['cases'];results=[]
    for c in cases:
        prediction=pine(c)
        results.append({'START':c['START'],'END':c['END'],'C_observed':c['C'],'C_auto_v4':prediction,
                        'manual_supplied_C':simulate(c,c['C']),'automatic_C':simulate(c,prediction)})
    summary={}
    for mode in ['manual_supplied_C','automatic_C']:
        summary[mode]={f:{'compared_values':sum(c[mode][f]['compared_values'] for c in results),
                          'max_error':max(c[mode][f]['max_error'] for c in results),
                          'before_first_gap_values':sum(c[mode][f]['before_first_gap_values'] for c in results),
                          'before_first_gap_max_error':max(c[mode][f]['before_first_gap_max_error'] for c in results),
                          'visibility_mismatches':sum(c[mode][f]['visibility_mismatches'] for c in results)} for f in ['Lite','Character']}
    out={'scope':'Offline closed-bar emulation of currentPine engine, nine native15s matrix cases,180min horizon. Not compilation, livePine test, fullsource support or universal curve equivalence.',
         'summary':summary,'cases':results}
    (ROOT/'Gemini_v4_curvas_auditoria.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
    live=next(c for c in results if c['START'].endswith('19:03:15+00:00') and c['END'].endswith('19:23:30+00:00'))
    print(json.dumps({'reported_live_case_first_values_reproduced_offline':live['automatic_C']['Lite']['first_visible_values']},indent=2))

if __name__=='__main__':main()
