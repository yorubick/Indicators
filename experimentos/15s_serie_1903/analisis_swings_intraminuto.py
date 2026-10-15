import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# 13 END cases with START 19:03
cases_end = [
    ("19:23", 88, 50),
    ("19:24", 67, 52),
    ("19:25", 88, 71),
    ("19:26", 88, 135),
    ("19:27", 79, 130),
    ("19:28", 102, 88),
    ("19:29", 123, 135),
    ("19:30", 67, 112),
    ("19:31", 87, 112),
    ("19:32", 106, 112),
    ("19:33", 87, 112),
    ("19:34", 123, 136),
    ("19:35", 87, 112),
]

t_start = int(datetime(2026, 10, 12, 19, 3, 0, tzinfo=timezone.utc).timestamp())

# Detect causal pivots dynamically up to t_eval
# In Pine Script: pivothigh(high, 2, 2) is confirmed 2 bars later (30s delay)
def get_confirmed_pivots_causal(subbars, R=2):
    piv_h = []
    piv_l = []
    # Can only confirm pivots up to len(subbars) - 1 - R
    for i in range(R, len(subbars) - R):
        h = float(subbars[i]["high"])
        l = float(subbars[i]["low"])
        is_h = all(float(subbars[i-j]["high"]) < h for j in range(1, R+1)) and all(float(subbars[i+k]["high"]) <= h for k in range(1, R+1))
        is_l = all(float(subbars[i-j]["low"]) > l for j in range(1, R+1)) and all(float(subbars[i+k]["low"]) >= l for k in range(1, R+1))
        t_sub = int(subbars[i]["time"])
        if is_h: piv_h.append((t_sub, h))
        if is_l: piv_l.append((t_sub, l))
    return piv_h, piv_l

print("=== ANÁLISIS DE PIVOTES INTRAMINUTO CAUSALES (15s) ===")
print(f"{'END':<6} | {'C_15s':<5} | {'C_1m':<5} | {'Last_Piv_H':<10} | {'Bars_H':<6} | {'Last_Piv_L':<10} | {'Bars_L':<6} | {'Swing_Rng':<9} | {'Close_vs_PivH'}")
print("-" * 95)

for m_str, c_15, c_1m in cases_end:
    e_m = int(m_str.split(":")[1])
    t_end = int(datetime(2026, 10, 12, 19, e_m, 45, tzinfo=timezone.utc).timestamp())
    
    # Subbars up to END
    subbars = [bars_15s[t] for t in range(t_start, t_end + 1, 15) if t in bars_15s]
    c_cur = float(subbars[-1]["close"])
    
    piv_h, piv_l = get_confirmed_pivots_causal(subbars, R=2)
    
    if piv_h:
        last_t_h, last_val_h = piv_h[-1]
        bars_since_h = (t_end - last_t_h) // 15
        h_str = f"{last_val_h:.2f}"
    else:
        last_val_h = 0
        bars_since_h = -1
        h_str = "None"
        
    if piv_l:
        last_t_l, last_val_l = piv_l[-1]
        bars_since_l = (t_end - last_t_l) // 15
        l_str = f"{last_val_l:.2f}"
    else:
        last_val_l = 0
        bars_since_l = -1
        l_str = "None"
        
    swing_rng = (last_val_h - last_val_l) if (piv_h and piv_l) else 0.0
    diff_piv_h = c_cur - last_val_h if piv_h else 0.0
    
    print(f"{m_str:<6} | {c_15:<5} | {c_1m:<5} | {h_str:<10} | {bars_since_h:<6} | {l_str:<10} | {bars_since_l:<6} | {swing_rng:<9.2f} | {diff_piv_h:+6.2f} pts")
