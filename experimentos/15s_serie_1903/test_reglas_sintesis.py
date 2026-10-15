import csv
from datetime import datetime, timezone
import numpy as np

# Load 15s bars
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# 21 confirmed cases
cases = [
    # START shifts (END 19:33)
    ("19:03", "19:33", 87),
    ("19:08", "19:33", 70),
    ("19:10", "19:33", 66),
    ("19:13", "19:33", 66),
    ("19:15", "19:33", 77),
    ("19:18", "19:33", 39),
    ("19:23", "19:33", 33),
    ("19:28", "19:33", 16),
    ("19:30", "19:33", 15),
    # END sweep (START 19:03)
    ("19:03", "19:23", 88),
    ("19:03", "19:24", 67),
    ("19:03", "19:25", 88),
    ("19:03", "19:26", 88),
    ("19:03", "19:27", 79),
    ("19:03", "19:28", 102),
    ("19:03", "19:29", 123),
    ("19:03", "19:30", 67),
    ("19:03", "19:31", 87),
    ("19:03", "19:32", 106),
    ("19:03", "19:34", 123),
    ("19:03", "19:35", 87),
]

print("=== EVALUACIÓN DE REGLAS DE SINTESIS PARA C ===")
print(f"{'Caso':<15} | {'T(s)':<5} | {'C_obs':<5} | {'C_base':<6} | {'C_teorico':<10} | {'Error':<5}")
print("-" * 55)

# Test candidate model:
# 1. Base linear equation: C_base = max(15, round(T * 10 / 183))
# 2. If T <= 1200 and not impulse: C = C_base
# 3. For impulse breakout at END (Close at >92% of range, upper wick < 1.0):
#    jump to expansion harmonic
for s_str, e_str, c_obs in cases:
    s_h, s_m = map(int, s_str.split(":"))
    e_h, e_m = map(int, e_str.split(":"))
    t_start = int(datetime(2026, 10, 12, s_h, s_m, 0, tzinfo=timezone.utc).timestamp())
    t_end = int(datetime(2026, 10, 12, e_h, e_m, 0, tzinfo=timezone.utc).timestamp())
    T = t_end - t_start
    c_base = max(15, round(T * 10.0 / 183.0))
    
    # Analyze END candle (4 subbars of e_m)
    sub = [bars_15s[t_end + i*15] for i in range(4)]
    o_end = float(sub[0]["open"])
    c_end = float(sub[3]["close"])
    h_end = max(float(b["high"]) for b in sub)
    l_end = min(float(b["low"]) for b in sub)
    rng_end = h_end - l_end
    wick_up = h_end - max(o_end, c_end)
    cl_pos = (c_end - l_end) / rng_end if rng_end > 0 else 0.5
    
    # Is it a major impulse candle?
    is_impulse = (cl_pos > 0.90) and (wick_up <= 0.75) and (rng_end >= 5.5)
    
    tag = f"{s_str}->{e_str}"
    print(f"{tag:<15} | {T:<5} | {c_obs:<5} | {c_base:<6} | {'Impulse' if is_impulse else 'Normal':<10} | {c_obs - c_base:+5d}")
