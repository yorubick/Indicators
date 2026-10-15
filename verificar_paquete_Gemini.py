"""QA de cobertura, deduplicación, incertidumbre y datos del paquete."""
import json,hashlib,math
from datetime import datetime
from analizar_C_fuente_vs_grafico import ROOT
from auditar_Gemini_v4 import independently_build112

def key(c):return c['dt'],int(datetime.fromisoformat(c['START'].replace('Z','+00:00')).timestamp()),int(datetime.fromisoformat(c['END'].replace('Z','+00:00')).timestamp())
def main():
    master=json.loads((ROOT/'master_all_C_cases.json').read_text());cases=master['cases'];bykey={key(c):c for c in cases}
    assert len(bykey)==len(cases) and len({c['id'] for c in cases})==len(cases)
    for c in cases:
        assert c['volume_complete'] and len(c['OHLC'])==len(c['OHLCV'])==c['bars']
        assert [r['time'] for r in c['OHLC']]==list(range(c['OHLC'][0]['time'],c['OHLC'][-1]['time']+1,c['dt']))
        assert datetime.fromisoformat(c['effective_START']).timestamp()==c['OHLC'][0]['time']
        assert datetime.fromisoformat(c['effective_END']).timestamp()==c['OHLC'][-1]['time']
        assert c['START_unix']<=c['OHLC'][0]['time']<=c['OHLC'][-1]['time']<=c['END_unix']
        for a,b in zip(c['OHLC'],c['OHLCV']):
            assert all(a[k]==b[k] for k in a)
            assert b['volume'] is not None and math.isfinite(b['volume']) and b['volume']>=0
            assert b['low']<=min(b['open'],b['close'])<=max(b['open'],b['close'])<=b['high']
        if c['C_Lite'] is None:assert c['C_Character_interval'] and c['C_measurement_kind']=='Character_unique_compatible_integer'
        else:assert abs(c['C']-c['C_Lite'])<1e-7
    base=independently_build112()
    for c in base:assert key(c) in bykey and abs(bykey[key(c)]['C']-c['C'])<1e-7
    extra=json.loads((ROOT/'Gemini_v4_auditoria.json').read_text())['outside112_matrix']['rows']+json.loads((ROOT/'Gemini_v4_barrido15_auditoria.json').read_text())['cases']
    assert len(extra)==9
    for c in extra:assert key(c) in bykey and abs(bykey[key(c)]['C']-c['C'])<1e-7
    double=json.loads((ROOT/'C_cruce_doble.json').read_text())['cases'];covered=[]
    for c in double:
        s=c['start'] if len(c['start'])>5 else c['start']+':00';e=c['end'] if len(c['end'])>5 else c['end']+':00'
        ck=(c['dt'],int(datetime.fromisoformat('2026-10-12T'+s+'+00:00').timestamp()),int(datetime.fromisoformat('2026-10-12T'+e+'+00:00').timestamp()))
        assert ck in bykey and abs(bykey[ck]['C']-c['C'])<1e-7,(ck,c['file'])
        covered.append(bykey[ck]['id'])
    sweep=json.loads((ROOT/'C_barrido_END_1855_1920_1924_15s.json').read_text())['cases'];assert len(sweep)==17
    for c in sweep:assert key(c) in bykey and abs(bykey[key(c)]['C_Lite']-c['C'])<1e-7
    for a,b in zip(sweep,sweep[1:]):assert a['OHLCV']==b['OHLCV'][:-1] and key(b)[2]-key(a)[2]==15
    tf=json.loads((ROOT/'C_test_timeframes_1900_1920.json').read_text())['cases'];assert {c['dt'] for c in tf}=={15,60,120}
    for c in tf:assert key(c) in bykey and abs(bykey[key(c)]['C_Lite']-c['C'])<1e-7
    index=[{k:c[k] for k in ['id','START','END','effective_START','effective_END','dt','bars','C','C_Lite','C_measurement_kind','volume_complete']} for c in cases]
    (ROOT/'master_all_C_cases_index.json').write_text(json.dumps(index,indent=2),encoding='utf-8')
    out={'status':'passed','total_cases':len(cases),'Lite_measured':master['Lite_measured_cases'],'Character_only':master['Character_only_cases'],
         'OHLCV_complete':len(cases),'original112_covered':len(base),'outside112_controls_covered':len(extra),'double_cross_controls_covered':len(covered),
         'continuous_END_positions':len(sweep),'timeframe_controls':len(tf),'master_sha256':hashlib.sha256((ROOT/'master_all_C_cases.json').read_bytes()).hexdigest(),
         'warning':'Coverage within known verified manifest; Character-only hasnullC_Lite. Auxiliaryreports retain alternativeconfigurations separately. Alllabels known; no blindvalidation claim.'}
    (ROOT/'PAQUETE_GEMINI_QA.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
