import json
from pathlib import Path

# Load cases from C_matriz
mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

def predict_c_hybrid(ohlc, delta_sec):
    n = len(ohlc)
    if n < 21:
        # 100% verified continuous fallback formula
        return max(float(delta_sec), n * delta_sec * 10.0 / 183.0)
    else:
        # Structural branch n >= 21
        highs = [float(r['high']) for r in ohlc]
        lows = [float(r['low']) for r in ohlc]
        closes = [float(r['close']) for r in ohlc]
        opens = [float(r['open']) for r in ohlc]
        
        H = max(highs)
        L = min(lows)
        R = H - L
        ticks = round(R * 4) # syminfo.mintick = 0.25
        
        # State: is last bar confirming a pivot or expanding?
        is_new_high = highs[-1] > max(highs[:-1])
        is_new_low = lows[-1] < min(lows[:-1])
        
        # Check pivot confirmation: bar n-2 was high, bar n-1 is lower
        is_pivot_high_confirmed = (len(highs) >= 3 and highs[-2] >= highs[-3] and highs[-2] >= highs[-1])
        
        if is_pivot_high_confirmed:
            # Retracement jump
            return float(ticks + n)
        elif is_new_high:
            # Expansion leg: locks to base fibonacci multiplier of ticks
            # Typically 0.786 or 71
            return round(ticks * 0.786)
        else:
            # Consolidation within range: base tick offset
            return float(round(ticks * 0.577) + (n - 21) * 2)

print("=== TESTING HYBRID FORMULA ON C_MATRIZ CASES ===")
print(f"{'START':<9} {'END':<9} {'Bars':<5} {'Actual_C':<12} {'Predicted_C':<12} {'Error':<10}")
for c in sorted(cases, key=lambda x: (x['START'], x['END'])):
    ohlc = c['OHLC']
    actual = c['C']
    pred = predict_c_hybrid(ohlc, 60)
    err = abs(actual - pred)
    print(f"{c['START']:<9} {c['END']:<9} {c['bars']:<5d} {actual:<12.4f} {pred:<12.4f} {err:<10.4f}")
