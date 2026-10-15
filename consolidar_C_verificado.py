"""Consolida reportes previamente auditados, deduplica selecciones y fija partición por episodio."""
import json,datetime,statistics,hashlib,csv
from pathlib import Path
ROOT=Path(__file__).parent
FILES=['C_matriz.json','C_fronteras_nuevas.json','C_21_regimenes.json','C_START_regimenes.json','C_23_desplazamientos.json','C_END1551.json','C_frontera21.json','C_corto_fuentes.json','C_regimen_decimal.json','C_ventanas_minimas.json','C_ventanas_fijas.json']
def main():
    unique={};excluded=[];references=0
    for name in FILES:
        report=json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
        assert not report.get('failures'),name
        for c in report.get('cases',[])+report.get('shifts',[]):
            raw=c.get('OHLC');C=next((c[k]for k in ['C','measured_C','Lite_C','C_Lite']if k in c),None)
            if not raw or C is None or len(raw)<2:
                excluded.append({'report':name,'case':c.get('prefix',c.get('START')),'reason':'Sin OHLC seleccionado o C escalar observable'});continue
            rows=[{'time':int(r['time']),**{k:float(r[k])for k in ['open','high','low','close']}}for r in raw];rows.sort(key=lambda r:r['time']);dts=[b['time']-a['time']for a,b in zip(rows,rows[1:])];dt=int(statistics.median(dts))
            assert all(x==dt for x in dts) and dt in [15,60,120],name
            if 'bars'in c:assert len(rows)==c['bars'],name
            key=(dt,rows[0]['time'],rows[-1]['time']);references+=1
            if key in unique:
                assert unique[key]['OHLC']==rows,'OHLC conflict '+str(key)
                assert abs(unique[key]['C']-C)<1e-7,'C conflict '+str(key)
                unique[key]['provenance'].append({'report':name,'prefix':c.get('prefix'),'pair':c.get('pair',c.get('suffixes'))});continue
            start=datetime.datetime.fromtimestamp(rows[0]['time'],datetime.timezone.utc);end=datetime.datetime.fromtimestamp(rows[-1]['time'],datetime.timezone.utc)
            split='training' if start.date()==datetime.date(2026,10,12) and ((start.hour==6 and end.hour==6) or start.hour>=18) else 'validation'
            unique[key]={'id':f'{start:%Y%m%d_%H%M%S}_{end:%H%M%S}_{dt}s','START':start.isoformat(),'END':end.isoformat(),'dt':dt,'bars':len(rows),'C':float(C),'branch':'short' if len(rows)<21 else 'long','split':split,'OHLC_sha256':hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),'OHLC':rows,'provenance':[{'report':name,'prefix':c.get('prefix'),'pair':c.get('pair',c.get('suffixes'))}]}
    cases=sorted(unique.values(),key=lambda c:(c['START'],c['dt'],c['END']));counts={f'{branch}_{split}':sum(c['branch']==branch and c['split']==split for c in cases)for branch in ['short','long']for split in ['training','validation']}
    out={'counts':counts,'raw_references':references,'unique_cases':len(cases),'excluded':excluded,'split_rule':'Algorithm training:12oct both START/END hour06, or START>=18; validation:other episodes and13oct. Labels already seen in investigation; not human-blind or new prospective measurement. Overlapping windows stay within episodes.','scope':'Reports listed were audited for native source=chart; no aggregated display experiments included. CSV pair audits inherited from reports, not independently rerun here. C generator inputs outside selected OHLC remain possible.','cases':cases}
    (ROOT/'C_dataset_verificado.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    with (ROOT/'C_dataset_indice.csv').open('w',newline='',encoding='utf-8-sig')as f:
        cols=['id','START','END','dt','bars','C','branch','split','OHLC_sha256'];writer=csv.DictWriter(f,fieldnames=cols);writer.writeheader();writer.writerows({k:c[k]for k in cols}for c in cases)
    print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2))
if __name__=='__main__':main()
