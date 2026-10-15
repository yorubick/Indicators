import csv

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

end_t = 1791832980 # 19:23:00

for start_m, c_val in [(0, 77), (1, 77), (2, 52), (3, 50)]:
    start_t = 1791831780 - (3 - start_m) * 60
    window = [rows[t] for t in sorted(rows.keys()) if start_t <= t <= end_t]
    highs = [float(r["high"]) for r in window]
    lows = [float(r["low"]) for r in window]
    w_high = max(highs)
    w_low = min(lows)
    start_row = rows[start_t]
    print(f"--- START 19:{start_m:02d} -> END 19:23 (C={c_val}) ---")
    print(f"Bars n = {len(window)}, Duration T = {len(window)*60} s")
    print(f"Window High = {w_high}, Low = {w_low}, Range = {w_high - w_low}")
    print(f"Start Candle: Open={start_row['open']}, High={start_row['high']}, Low={start_row['low']}, Close={start_row['close']}")
