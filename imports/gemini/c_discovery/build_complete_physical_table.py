import csv
from datetime import datetime, timezone

# Load 15s bars from C_barrido_15s_start1902.csv
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Build 1m bars
t_start = int(datetime(2026, 10, 12, 19, 3, 0, tzinfo=timezone.utc).timestamp())
t_end_max = int(datetime(2026, 10, 12, 19, 36, 0, tzinfo=timezone.utc).timestamp())

bars_1m = {}
for t in range(t_start, t_end_max + 60, 60):
    sub = [bars_15s[t + s] for s in [0, 15, 30, 45]]
    bars_1m[t] = {
        "open": float(sub[0]["open"]),
        "high": max(float(b["high"]) for b in sub),
        "low": min(float(b["low"]) for b in sub),
        "close": float(sub[3]["close"])
    }

cases = [
    {"n": 21, "m": 23, "C_1m": 50, "C_15s": 88},
    {"n": 22, "m": 24, "C_1m": 52, "C_15s": 67},
    {"n": 23, "m": 25, "C_1m": 71, "C_15s": 88},
    {"n": 24, "m": 26, "C_1m": 135, "C_15s": 88},
    {"n": 25, "m": 27, "C_1m": 130, "C_15s": 79},
    {"n": 26, "m": 28, "C_1m": 88, "C_15s": 102},
    {"n": 27, "m": 29, "C_1m": 135, "C_15s": 123},
    {"n": 28, "m": 30, "C_1m": 112, "C_15s": 67},
    {"n": 29, "m": 31, "C_1m": 136, "C_15s": 87},
    {"n": 30, "m": 32, "C_1m": 112, "C_15s": 106},
    {"n": 31, "m": 33, "C_1m": 112, "C_15s": 87},
    {"n": 32, "m": 34, "C_1m": 135, "C_15s": 123},
    {"n": 33, "m": 35, "C_1m": 112, "C_15s": 87},
]

print("=== COMPLETE 13-CASE PHYSICAL TABLE ===")
print(f"{'m':>2} | {'C_1m':>5} | {'C_15s':>5} | {'T (s)':>5} | {'T/18.3':>6} | {'Win_H':>8} | {'Win_L':>8} | {'Win_Rng':>7} | {'Bar_Rng':>7} | {'Bar_Close':>9} | {'(C-L)/Rng':>9}")
print("-" * 95)

running_high = -1e9
running_low = 1e9

for c in cases:
    m = c["m"]
    t = int(datetime(2026, 10, 12, 19, m, 0, tzinfo=timezone.utc).timestamp())
    b = bars_1m[t]
    
    # window up to t
    win_bars = [bars_1m[t_i] for t_i in range(t_start, t + 1, 60)]
    w_h = max(wb["high"] for wb in win_bars)
    w_l = min(wb["low"] for wb in win_bars)
    w_rng = w_h - w_l
    
    T = (t - t_start) # in seconds
    t_183 = T / 18.3
    
    bar_rng = b["high"] - b["low"]
    bar_pos = (b["close"] - b["low"]) / bar_rng if bar_rng > 0 else 0.5
    
    print(f"{m:>2} | {c['C_1m']:>5} | {c['C_15s']:>5} | {T:>5} | {t_183:>6.1f} | {w_h:>8.2f} | {w_l:>8.2f} | {w_rng:>7.2f} | {bar_rng:>7.2f} | {b['close']:>9.2f} | {bar_pos:>8.1%}")
