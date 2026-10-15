"""Familia finita de períodos espectrales; no selecciona parámetros por rango."""
import json
import math
from pathlib import Path
import numpy as np
from probar_C_estructura import load

ROOT = Path(__file__).parent

def descriptors(v):
    o, h, l, c = v.T
    sources = {'close':c, 'hl2':(h+l)/2, 'hlc3':(h+l+c)/3, 'ohlc4':v.mean(axis=1)}
    out = {}
    for source, x in sources.items():
        for transform in ('centered', 'linear_residual', 'difference'):
            y = x.copy()
            if transform == 'linear_residual':
                t = np.arange(len(y))
                y -= np.polyval(np.polyfit(t, y, 1), t)
            elif transform == 'difference':
                y = np.diff(y)
            y -= y.mean()
            for window in ('rectangular', 'Hann', 'Hamming'):
                weights = np.ones(len(y)) if window == 'rectangular' else (
                    np.hanning(len(y)) if window == 'Hann' else np.hamming(len(y)))
                for padding in (1, 4):
                    frequencies = np.fft.rfftfreq(len(y)*padding)[1:]
                    power = abs(np.fft.rfft(y*weights, n=len(y)*padding)[1:])**2
                    total = power.sum()
                    vals = None
                    if len(y) >= 5 and total > 1e-20:
                        vals = {
                            'peak_period':1/frequencies[int(np.argmax(power))],
                            'mean_period':float(np.sum(power/frequencies)/total),
                            'inverse_mean_frequency':float(total/np.sum(power*frequencies)),
                            'median_power_period':1/frequencies[int(np.searchsorted(np.cumsum(power), total/2))],
                        }
                    for metric in ('peak_period', 'mean_period', 'inverse_mean_frequency', 'median_power_period'):
                        out[(source,transform,window,padding,metric)] = None if vals is None else float(vals[metric])
    return out

def main():
    old = json.loads((ROOT/'C_estructura.json').read_text())
    train = [dict(c) for c in old['training_cases']+old['reserved_cases'] if c['C']>c['dt']]
    diagnostic = [{'file':c['extraction']['file'], 'start':'18:55:00', 'end':c['END_UTC'], 'dt':15, 'C':c['C']}
                  for c in json.loads((ROOT/'C_END_barrido.json').read_text())['cases']]
    measured = []
    for case in train+diagnostic:
        v, interval, fallback = load(case)
        case['interval'] = interval
        case['OHLC_fallback'] = fallback
        measured.append(descriptors(v))
    scores, missing = [], []
    for key in measured[0]:
        absent = [i for i,m in enumerate(measured[:len(train)]) if m[key] is None]
        if absent:
            missing.append({'model':key, 'missing_indices':absent})
            continue
        shape = [case['dt']*m[key] if m[key] is not None else None for case,m in zip(train+diagnostic,measured)]
        K = math.exp(float(np.mean(np.log([c['C']/s for c,s in zip(train,shape)]))))
        for quantization in ('none', 'nearest_second', 'floor_second', 'ceil_second'):
            bounds = []
            for case,s in zip(train,shape):
                if quantization == 'none':
                    lo, hi = case['interval']['lower_inclusive'], case['interval']['upper_exclusive']
                else:
                    # All training cases have a unique compatible integer C.
                    delta = {'nearest_second':(-.5,.5), 'floor_second':(0,1), 'ceil_second':(-1,0)}[quantization]
                    lo, hi = case['C']+delta[0], case['C']+delta[1]
                bounds.append((lo/s,hi/s))
            lower, upper = max(b[0] for b in bounds), min(b[1] for b in bounds)
            def predict(s,dt):
                if s is None:return None
                p=K*s
                if quantization=='nearest_second':p=math.floor(p+.5)
                elif quantization=='floor_second':p=math.floor(p)
                elif quantization=='ceil_second':p=math.ceil(p)
                return max(dt,p)
            preds = [predict(s,c['dt']) for c,s in zip(train,shape)]
            tests = [{'END':c['end'], 'C':c['C'], 'prediction':predict(s,c['dt'])}
                     for c,s in zip(diagnostic,shape[len(train):])]
            scores.append({'model':key,'quantization':quantization,'K_training_only':K,
                           'K_lower':lower,'K_upper':upper,'common_K_exists':lower<upper,
                           'lower_constraint_case':{k:train[max(range(len(bounds)),key=lambda i:bounds[i][0])][k] for k in ('start','end','dt','C')},
                           'upper_constraint_case':{k:train[min(range(len(bounds)),key=lambda i:bounds[i][1])][k] for k in ('start','end','dt','C')},
                           'worst_training_relative_error':max(abs(p/c['C']-1) for c,p in zip(train,preds)),
                           'latest_END_diagnostics':tests})
    scores.sort(key=lambda r:r['worst_training_relative_error'])
    out={'formula':'C=max(dt, quantize(K*dt*spectral_period_bars))',
         'training_cases':train,'diagnostic_cases':diagnostic,'descriptor_count':len(measured[0]),
         'tested_rules':len(scores),'common_K_rules':sum(s['common_K_exists'] for s in scores),
         'training_count':len(train),'diagnostic_count':len(diagnostic),
         'smallest_rejection_gap_K':min(s['K_lower']-s['K_upper'] for s in scores),
         'missing_descriptors':missing,'best_training_rules':scores[:10],
         'scope':'Finite spectral family. No per-range tuning or model selection on latest END. Cases overlap within one day. FFT is an offline hypothesis test, not a claim about Pine implementation. Floor empirical. Ceil endpoints have reversed inclusivity; all empty intersections are separated by a positive gap so endpoints do not affect rejection.'}
    (ROOT/'C_espectro.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('training_cases','diagnostic_cases','missing_descriptors','best_training_rules')},indent=2))
    print(json.dumps(scores[0],indent=2))

if __name__=='__main__':main()
