import csv
from datetime import datetime, timezone
import numpy as np

# Load 15s bars
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Solved C values
c_15s_map = {
    21: 88, 22: 67, 23: 88, 24: 88, 25: 79, 26: 102, 27: 123,
    28: 67, 29: 87, 30: 106, 31: 87, 32: 123, 33: 87
}
c_1m_map = {
    21: 50, 22: 52, 23: 71, 24: 135, 25: 130, 26: 88, 27: 135,
    28: 112, 29: 136, 30: 112, 31: 112, 32: 135, 33: 112
}

print(f"{'n':>2} | {'Min':>5} | {'C_15s':>5} | {'C_1m':>4} | {'Rng':>5} | {'Body':>6} | {'UWick':>5} | {'LWick':>5} | {'Pos%':>5} | {'MonotonicUp':>11} | {'MaxAtSubbar':>11}")
print("-" * 80)

for m in range(23, 36):
    n = m - 2 # 19:23 -> n=21
    t_min = int(datetime(2026, 10, 12, 19, m, 0, tzinfo=timezone.utc).timestamp())
    sub = [bars_15s[t_min + s] for s in [0, 15, 30, 45]]
    
    m_open = float(sub[0]["open"])
    m_close = float(sub[3]["close"])
    m_high = max(float(b["high"]) for b in sub)
    m_low = min(float(b["low"]) for b in sub)
    
    m_rng = m_high - m_low
    m_body = m_close - m_open
    m_uwick = m_high - max(m_open, m_close)
    m_lwick = min(m_open, m_close) - m_low
    pos_pct = ((m_close - m_low) / m_rng * 100.0) if m_rng > 0 else 50.0
    
    # check monotonic closes: c0 < c1 < c2 < c3
    closes = [float(b["close"]) for b in sub]
    mono_up = all(closes[i] < closes[i+1] for i in range(3))
    
    # which sub-bar made the high of the minute?
    sub_highs = [float(b["high"]) for b in sub]
    max_idx = np.argmax(sub_highs)
    sub_names = [":00", ":15", ":30", ":45"]
    max_sub = sub_names[max_idx]
    
    c15 = c_15s_map.get(n, "?")
    c1m = c_1m_map.get(n, "?")
    
    print(f"{n:>2} | 19:{m:02d} | {c15:>5} | {c1m:>4} | {m_rng:>5.2f} | {m_body:>+6.2f} | {m_uwick:>5.2f} | {m_lwick:>5.2f} | {pos_pct:>5.1f}% | {str(mono_up):>11} | {max_sub:>11}")
