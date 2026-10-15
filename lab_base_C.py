"""Base experimental: estado observable separado de hipótesis numéricas de C.

No afirma el algoritmo del indicador. La rama larga devuelve C=None hasta
que una regla explícita supere los controles; nunca sustituye por71/77.
"""
from dataclasses import dataclass,asdict

@dataclass
class RangeState:
    n:int=0
    high:float|None=None
    low:float|None=None
    idx_high:int|None=None
    idx_low:int|None=None
    start_time:int|None=None
    end_time:int|None=None
    close:float|None=None
    new_high:bool=False
    new_low:bool=False
    last_confirmed_high:int|None=None
    last_confirmed_low:int|None=None

def states(rows):
    """Flujo causal desde START. Extremos estrictos conservan el primer empate.

    Pivote radio1:estricto frente a izquierda, permite empate a derecha;
    solo confirma al recibir la vela derecha, nunca usa datos posteriores.
    """
    state=RangeState();history=[]
    for row in rows:
        i=state.n;high=float(row['high']);low=float(row['low'])
        state.new_high=state.high is not None and high>state.high
        state.new_low=state.low is not None and low<state.low
        if state.high is None or high>state.high:state.high=high;state.idx_high=i
        if state.low is None or low<state.low:state.low=low;state.idx_low=i
        if state.start_time is None:state.start_time=int(row['time'])
        state.end_time=int(row['time']);state.close=float(row['close']);state.n+=1
        if len(history)>=2:
            left,prev=history[-2:]
            if float(prev['high'])>float(left['high'])and float(prev['high'])>=high:state.last_confirmed_high=i-1
            if float(prev['low'])<float(left['low'])and float(prev['low'])<=low:state.last_confirmed_low=i-1
        history.append(row);yield asdict(state)

def estimate_C(final_state,source_seconds):
    n=final_state['n']
    if source_seconds not in [15,60,120]:return {'C':None,'status':'source_outside_tested_domain'}
    if n<2:return {'C':None,'status':'not_observable_in_verified_controls'}
    if n<21:return {'C':max(source_seconds,n*source_seconds*10/183),'status':'empirical_short_rule','scope':'Matches observed short cases; not a universal proof.'}
    return {'C':None,'status':'long_generator_not_identified'}

def experimental_consolidation(final_state,source_seconds):
    """Hipótesis numérica sola; no decide que el rango sea consolidación."""
    import math
    return math.floor((final_state['n']-1)*source_seconds/24)
