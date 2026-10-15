"""Control de convergencia de los cinco mejores candidatos, no nuevos modelos."""
import json
import numpy as np
from probar_C_contacto_interior import ROOT,load
def roots(case,model,count):
    direction,source,inclusion,seed_name,timing,target,selection=model
    seg=load(case);point=seg[0 if direction=='forward' else -1]
    seed=dict(zip(('open','high','low','close'),point))
    seed.update(range_high=seg[:,1].max(),range_low=seg[:,2].min(),range_mid=(seg[:,1].max()+seg[:,2].min())/2)
    sources={'close':seg[:,3],'hl2':seg[:,1:3].mean(axis=1),'hlc3':seg[:,1:].mean(axis=1),'ohlc4':seg.mean(axis=1)}
    sl={'all':slice(None),'skip_start':slice(1,None),'skip_end':slice(None,-1),'skip_both':slice(1,-1)}[inclusion]
    samples=sources[source][sl];targets=seg[sl,('open','high','low','close').index(target)]
    if direction=='reverse':samples=samples[::-1];targets=targets[::-1]
    grid=np.geomspace(1.00001,10000,count);a=2/(grid+1);v=np.full(count,seed[seed_name]);groups=[]
    for i,(price,tgt) in enumerate(zip(samples,targets)):
        if timing=='after':v+=a*(price-v)
        if 0<i<len(samples)-1:
            residual=v-tgt;cross=np.flatnonzero(residual[:-1]*residual[1:]<0)
            found=[float((grid[j]+(grid[j+1]-grid[j])*(-residual[j])/(residual[j+1]-residual[j]))*case['dt']/case['C']) for j in cross]
            if found:groups.append(found)
        if timing=='before':v+=a*(price-v)
    if not groups:return None
    selected=groups[0] if selection.startswith('first') else groups[-1] if selection.startswith('last') else [x for g in groups for x in g]
    return (min if selection.endswith('min_N') or selection=='min_N' else max)(selected)
def main():
    data=json.loads((ROOT/'C_contacto_interior.json').read_text())
    output=[]
    for model in data['best_models']:
        refinements=[]
        for n in (4800,19200):
            ks=[roots(c,model['model'],n) for c in data['cases']]
            assert all(x is not None for x in ks)
            refinements.append({'grid_points':n,'K_min':min(ks),'K_max':max(ks),
                'max_relative_change_from_1200':max(abs(x/y-1) for x,y in zip(ks,model['K_by_case']))})
        output.append({'model':model['model'],'refinements':refinements})
    (ROOT/'C_contacto_convergencia.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps(output[:1],indent=2))
if __name__=='__main__':main()
