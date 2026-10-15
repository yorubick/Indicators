import csv
from datetime import datetime, timezone

rows = {}
with open(r"G:\trading\guias\analisis\manual\Lite_1904_193000_1m_b.csv", "r") as f:
    for r in csv.DictReader(f):
        t = int(r["time"])
        dt_val = datetime.fromtimestamp(t, tz=timezone.utc)
        if dt_val.strftime("%Y-%m-%d") == "2026-10-12":
            rows[t] = r

sorted_times = sorted(rows.keys())
time_map = {datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"): t for t in sorted_times}

t_start = time_map["19:03"]

c_map = {
    "19:25": 71,
    "19:26": 135,
    "19:27": 130,
    "19:28": 88,
    "19:29": 135,
    "19:30": 112,
    "19:31": 136,
}

def analyze_window(end_m):
    t_end = time_map[end_m]
    w = [rows[t] for t in sorted_times if t_start <= t <= t_end]
    n = len(w)
    h_max = max(float(b["high"]) for b in w)
    l_min = min(float(b["low"]) for b in w)
    rng = h_max - l_min
    
    eb = w[-1]
    eb_o, eb_h, eb_l, eb_c = float(eb["open"]), float(eb["high"]), float(eb["low"]), float(eb["close"])
    
    s_open = float(w[0]["open"])
    disp = eb_c - s_open
    
    h_idx = max(i for i, b in enumerate(w) if float(b["high"]) == h_max)
    l_idx = min(i for i, b in enumerate(w) if float(b["low"]) == l_min)
    bars_since_h = (n - 1) - h_idx
    bars_since_l = (n - 1) - l_idx
    
    norm_c = (eb_c - l_min) / rng
    
    # Delta from previous bar
    prev_b = w[-2]
    prev_h = float(prev_b["high"])
    prev_l = float(prev_b["low"])
    prev_c = float(prev_b["close"])
    
    # Cumulative bar by bar path
    path = sum(abs(float(w[i]["close"]) - float(w[i-1]["close"])) for i in range(1, len(w)))
    
    # High expansion delta: how much did High increase compared to max high of previous bars?
    h_prev_bars = max(float(b["high"]) for b in w[:-1])
    h_expansion = eb_h - h_prev_bars
    
    # Close expansion delta: did Close break the previous max high?
    c_break = eb_c - h_prev_bars
    
    return {
        "end": end_m, "C": c_map[end_m], "n": n, "rng": rng, "h": h_max, "l": l_min,
        "bars_since_h": bars_since_h, "bars_since_l": bars_since_l,
        "norm_c": norm_c, "disp": disp, "eb_c": eb_c, "eb_h": eb_h,
        "h_expansion": h_expansion, "c_break": c_break, "path": path,
        "er": disp / path if path > 0 else 0
    }

print(f"{'END':5} | {'C':3} | {'n':2} | {'Rng':5} | {'H_exp':5} | {'C_break':7} | {'norm_C':6} | {'ER':5} | {'Path':5}")
print("-" * 65)
for m in sorted(c_map.keys()):
    d = analyze_window(m)
    print(f"{d['end']:5} | {d['C']:3d} | {d['n']:2d} | {d['rng']:5.2f} | {d['h_expansion']:+5.2f} | {d['c_break']:+7.2f} | {d['norm_c']:6.3f} | {d['er']:5.3f} | {d['path']:5.2f}")
