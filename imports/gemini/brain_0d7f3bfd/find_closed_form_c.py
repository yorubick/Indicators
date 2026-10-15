import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

train = [c for c in d["cases"] if c["branch"] == "long" and c["split"] == "training"]

print(f"Loaded {len(train)} training cases.")

# We want to find an EXACT formula:
# C_pred = round( formula(OHLC) )
# such that C_pred == round(c['C']) for ALL 32 training cases!

# Let's extract potential components for each case:
data = []
for c in train:
    ohlc = c["OHLC"]
    n = len(ohlc)
    dt = c["dt"]
    opens = np.array([b["open"] for b in ohlc])
    highs = np.array([b["high"] for b in ohlc])
    lows = np.array([b["low"] for b in ohlc])
    closes = np.array([b["close"] for b in ohlc])
    
    h_max = np.max(highs)
    l_min = np.min(lows)
    i_max = int(np.argmax(highs))
    i_min = int(np.argmin(lows))
    
    rng = h_max - l_min
    
    # Distance between extremes
    d_hl = abs(i_max - i_min)
    
    # Initial candle range
    init_rng = highs[0] - lows[0]
    
    # End candle range
    end_rng = highs[-1] - lows[-1]
    
    # First close
    c0 = closes[0]
    c_end = closes[-1]
    
    # Time span
    t_span = (n - 1) * dt
    
    # True range sum
    tr = np.maximum(highs - lows, np.abs(highs - np.roll(closes, 1)))
    tr[0] = highs[0] - lows[0]
    sum_tr = np.sum(tr)
    atr = np.mean(tr)
    
    c_target = int(round(c["C"]))
    
    data.append({
        "id": c["id"],
        "C": c_target,
        "n": n,
        "dt": dt,
        "rng": rng,
        "d_hl": d_hl,
        "i_max": i_max,
        "i_min": i_min,
        "d_max_end": n - 1 - i_max,
        "d_min_end": n - 1 - i_min,
        "init_rng": init_rng,
        "end_rng": end_rng,
        "c0": c0,
        "c_end": c_end,
        "t_span": t_span,
        "sum_tr": sum_tr,
        "atr": atr
    })

# Check if C / dt has simple relationships
print("Checking C / dt across training:")
for r in data:
    ratio = r["C"] / r["dt"]
    print(f"{r['id']:28s} n={r['n']:2d} C={r['C']:3d} dt={r['dt']:3d} C/dt={ratio:6.3f} rng={r['rng']:5.2f} d_hl={r['d_hl']:2d}")
