"""C como escala de una EMA que equilibra todo el recorrido.

N=K*C/resolucion. K se ajusta solo a casos anteriores; las raíces extremas
se seleccionan sin usar el C real del caso. Búsqueda numérica finita.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from probar_C_estructura import load
ROOT=Path(__file__).parent

def roots(v,grid,only_model=None,phase='after'):
    result={};o,h,l,c=v.T
    sources={'close':c,'hl2':(h+l)/2,'hlc3':(h+l+c)/3,'ohlc4':v.mean(axis=1)}
    for direction in ('forward','reverse'):
        if only_model and direction!=only_model[0]:continue
        point=v[0 if direction=='forward' else -1]
        seeds=dict(zip(('open','high','low','close'),point))
        seeds['range_mid']=(h.max()+l.min())/2
        seeds['range_high']=h.max();seeds['range_low']=l.min()
        up=c[-1]>=c[0]
        if direction=='reverse':up=not up
        seeds['range_extreme_against_net_move']=h.max() if up else l.min()
        seeds['range_extreme_with_net_move']=l.min() if up else h.max()
        for inclusion in ('all','skip_start','skip_end','skip_both'):
            if only_model and inclusion!=only_model[1]:continue
            indices={'all':np.arange(len(v)),'skip_start':np.arange(1,len(v)),
                'skip_end':np.arange(len(v)-1),'skip_both':np.arange(1,len(v)-1)}[inclusion]
            if direction=='reverse':indices=indices[::-1]
            for source,x in sources.items():
                if only_model and source!=only_model[2]:continue
                for seed_name,seed in seeds.items():
                    if only_model and seed_name!=only_model[3]:continue
                    ema=np.full(len(grid),seed);alpha=2/(grid+1)
                    area=np.zeros(len(grid));energy=np.zeros(len(grid));wick=np.zeros(len(grid));square=np.zeros(len(grid))
                    count=0;tr=[];previous=None
                    for i in indices:
                        if phase=='after':ema+=alpha*(x[i]-ema)
                        residual=c[i]-ema
                        area+=residual;energy+=residual*abs(residual);square+=residual**2
                        if h[i]>l[i]:wick+=(ema-(h[i]+l[i])/2)/(h[i]-l[i]);count+=1
                        if previous is not None:tr.append(max(h[i]-l[i],abs(h[i]-previous),abs(l[i]-previous)))
                        previous=c[i]
                        if phase=='before':ema+=alpha*(x[i]-ema)
                    metrics={'signed_area_zero':area,'signed_energy_zero':energy,
                        'mean_wick_position_half':wick,
                        'RMS_residual_equals_mean_TR':np.sqrt(square/len(indices))-np.mean(tr)}
                    for name,res in metrics.items():
                        crossing=np.flatnonzero(res[:-1]*res[1:]<0)
                        found=[float(grid[i]+(grid[i+1]-grid[i])*(-res[i])/(res[i+1]-res[i])) for i in crossing]
                        result[(direction,inclusion,source,seed_name,name)]=found
    return result

def score(cases,root_sets,key,K,branch):
    pred=[];matched=0
    for c,rs in zip(cases,root_sets):
        options=rs[key]
        if not options:return None
        length=min(options) if branch=='smallest' else max(options)
        value=max(c['dt'],length*c['dt']/K);pred.append(value)
        matched+=int(c['interval']['lower_inclusive']<=value<c['interval']['upper_exclusive'])
    return {'predictions':pred,'interval_matches':matched,
        'median_relative_error':float(np.median([abs(p/c['C']-1) for p,c in zip(pred,cases)])),
        'max_relative_error':max(abs(p/c['C']-1) for p,c in zip(pred,cases))}

def main():
    phase='before' if '--before' in sys.argv[1:] else 'after'
    prior=json.loads((ROOT/'C_estructura.json').read_text())
    train=prior['training_cases']+prior['reserved_cases']
    new=json.loads((ROOT/'C_barrido_ampliado.json').read_text())['new_controls']
    test=[{'file':c['extraction']['file'],'start':c['START_UTC'],'end':c['END_UTC'],'dt':15,
           'C':c['extraction']['compatible_integer_C_seconds'][0]} for c in new]
    grid=np.geomspace(1.00001,10000,1200);all_roots=[]
    for i,c in enumerate(train+test):
        v,interval,_=load(c);c['interval']=interval
        all_roots.append(roots(v,grid,phase=phase))
        print('Processed',i+1,len(train+test),flush=True)
    train_roots=all_roots[:len(train)];test_roots=all_roots[len(train):];scores=[];coverage=[]
    active_indices=[i for i,c in enumerate(train) if c['C']>c['dt']]
    active_cases=[train[i] for i in active_indices];active_roots=[train_roots[i] for i in active_indices]
    for key in all_roots[0]:
        missing=[{'start':train[i]['start'],'end':train[i]['end'],'dt':train[i]['dt'],'C':train[i]['C']} for i in active_indices if not train_roots[i][key]]
        coverage.append({'model':key,'nonfloor_cases_with_roots':len(active_indices)-len(missing),'missing_nonfloor_cases':missing})
        # A missing root in a saturated case is not used to reject a rule.
        if missing:continue
        for branch in ('smallest','largest'):
            get=min if branch=='smallest' else max
            ratios=[get(r[key])*c['dt']/c['C'] for c,r in zip(train,train_roots) if c['C']>c['dt']]
            K=math.exp(float(np.mean(np.log(ratios))))
            lower=max(get(r[key])*c['dt']/c['interval']['upper_exclusive'] for c,r in zip(active_cases,active_roots))
            upper=min(get(r[key])*c['dt']/c['interval']['lower_inclusive'] for c,r in zip(active_cases,active_roots))
            scores.append({'model':key,'root_branch':branch,'K_training_only':K,
                'K_compatible_lower':lower,'K_compatible_upper':upper,'K_compatible_intersection_nonempty':lower<upper,
                'K_min_nonfloor':min(ratios),'K_max_nonfloor':max(ratios),
                'training':score(active_cases,active_roots,key,K,branch),'reserved':score(test,test_roots,key,K,branch)})
    scores.sort(key=lambda s:(s['training']['max_relative_error'],s['training']['median_relative_error']))
    coverage.sort(key=lambda c:-c['nonfloor_cases_with_roots'])
    out={'formula':'N=K*C/source_seconds; select smallest or largest positive root of whole-path condition; C_pred=max(source_seconds,N*source_seconds/K)',
        'grid':[float(grid[0]),float(grid[-1]),len(grid)],'EMA_evaluation_phase':phase,'training_count':len(train),'reserved_count':len(test),
        'conditions':list(dict.fromkeys(k[-1] for k in all_roots[0])),
        'model_count':len(all_roots[0])*2,'models_with_roots_all_nonfloor_training':len(scores),
        'nonfloor_training_count':len(active_indices),'best_root_coverage':coverage[:5],
        'models_with_compatible_K_nonfloor_training':sum(s['K_compatible_intersection_nonempty'] for s in scores),
        'selection':'Root branch and K selected only by earlier training cases, without choosing roots nearest the known C. Four latest ranges checked afterwards.',
        'scope':'Finite grid, sign-changing roots, selected EMA phase, explicit seeds and inclusions. Missing/tangent roots and other adaptive rules not excluded. Same-date overlapping windows.',
        'best_training_models':scores[:10],
        'reserved_cases':[{k:c[k] for k in ('start','end','dt','C','file')} for c in test]}
    output_name='C_balance_recorrido_antes_update.json' if phase=='before' else 'C_balance_recorrido.json'
    (ROOT/output_name).write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('reserved_cases','best_training_models','best_root_coverage')},indent=2))
    print(json.dumps(coverage[:1],indent=2))
    print(json.dumps(scores[:1],indent=2))

if __name__=='__main__':main()
