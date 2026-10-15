import csv

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

start_t = 1791831780 # 19:03:00

for end_m, c_val in [(23, 50), (24, 52), (25, 71)]:
    end_t = 1791831780 + (end_m - 3) * 60
    window = [rows[t] for t in sorted(rows.keys()) if start_t <= t <= end_t]
    highs = [float(r["high"]) for r in window]
    lows = [float(r["low"]) for r in window]
    w_high = max(highs)
    w_low = min(lows)
    end_row = rows[end_t]
    print(f"--- END 19:{end_m:02d} (C={c_val}) ---")
    print(f"Bars n = {len(window)}, Duration T = {len(window)*60} s")
    print(f"Window High = {w_high}, Low = {w_low}, Range = {w_high - w_low}")
    print(f"End Candle: Open={end_row['open']}, High={end_row['high']}, Low={end_row['low']}, Close={end_row['close']}")
    print(f"Did End candle make new Window High? {float(end_row['high']) == w_high}")
    print(f"Did End candle make new Window Low? {float(end_row['low']) == w_low}")
    print(f"T / 18.3 = {(len(window)*60)/18.3:.2f}")
