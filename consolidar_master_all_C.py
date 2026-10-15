"""Unifica observaciones verificadas, no predicciones ni C sintéticos.

Conserva procedencia y distingue C medido enLite de entero compatibleCT.
Volumen se une por timestamp/fuente conOHLCidéntico; agregación solo hacia arriba.
"""
import json,csv,statistics,hashlib,re
from pathlib import Path
from datetime import datetime,timezone
from analizar_C_fuente_vs_grafico import ROOT,fit_lite
from obtener_C import recover
from auditar_Gemini_v4 import independently_build112

def iso(t):return datetime.fromtimestamp(t,timezone.utc).isoformat()
def timestamp(s,default_date='2026-10-12'):
    if isinstance(s,int):return s
    if 'T' not in s:
        if len(s)==5:s+=':00'
        s=default_date+'T'+s+'+00:00'
    return int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
def read_path(path):
    p=Path(str(path).replace('\\\\','\\'))
    if not p.is_absolute():p=ROOT/p
    with p.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))[:-1]
    assert rows
    return p,{int(r['time']):r for r in rows}
def ohlc(rows):return [{'time':int(r['time']),**{k:float(r[k]) for k in ['open','high','low','close']}} for r in rows]

def main():
    unique={};excluded=[];refs=0;input_hashes={}
    def add(rows,dt,C,report,detail=None,lite=None,interval=None,split=None,requested_anchors=None):
        nonlocal refs
        rows=ohlc(rows);rows.sort(key=lambda r:r['time']);assert len(rows)>=2
        assert [r['time'] for r in rows]==list(range(rows[0]['time'],rows[-1]['time']+1,dt))
        requested_anchors=requested_anchors or (rows[0]['time'],rows[-1]['time'])
        key=(dt,*requested_anchors);refs+=1
        provenance={'report':report,'detail':detail,'C_Lite_measured':lite,'C_Character_interval':interval}
        input_hashes[report]=hashlib.sha256((ROOT/report).read_bytes()).hexdigest()
        if key in unique:
            c=unique[key];assert c['OHLC']==rows,('OHLC conflict',key,report)
            # Character compatibleinteger is not preciseLite; require interval if nonintegerLite exists.
            if interval and c['C_Lite'] is not None:assert interval['lower_inclusive']-1e-7<=c['C_Lite']<interval['upper_exclusive']+1e-7
            elif lite is not None and c['C_Lite'] is None and c['C_Character_interval']:
                iv=c['C_Character_interval'];assert iv['lower_inclusive']-1e-7<=lite<iv['upper_exclusive']+1e-7
            else:assert abs(c['C']-C)<1e-7,('C conflict',key,report,c['C'],C)
            if lite is not None:
                if c['C_Lite'] is not None:assert abs(c['C_Lite']-lite)<1e-7
                c['C_Lite']=float(lite);c['C']=float(lite)
            if interval:c['C_Character_interval']=interval
            if provenance not in c['provenance']:c['provenance'].append(provenance)
            return
        s,e=requested_anchors
        unique[key]={'id':f'{datetime.fromtimestamp(s,timezone.utc):%Y%m%d_%H%M%S}_{datetime.fromtimestamp(e,timezone.utc):%H%M%S}_{dt}s',
                     'symbol':'CME_MINI:NQ1!','session':'ETH','timezone':'UTC','contract_adjustment':False,'mode':'Manual','profile':'B',
                     'START':iso(s),'END':iso(e),'START_unix':s,'END_unix':e,'dt':dt,'source_seconds':dt,'chart_seconds':dt,'bars':len(rows),
                     'effective_START':iso(rows[0]['time']),'effective_END':iso(rows[-1]['time']),
                     'C':float(C),'C_Lite':float(lite) if lite is not None else None,'C_Character_interval':interval,
                     'OHLC':rows,'provenance':[provenance],'prior_split':split,'blind_or_prospective':False}
    # The112 observations independently assembled from originals, not external model labels.
    for c in independently_build112():
        add(c['OHLC'],c['dt'],c['C'],'Gemini_v4_auditoria.json',{'id':c['id'],'partition':c['partition'],'basis':'Independent original112 reconstruction; underlyingreports in prior audit'},lite=c['C'],split=c['partition'])
    for c in load('C_matriz_frontera15s.json')['cases']:add(c['OHLC'],c['dt'],c['C'],'C_matriz_frontera15s.json',c['provenance'],lite=c['C'])
    for c in load('C_sin_evento_resultados.json')['cases']:
        for m in c['measured']:add(c['OHLC'][:m['bars']],60,m['C'],'C_sin_evento_resultados.json',{'prefix':m['prefix'],'pair':m['pair']},lite=m['C'],interval=m['Character_interval'])
    for name in ['C_barrido_END_1855_1920_1924_15s.json','C_test_timeframes_1900_1920.json']:
        for c in load(name)['cases']:add(c['OHLC'],c['dt'],c['C'],name,{'source_files':c['source_files'],'verification':c['verification']},lite=c['C_Lite'],interval=c.get('C_Character_interval'))
    # All direct Lite comparison files: re-estimateC from native closedCSV.
    for p in sorted(ROOT.glob('Lite_*_comparacion.json')):
        try:
            r=load(p.name);s=timestamp(r['START_UTC']);e=timestamp(r['END_UTC']);dt=int(r['Lite_source_seconds']);chart=int(r['chart_seconds'])
            assert chart==dt,'non-native source/chart; separate aggregation study'
            path,data=read_path(r['file']);source_ohlc=None
            if not all(t in data for t in range(s,e+1,dt)):
                backup={15:'C_recorte1903_30_d.csv',60:'C_VOL_1m_b.csv',120:'C_pack_tf120_d.csv'}[dt]
                backup_path,backup_data=read_path(ROOT/'manual'/backup)
                assert all(data[t][k]==backup_data[t][k] for t in set(data)&set(backup_data) for k in ['open','high','low','close']), 'backupOHLC conflict'
                selected=[data[t] if t in data else backup_data[t] for t in range(s,e+1,dt)]
                source_ohlc=str(backup_path)
            else:selected=[data[t] for t in range(s,e+1,dt)]
            fits=fit_lite(data,dt,dt);Cs=[v['C'] for v in fits.values()];C=sum(Cs)/6
            assert max(Cs)-min(Cs)<1e-7 and max(v['rmse'] for v in fits.values())<1e-8
            iv=recover(path)['C_seconds_interval'];assert iv['lower_inclusive']-1e-7<=C<iv['upper_exclusive']+1e-7,'CT/Lite mismatch'
            add(selected,dt,C,p.name,{'file':str(path),'reestimated_sixLite':True,'OHLC_completed_from':source_ohlc},lite=C,interval=iv)
        except (Exception,SystemExit) as ex:excluded.append({'report':p.name,'reason':str(ex),'exception':type(ex).__name__})
    # Historical selection descriptors, including inputs to the old double-cross test.
    historical=['C_cruce_doble.json','C_sensibilidad_inicio.json','C_sensibilidad_15s.json','C_barrido_ampliado.json','C_END_barrido.json','C_bajistas.json','C_limites_y_mecha.json','C_limite_segundo.json']
    for name in historical:
        report=load(name)
        for idx,c in enumerate(report.get('cases',[])+report.get('END_controls',[])):
            try:
                ex=c.get('extraction',{});file=c.get('file',ex.get('file'));assert file,'noCSV'
                dt=int(c.get('dt',c.get('source_seconds',ex.get('source_seconds',report.get('source_seconds',15)))))
                ss=next((c[k] for k in ['START_UTC','START','start','requested_START_UTC'] if k in c),None)
                ee=next((c[k] for k in ['END_UTC','END','end','requested_END_UTC'] if k in c),None)
                ss=ss or report.get('START_UTC') or ('18:55:00' if name=='C_END_barrido.json' else None)
                ee=ee or report.get('END_UTC') or ('19:20:00' if name in ['C_sensibilidad_inicio.json','C_limite_segundo.json'] else None)
                assert ss and ee,'missing anchor timestamps'
                s=timestamp(ss);e=timestamp(ee)
                es=c.get('first_source_open_UTC',c.get('effective_first_source_bar_UTC'))
                eeff=c.get('last_source_open_UTC')
                effective_start=timestamp(es) if es else s
                effective_end=timestamp(eeff) if eeff else e
                assert effective_start%dt==0 and effective_end%dt==0,'subbar anchors require explicit source-open metadata'
                path,data=read_path(file);times=sorted(data);spacing=int(statistics.median(b-a for a,b in zip(times,times[1:])));assert spacing==dt,'export/source resolution mismatch'
                selected=[data[t] for t in range(effective_start,effective_end+1,dt)]
                iv=recover(path)['C_seconds_interval'];ints=recover(path)['compatible_integer_C_seconds'];assert len(ints)==1,'no unique compatibleintegerC'
                C=ints[0]
                if 'C' in c:assert abs(C-c['C'])<1e-7,'statedC mismatch'
                add(selected,dt,C,name,{'index':idx,'file':str(path),'C_precision':'Unique compatible CTinteger; Lite null unless separately measured'},interval=iv,requested_anchors=(s,e))
            except (Exception,SystemExit) as er:excluded.append({'report':name,'index':idx,'reason':str(er),'exception':type(er).__name__})
    # Native aggregation controls include30s; retain requested and effective anchors.
    for group in load('C_agregacion.json')['ranges']:
        for c in group['cases']:
            try:
                dt=c['source_seconds'];ex=c['extraction'];path,data=read_path(ex['file'])
                start=timestamp(c['first_source_open']);end=timestamp(c['last_source_open'])
                selected=[data[t] for t in range(start,end+1,dt)]
                actual=recover(path);iv=actual['C_seconds_interval'];ints=actual['compatible_integer_C_seconds'];assert len(ints)==1
                add(selected,dt,ints[0],'C_agregacion.json',{'file':str(path),'coverage':group.get('actual_source_coverage_UTC')},interval=iv,
                    requested_anchors=(timestamp(group['requested_START_UTC']),timestamp(group['requested_END_UTC'])))
            except (Exception,SystemExit) as er:excluded.append({'report':'C_agregacion.json','source_seconds':c.get('source_seconds'),'reason':str(er),'exception':type(er).__name__})
    # Join observed volume. Never substitute0 or disaggregate1m into15s.
    volume_sources={60:['C_VOL_1m_a.csv','C_VOL_1m_b.csv'],15:['C_recorte1903_30_c.csv','C_recorte1903_30_d.csv'],120:['C_pack_tf120_c.csv','C_pack_tf120_d.csv']}
    volumes={}
    for dt,names in volume_sources.items():
        ap,a=read_path(ROOT/'manual'/names[0]);bp,b=read_path(ROOT/'manual'/names[1]);joined={}
        for t in set(a)&set(b):
            if not b[t].get('Volume'):continue
            assert all(a[t][k]==b[t][k] for k in ['open','high','low','close','Volume']),('volume export conflict',dt,t)
            joined[t]={**ohlc([b[t]])[0],'volume':float(b[t]['Volume'])}
        volumes[dt]=(joined,[str(ap),str(bp)])
    def volume_for(r,dt):
        index,files=volumes.get(dt,({},[]));v=index.get(r['time'])
        if v and all(v[k]==r[k] for k in ['open','high','low','close']):return v['volume'],{'kind':'native_verified_pair','files':files}
        if dt in [30,120]:
            lower_dt=15 if dt==30 else 60
            idx,files=volumes[lower_dt];parts=[idx.get(t) for t in range(r['time'],r['time']+dt,lower_dt)]
            if all(parts):
                agg={'open':parts[0]['open'],'high':max(x['high'] for x in parts),'low':min(x['low'] for x in parts),'close':parts[-1]['close']}
                if all(agg[k]==r[k] for k in agg):return sum(x['volume'] for x in parts),{'kind':f'sum_native{lower_dt}s_bars_exact_{dt}s_OHLC','files':files}
        return None,{'kind':'missing_or_OHLC_mismatch'}
    cases=[]
    for c in sorted(unique.values(),key=lambda c:(c['START'],c['dt'],c['END'])):
        rows=[];provs=[]
        for r in c['OHLC']:
            v,proof=volume_for(r,c['dt']);rows.append({**r,'volume':v});provs.append(proof)
        c['OHLCV']=rows;c['volume_complete']=all(r['volume'] is not None for r in rows)
        c['volume_provenance']=list({json.dumps(p,sort_keys=True):p for p in provs}.values())
        c['C_measurement_kind']='Lite_decimal_verified' if c['C_Lite'] is not None else 'Character_unique_compatible_integer'
        c['OHLCV_sha256']=hashlib.sha256(json.dumps(rows,separators=(',',':'),sort_keys=True).encode()).hexdigest();cases.append(c)
    auxiliary_names=['C_fuente_vs_grafico.json','Lite_START_efectivo.json','Lite_END_efectivo.json','C_control_perfiles.json',
                     'C_orden_direccion.json','C_auto_mecha.json','C_extracciones_verificadas.json','C_observabilidad.json']
    auxiliary=[{'report':n,'reason_not_merged':'Alternativeconfiguration, incompleteanchor metadata, or unassignedC. Preserve original scope; not homogeneous nativeManual case.',
                'data':load(n)} for n in auxiliary_names]
    out={'schema_version':1,'created_date_local':'2026-10-14','timezone_of_timestamps':'UTC','symbol':'CME_MINI:NQ1!',
         'scope':'All nativeManual verified observations consolidated from documented manifests/directLitecomparisons/historicalselectors enumerated here. Not everyJSONcase is a measurement; model predictions and Auto/unvalidated/aggregation/subbar cases excluded explicitly. No inferred Litevalues or fabricated volume. Existinglabels known, overlapping, no blindholdout certification.',
         'unique_cases':len(cases),'references':refs,'Lite_measured_cases':sum(c['C_Lite'] is not None for c in cases),
         'Character_only_cases':sum(c['C_Lite'] is None for c in cases),'complete_volume_cases':sum(c['volume_complete'] for c in cases),
         'input_report_sha256':input_hashes,'excluded_references':excluded,'auxiliary_reports':auxiliary,'cases':cases}
    (ROOT/'master_all_C_cases.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    (ROOT/'master_all_C_cases_exclusions.json').write_text(json.dumps({'excluded':excluded,'scope':out['scope']},indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ['cases','input_report_sha256','scope','excluded_references','auxiliary_reports']},indent=2))
    print(json.dumps({'exclusions':excluded[:12],'missing_volume_ids':[c['id'] for c in cases if not c['volume_complete']],
                      'Character_only_ids':[c['id'] for c in cases if c['C_Lite'] is None]},indent=2))

if __name__=='__main__':main()
