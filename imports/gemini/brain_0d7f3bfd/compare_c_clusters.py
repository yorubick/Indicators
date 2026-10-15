import json
from pathlib import Path

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

c71_cases = [c for c in cases if abs(c['C'] - 71.0) < 1e-4]
c50_cases = [c for c in cases if abs(c['C'] - 50.0) < 1e-4]
c77_cases = [c for c in cases if abs(c['C'] - 77.0) < 1e-4]

print(f"Number of C=71 cases: {len(c71_cases)}")
for c in c71_cases:
    print(f"C=71: START={c['START']} END={c['END']} bars={c['bars']} H={c['high']} L={c['low']} R={c['high']-c['low']}")

print(f"\nNumber of C=50 cases: {len(c50_cases)}")
for c in c50_cases:
    print(f"C=50: START={c['START']} END={c['END']} bars={c['bars']} H={c['high']} L={c['low']} R={c['high']-c['low']}")

print(f"\nNumber of C=77 cases: {len(c77_cases)}")
for c in c77_cases:
    print(f"C=77: START={c['START']} END={c['END']} bars={c['bars']} H={c['high']} L={c['low']} R={c['high']-c['low']}")
