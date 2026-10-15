import csv
from pathlib import Path

ROOT = Path(r"G:\trading\guias\analisis\manual")

def read_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({k: float(r[k]) if k != 'time' else int(r[k]) for k in ['time', 'open', 'high', 'low', 'close', 'Volume']})
    return {r['time']: r for r in rows}

# Read 1s plateau sequence
# We have C_1s_plateau_n{n}_a.csv for n=21..40
c_values = {
    21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1,
    33: 2, 34: 1, 35: 1, 36: 2, 37: 2, 38: 2, 39: 2, 40: 2
}

print("1s Sequence (n=21..40) Detailed Structural Audit:")
print("=" * 80)

for n in range(21, 41):
    if n in [20, 21]:
        p = ROOT / f"C_1s_r1404_n{n}_a.csv"
    else:
        p = ROOT / f"C_1s_plateau_n{n}_a.csv"
    
    rows = read_csv(p)
    times = sorted(rows.keys())[:n]
    w = [rows[t] for t in times]
    
    w_h = max(b["high"] for b in w)
    w_l = min(b["low"] for b in w)
    w_rng = w_h - w_l
    
    end_c = w[-1]["close"]
    end_pos = (end_c - w_l) / w_rng
    
    idx_l = [b["low"] for b in w].index(w_l)
    age_l = n - 1 - idx_l
    
    # Net displacement
    net_disp = (end_c - w[0]["open"]) / w_rng
    
    T_183 = n / 18.3
    c_val = c_values[n]
    
    print(f"n={n:2d} | C={c_val} | T/18.3={T_183:.2f} | EndPos={end_pos:.3f} | AgeL={age_l:2d} | Low={w_l:.2f} | EndClose={end_c:.2f}")
