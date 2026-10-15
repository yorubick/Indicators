# Deep comparison of 19:26, 19:29, 19:33, 19:34
import csv
from datetime import datetime, timezone

with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

for m in [26, 29, 30, 31, 32, 33, 34, 35]:
    t = int(datetime(2026, 10, 12, 19, m, 0, tzinfo=timezone.utc).timestamp())
    prev_t = t - 60
    
    sub = [bars_15s[t + s] for s in [0, 15, 30, 45]]
    prev_sub = [bars_15s[prev_t + s] for s in [0, 15, 30, 45]]
    
    h = max(float(b["high"]) for b in sub)
    l = min(float(b["low"]) for b in sub)
    o = float(sub[0]["open"])
    c = float(sub[3]["close"])
    
    prev_h = max(float(b["high"]) for b in prev_sub)
    prev_l = min(float(b["low"]) for b in prev_sub)
    
    rng = h - l
    prev_rng = prev_h - prev_l
    
    body = c - o
    h_expansion = h - prev_h # how much higher than previous bar's high
    c_expansion = c - prev_h # how much close exceeded previous high
    
    # 15s closes progression
    sub_c = [float(b["close"]) for b in sub]
    monotonic = all(sub_c[i] < sub_c[i+1] for i in range(3))
    
    print(f"19:{m} | Rng={rng:5.2f} | Body={body:+5.2f} | H_exp={h_expansion:+5.2f} | C_exp={c_expansion:+5.2f} | Rng/PrevRng={rng/prev_rng:4.2f} | Monotonic={str(monotonic):<5} | Closes={[round(x, 2) for x in sub_c]}")
