"""Contacto de una EMA con precios observables en la primera ruptura.

Usa precios posteriores aEND, no el objetivoEND de ensayos anteriores.
Contraste de residuos enCobservado: condición necesaria antes de buscar raíces.
"""
import json,sys,csv,itertools
from datetime import datetime,timezone
from analizar_C_fuente_vs_grafico import ROOT

FILES={
 '20261012_060000_062000_60s':['C_frontera_nueva_0600_21_c.csv','C_frontera_nueva_0600_21_d.csv'],
 '20261012_060100_062100_60s':['C_frontera_shift_0601_c.csv','C_frontera_shift_0601_d.csv'],
 '20261012_180000_184000_120s':['Lite_180000_184000_2m_a.csv','Lite_180000_184000_2m_b.csv'],
 '20261012_185800_191800_60s':['Lite_1858_191800_1m_a.csv','Lite_1858_191800_1m_b.csv'],
 '20261012_185900_191900_60s':['Lite_1859_191900_1m_a.csv','Lite_1859_191900_1m_b.csv'],
 '20261012_190000_190500_15s':['Lite_190000_190500_15s_a.csv','Lite_190000_190500_15s_b.csv'],
 '20261012_190000_192000_60s':['Lite_1900_1920_1m_a.csv','Lite_1900_1920_1m_b.csv'],
 **{f'20261012_190{i}00_192{i}00_60s':[f'Lite_190{i}_192{i}00_1m_a.csv',f'Lite_190{i}_192{i}00_1m_b.csv'] for i in range(1,5)}}
FACTORS={'Lane 3 A':24.,'Lane 3 B':89/3,'Lane 2 A':8.,'Lane 2 B':89/9,'Lane 1 A':72/27,'Lane 1 B':89/27}
TARGETS=['range_high','range_low','range_mid','END_close','break_open','break_high','break_low','break_close','break_hl2']
SPEC={'cases':'Eleven mastertraining cases n21; accepted CSV pairs explicitly listed.',
 'files':FILES,'event':'First close strictly outside inclusive rangeH/L afterEND; verify firstpublished sixLite curves matches event.',
 'model':'One of sixLite EMA periods factor*C/dt fitted to a fixedtarget price at firstbreak, using close orHL2 afterEND. Bull seedENDlow, bear seedENDhigh; process all postEND bars including break.',
 'factors':FACTORS,'targets':TARGETS,'sources':['close','hl2'],
 'gate':'Fixed configuration must give abs(EMA_at_observedC-target)<=1e-7 price for all11. Necessary exactcontact, no root optimization, ticksnap or per-case choice.',
 'scope':'108 exactcontact configurations. Not all postEND mechanisms, optimization objectives or other period scales. Known labels, no reservedvalidation. Close also independently reconstructs firstpublished values.'}

def read(name):
    with (ROOT/'manual'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))[:-1]

def main():
    p=ROOT/'C_contacto_ruptura21_preregistro.json'
    if '--spec' in sys.argv:p.write_text(json.dumps(SPEC,indent=2),encoding='utf-8');print('108 contactos registrados; sinvalidacion.');return
    assert json.loads(p.read_text())==SPEC
    cases=[c for c in json.loads((ROOT/'C_dataset_verificado.json').read_text())['cases'] if c['bars']==21 and c['split']=='training'];prepared=[]
    for c in cases:
        a,b=[read(f) for f in FILES[c['id']]];ad={int(r['time']):r for r in a};bd={int(r['time']):r for r in b}
        for row in c['OHLC']:
            assert all(float(bd[row['time']][k])==row[k] for k in ['open','high','low','close'])
        H=max(r['high'] for r in c['OHLC']);L=min(r['low'] for r in c['OHLC']);end=c['OHLC'][-1]
        post=sorted([r for t,r in bd.items() if t>end['time']],key=lambda r:int(r['time']))
        first=next(r for r in post if float(r['close'])>H or float(r['close'])<L);t=int(first['time'])
        sequence=[r for r in post if int(r['time'])<=t]
        assert [int(r['time']) for r in sequence]==list(range(end['time']+c['dt'],t+1,c['dt']))
        assert all(first[k] and ad[t][k]==first[k] for k in FACTORS)
        assert min(int(r['time']) for r in b if any(r[k] for k in FACTORS))==t
        seed=end['low'] if float(first['close'])>H else end['high']
        targets={'range_high':H,'range_low':L,'range_mid':(H+L)/2,'END_close':end['close'],
                 **{'break_'+k:float(first[k]) for k in ['open','high','low','close']},'break_hl2':(float(first['high'])+float(first['low']))/2}
        values={}
        for source,col in itertools.product(SPEC['sources'],FACTORS):
            alpha=2/(FACTORS[col]*c['C']/c['dt']+1);v=seed
            assert 0<alpha<=1
            for row in sequence:
                price=float(row['close']) if source=='close' else (float(row['high'])+float(row['low']))/2
                v+=alpha*(price-v)
            values[source,col]=v
        errors={k:abs(values['close',k]-float(first[k])) for k in FACTORS}
        assert max(errors.values())<1e-7,(c['id'],errors)
        prepared.append({'case':c,'event':t,'after_END_bars':len(sequence),'targets':targets,'values':values,'reconstruction_errors':errors})
    models=[]
    for source,col,target in itertools.product(SPEC['sources'],FACTORS,TARGETS):
        records=[{'id':r['case']['id'],'C':r['case']['C'],'residual':r['values'][source,col]-r['targets'][target]} for r in prepared]
        models.append({'source':source,'curve':col,'target':target,'exact_contacts':sum(abs(r['residual'])<=1e-7 for r in records),'cases':records})
    out={'spec':SPEC,'cases':[{'id':r['case']['id'],'C':r['case']['C'],'break_time':datetime.fromtimestamp(r['event'],timezone.utc).isoformat(),
                              'after_END_bars':r['after_END_bars'],'reconstruction_errors':r['reconstruction_errors']} for r in prepared],
         'models':models,'model_count':len(models),'survivors_all11':sum(m['exact_contacts']==11 for m in models),
         'best_contact_count':max(m['exact_contacts'] for m in models),'reserved_validation_used':False}
    (ROOT/'C_contacto_ruptura21_resultados.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ['spec','models']},indent=2))

if __name__=='__main__':main()
