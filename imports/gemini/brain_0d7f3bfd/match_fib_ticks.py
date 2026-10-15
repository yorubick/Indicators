import json
from pathlib import Path

# Standard Fibonacci and harmonic ratios
FIB_RATIOS = [
    0.236, 0.382, 0.500, 0.577, 0.618, 0.707, 0.786, 0.886, 1.000,
    1.128, 1.272, 1.414, 1.500, 1.618, 1.732, 2.000
]

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

print("=== MATCHING C TO (TICKS * FIB_RATIO) ===")
print(f"{'START':<9} {'END':<9} {'B':<3} {'C':<6} {'R_pts':<6} {'Ticks':<6} {'BestFib':<8} {'PredC':<6} {'Error':<6}")

for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    if c['bars'] < 21: continue
    s = c['START']
    e = c['END']
    C = c['C']
    B = c['bars']
    
    ohlc = c['OHLC']
    highs = [float(r['high']) for r in ohlc]
    lows = [float(r['low']) for r in ohlc]
    
    H = max(highs)
    L = min(lows)
    R = H - L
    T = round(R * 4) # ticks
    
    # Find closest fib ratio
    best_fib = None
    min_err = 999
    best_pred = 0
    for fib in FIB_RATIOS:
        pred = round(T * fib)
        err = abs(C - pred)
        if err < min_err:
            min_err = err
            best_fib = fib
            best_pred = pred
            
    print(f"{s:<9} {e:<9} {B:<3d} {C:<6.1f} {R:<6.2f} {T:<6d} {best_fib:<8.3f} {best_pred:<6d} {min_err:<6.1f}")
