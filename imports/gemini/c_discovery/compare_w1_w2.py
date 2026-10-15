import csv
from pathlib import Path

ROOT = Path(r"G:\trading\guias\analisis\manual")

# Read rows
def read_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({k: float(r[k]) if k != 'time' else int(r[k]) for k in ['time', 'open', 'high', 'low', 'close', 'Volume']})
    return {r['time']: r for r in rows}

f_00 = read_csv(ROOT / "C_1s_plateau_n33_a.csv")
f_01 = read_csv(ROOT / "C_1s_start01_end33_a.csv")

# Range 1: 14:04:00 (1791986640) to 14:04:32 (1791986672) -> 33 bars, C = 2
w1_times = list(range(1791986640, 1791986672 + 1))
w1 = [f_00[t] for t in w1_times]

# Range 2: 14:04:01 (1791986641) to 14:04:33 (1791986673) -> 33 bars, C = 1
w2_times = list(range(1791986641, 1791986673 + 1))
w2 = [f_01[t] for t in w2_times]

print(f"Window 1 (14:04:00..14:04:32, n=33, C=2):")
print(f"  Start bar: {w1[0]}")
print(f"  End bar:   {w1[-1]}")
print(f"  High: {max(b['high'] for b in w1)}, Low: {min(b['low'] for b in w1)}")
print(f"  Net change: {w1[-1]['close'] - w1[0]['open']}")

print(f"\nWindow 2 (14:04:01..14:04:33, n=33, C=1):")
print(f"  Start bar: {w2[0]}")
print(f"  End bar:   {w2[-1]}")
print(f"  High: {max(b['high'] for b in w2)}, Low: {min(b['low'] for b in w2)}")
print(f"  Net change: {w2[-1]['close'] - w2[0]['open']}")

# Unique bars:
# Bar in W1 not in W2: 1791986640 (14:04:00)
# Bar in W2 not in W1: 1791986673 (14:04:33)
print("\nUnique Bar in W1 (14:04:00):", w1[0])
print("Unique Bar in W2 (14:04:33):", w2[-1])
