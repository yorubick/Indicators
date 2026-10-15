import csv
from pathlib import Path

ROOT = Path(r"G:\trading\guias\analisis\manual")

def read_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({k: float(r[k]) if k != 'time' else int(r[k]) for k in ['time', 'open', 'high', 'low', 'close', 'Volume']})
    return {r['time']: r for r in rows}

f_00 = read_csv(ROOT / "C_1s_plateau_n33_a.csv")
f_01 = read_csv(ROOT / "C_1s_start01_end33_a.csv")

# We have the 4 cases:
# (00, 32): 1791986640 to 1791986672 (n=33) -> C = 2
# (00, 33): 1791986640 to 1791986673 (n=34) -> C = 1
# (01, 32): 1791986641 to 1791986672 (n=32) -> C = 1
# (01, 33): 1791986641 to 1791986673 (n=33) -> C = 1

cases = [
    ("start00_end32", 1791986640, 1791986672, 33, 2),
    ("start00_end33", 1791986640, 1791986673, 34, 1),
    ("start01_end32", 1791986641, 1791986672, 32, 1),
    ("start01_end33", 1791986641, 1791986673, 33, 1),
]

print("Evaluating Invariant Discriminators on 2x2 Matrix:")
print("=" * 70)

for name, t_start, t_end, n_bars, C_obs in cases:
    source = f_00 if t_start == 1791986640 else f_01
    times = list(range(t_start, t_end + 1))
    w = [source[t] for t in times]
    
    # Invariant features:
    # 1. Net displacement ratio: (Close_end - Open_start) / (High_win - Low_win)
    w_h = max(b["high"] for b in w)
    w_l = min(b["low"] for b in w)
    w_rng = w_h - w_l
    net_disp = (w[-1]["close"] - w[0]["open"]) / w_rng
    
    # 2. Position of END close: (Close_end - Low_win) / Range
    pos_end_c = (w[-1]["close"] - w_l) / w_rng
    
    # 3. Position of START open: (Open_start - Low_win) / Range
    pos_start_o = (w[0]["open"] - w_l) / w_rng
    
    # 4. Bars since High and Low
    idx_h = [b["high"] for b in w].index(w_h)
    idx_l = [b["low"] for b in w].index(w_l)
    age_h = n_bars - 1 - idx_h
    age_l = n_bars - 1 - idx_l
    
    # 5. Ratio of upward bars to downward bars
    up_bars = sum(1 for b in w if b["close"] > b["open"])
    dn_bars = sum(1 for b in w if b["close"] < b["open"])
    
    # 6. Cumulative displacement: sum(close - open) / Range
    cum_body = sum(b["close"] - b["open"] for b in w) / w_rng
    
    print(f"{name:15s} | C={C_obs} n={n_bars} | NetDisp={net_disp:+.3f} | EndCPos={pos_end_c:.3f} | StartOPos={pos_start_o:.3f} | AgeH={age_h:2d} AgeL={age_l:2d} | Up={up_bars:2d} Dn={dn_bars:2d} | CumBody={cum_body:+.2f}")
