"""Audita los dos rangos elegidos solo por OHLC antes de medir C."""
import json,datetime
from analizar_C_fuente_vs_grafico import ROOT,read,fit_lite,COLS
from obtener_C import recover
def main():
    selected=json.loads((ROOT/'C_21_seleccion_regimenes.json').read_text())['selected'];cases=[]
    for tag,key in [('alcista','bull'),('lateral','lateral')]:
        info=selected[key];prefix=f'C_21_{tag}';a,b=[read(f'{prefix}_{s}.csv')for s in ['c','d']];common=set(a)&set(b)
        assert common and all(a[t][k]==b[t][k]for t in common for k in COLS),'pareja inestable'
        start,end=[int(datetime.datetime.fromisoformat(info[k]).timestamp())for k in ['START','END']];ts=list(range(start,end+1,60));assert len(ts)==21 and all(t in b for t in ts)
        fits=fit_lite(b,60,60);Cs=[v['C']for v in fits.values()];C=sum(Cs)/6;ct=recover(ROOT/'manual'/f'{prefix}_d.csv');iv=ct['C_seconds_interval']
        assert max(Cs)-min(Cs)<1e-7 and max(v['rmse']for v in fits.values())<1e-8
        assert iv['lower_inclusive']-1e-8<=C<iv['upper_exclusive']+1e-8,'Character incompatible'
        rows=[b[t]for t in ts]
        cases.append({'prefix':prefix,'suffixes':['c','d'],'START':info['START'],'END':info['END'],'bars':21,'C':C,'selection_metrics':{k:info[k]for k in ['net','ER','range']},'Gemini_prediction_before_measurement':info['Gemini_prediction_before_measurement'],'Gemini_match':abs(info['Gemini_prediction_before_measurement']['C']-C)<1e-7,'Character_interval':iv,'high':max(float(r['high'])for r in rows),'low':min(float(r['low'])for r in rows),'repeated_curve_cells':len(common)*16,'OHLC':[{'time':t,**{k:float(b[t][k])for k in ['open','high','low','close']}}for t in ts]})
    (ROOT/'C_21_regimenes.json').write_text(json.dumps({'cases':cases,'scope':'Source/chart60s, manual aligned anchors, two21bar ranges selected by OHLC only.'},indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in c.items()if k!='OHLC'}for c in cases],indent=2))
if __name__=='__main__':main()
