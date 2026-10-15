"""Entrada antes no ensayada: volumen nativo1m, unido por timestamp y OHLC idéntico."""
import json,math
import numpy as np
from analizar_C_fuente_vs_grafico import ROOT,read
def metrics(c):
    rows=c['OHLC'];v=np.array([r['volume']for r in rows]);p=np.array([r['close']for r in rows]);n=len(v);mean=float(v.mean());end=float(v[-1]);first=float(v[0]);neff=float(v.sum()**2/np.dot(v,v));ema=float(v[:20].mean())
    for x in v[20:]:ema+=(2/21)*(x-ema)
    std=float(v.std());rho=abs(float(np.corrcoef(p,v)[0,1]));f={'n_over_Neff':n/neff,'Neff_over_n':neff/n,'end_over_mean':end/mean,'mean_over_end':mean/end,'first_over_mean':first/mean,'mean_over_first':mean/first,'EMA20_over_end':ema/end,'end_over_EMA20':end/ema,'EMA20_over_mean':ema/mean,'mean_over_EMA20':mean/ema,'1+CV':1+std/mean,'inverse1+CV':1/(1+std/mean)}
    if math.isfinite(rho)and rho<1:
        f.update({'1+abs_corrPV':1+rho,'1-abs_corrPV':1-rho,'inverse1+corrPV':1/(1+rho),'inverse1-corrPV':1/(1-rho),'1+corrPV2':1+rho*rho,'1-corrPV2':1-rho*rho,'inverse1+corrPV2':1/(1+rho*rho),'inverse1-corrPV2':1/(1-rho*rho)})
    vwap=float(np.dot(v,p)/v.sum());plain=float(p.mean());price_sd=float(p.std());height=max(r['high']for r in rows)-min(r['low']for r in rows)
    if height>0:f['1+VWAP_offset_range']=1+abs(vwap-plain)/height
    if price_sd>0:f['1+VWAP_offset_std']=1+abs(vwap-plain)/price_sd
    return {k:float(value)for k,value in f.items()}
def quantize(x,mode):return math.floor(x+.5)if mode=='nearest'else(math.floor(x)if mode=='floor'else math.ceil(x))
def main():
    a,b=[read(f'C_VOL_1m_{s}.csv')for s in ['a','b']];shared=set(a)&set(b)
    assert all(a[t]['Volume']==b[t]['Volume']and all(a[t][k]==b[t][k]for k in ['open','high','low','close'])for t in shared)
    dataset=json.loads((ROOT/'C_dataset_verificado.json').read_text());joined=[];excluded=[]
    for c in dataset['cases']:
        if c['dt']!=60:excluded.append({'id':c['id'],'reason':'Volumen exportado solo1m'});continue
        if not all(r['time']in b for r in c['OHLC']):excluded.append({'id':c['id'],'reason':'Cobertura volumen incompleta'});continue
        rows=[]
        for r in c['OHLC']:
            assert all(r[k]==float(b[r['time']][k])for k in ['open','high','low','close']),c['id']
            assert b[r['time']]['Volume'],c['id'];rows.append({**r,'volume':float(b[r['time']]['Volume'])})
        joined.append({**c,'OHLC':rows})
    (ROOT/'C_dataset_con_volumen.json').write_text(json.dumps({'cases':joined,'excluded':excluded,'source':'manual/C_VOL_1m_b.csv','repeated_OHLC_volume_cells':len(shared)*5,'scope':'1m only; joins validated by exact OHLC. Volumes are observations, not demonstrated inputs of original C.'},indent=2),encoding='utf-8')
    train=[c for c in joined if c['branch']=='long'and c['split']=='training'];test=[c for c in joined if c['branch']=='long'and c['split']=='validation'];features=[metrics(c)for c in train];names=sorted(set.intersection(*(set(f)for f in features)));records=[]
    for name in names:
        vals=[f[name]*c['bars']*c['dt']*10/183 for f,c in zip(features,train)]
        if not all(math.isfinite(v)and v>0 for v in vals):continue
        for mode in ['nearest','floor','ceil']:
            bounds=[((round(c['C'])-.5,round(c['C'])+.5)if mode=='nearest'else((round(c['C']),round(c['C'])+1)if mode=='floor'else(round(c['C'])-1,round(c['C']))))for c in train];low=max(lo/v for(lo,hi),v in zip(bounds,vals));high=min(hi/v for(lo,hi),v in zip(bounds,vals));ok=low<high;K=(low+high)/2 if ok else float(np.median([c['C']/v for c,v in zip(train,vals)]));errors=[abs(quantize(K*v,mode)-round(c['C']))for c,v in zip(train,vals)]
            rec={'feature':name,'quantizer':mode,'K_training':K,'K_interval':[low,high],'exact_training_candidate':ok,'training_matches':sum(e==0 for e in errors),'training_cases':len(train),'max_training_error_seconds':max(errors)}
            if ok:rec['validation_matches']=sum(quantize(K*metrics(c)[name]*c['bars']*c['dt']*10/183,mode)==round(c['C'])for c in test)
            records.append(rec)
    records.sort(key=lambda r:(-r['training_matches'],r['max_training_error_seconds'],r['feature'],r['quantizer']));out={'joined_cases':len(joined),'excluded':excluded,'long_training_cases':len(train),'long_validation_cases':len(test),'models_tested':len(records),'exact_training_candidates':sum(r['exact_training_candidate']for r in records),'formula':'quantize(K*n*dt*10/183*volume_feature), K trained only; no global floor','scope':'Finite predeclared volume family. Neither failure nor success establishes whether original C uses volume. Validation untouched unless full training passed.','records':records};(ROOT/'C_volumen_candidatos.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({**{k:v for k,v in out.items()if k!='records'},'best_training_only':records[:2]},indent=2))
if __name__=='__main__':main()
