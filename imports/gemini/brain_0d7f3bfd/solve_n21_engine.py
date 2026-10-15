import csv, json, datetime
from pathlib import Path
import numpy as np

# Load 1m data
p_1m = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(p_1m.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def stamp(s, date="2026-10-12"):
    return int(datetime.datetime.fromisoformat(f"{date}T{s}+00:00").timestamp())

# Cases in 1m ending at 19:20 or nearby
cases_1m = [
    ("18:50:00", "19:20:00", 118),
    ("18:54:00", "19:20:00", 134),
    ("18:55:00", "19:20:00", 62),
    ("18:56:00", "19:20:00", 109),
    ("18:57:00", "19:20:00", 77),
    ("18:58:00", "19:20:00", 77),
    ("18:59:00", "19:20:00", 77),
    ("19:00:00", "19:20:00", 77),
    ("19:00:00", "19:21:00", 102),
    ("19:00:00", "19:22:00", 77),
    ("19:11:00", "19:31:00", 80),
    ("04:45:00", "05:05:00", 75),
    ("04:45:00", "05:15:00", 116),
    ("04:45:00", "05:25:00", 113),
    ("04:45:00", "05:30:00", 110),
]

print("=== DEEP MINING FOR n >= 21 ENGINE ===")

# For each case, let's extract:
# 1. Total range
# 2. Cumulative path length (sum of abs(close - close[1]))
# 3. Sum of true ranges (ATR sum)
# 4. Standard deviation of close
# 5. Position of highest high and lowest low
# 6. Distance from lowest low to end
# 7. Distance from highest high to end
# 8. Retracement from high to end close
# 9. Net displacement abs(close[-1] - open[0])
for s_str, e_str, C in cases_1m:
    # check date
    date = "2026-10-12"
    t_s = stamp(s_str, date)
    t_e = stamp(e_str, date)
    sub = [candles_1m[t] for t in range(t_s, t_e + 60, 60) if t in candles_1m]
    if not sub:
        continue
    n = len(sub)
    highs = [b['high'] for b in sub]
    lows = [b['low'] for b in sub]
    closes = [b['close'] for b in sub]
    opens = [b['open'] for b in sub]
    
    rng = max(highs) - min(lows)
    idx_max = highs.index(max(highs))
    idx_min = lows.index(min(lows))
    bars_from_min = n - 1 - idx_min
    bars_from_max = n - 1 - idx_max
    
    path = sum(abs(closes[i] - closes[i-1]) for i in range(1, n))
    tr_sum = sum(max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])) for i in range(1, n))
    std_c = np.std(closes)
    
    disp = abs(closes[-1] - opens[0])
    eff = disp / path if path > 0 else 0
    
    # Check linear regression slope
    x = np.arange(n)
    slope, intercept = np.polyfit(x, closes, 1)
    
    print(f"[{s_str[:5]}->{e_str[:5]}] n={n:2d} | C={C:3d} | Rng={rng:5.2f} | BarsFromMin={bars_from_min:2d} | BarsFromMax={bars_from_max:2d} | Path={path:6.2f} | TR_sum={tr_sum:6.2f} | Slope={slope:6.3f} | Std={std_c:5.2f}")
