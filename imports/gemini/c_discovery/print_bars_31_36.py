from pathlib import Path
import csv

ROOT = Path(r"G:\trading\guias\analisis\manual")
def read_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({k: float(r[k]) if k != 'time' else int(r[k]) for k in ['time', 'open', 'high', 'low', 'close', 'Volume']})
    return {r['time']: r for r in rows}

r35 = read_csv(ROOT / 'C_1s_plateau_n35_a.csv')
times = sorted(r35.keys())[:36]
for i in range(30, 36):
    b = r35[times[i]]
    print(f"Bar {i+1:2d} (t={b['time']}): O={b['open']:8.2f} H={b['high']:8.2f} L={b['low']:8.2f} C={b['close']:8.2f} V={b['Volume']:3.0f}")
