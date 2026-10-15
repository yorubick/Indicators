import json
from pathlib import Path

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

c_1900_20 = next(c for c in cases if c['START'] == '19:00:00' and c['END'] == '19:20:00')
c_1900_21 = next(c for c in cases if c['START'] == '19:00:00' and c['END'] == '19:21:00')
c_1900_22 = next(c for c in cases if c['START'] == '19:00:00' and c['END'] == '19:22:00')

c_1904_27 = next(c for c in cases if c['START'] == '19:04:00' and c['END'] == '19:27:00')
c_1904_28 = next(c for c in cases if c['START'] == '19:04:00' and c['END'] == '19:28:00')
c_1904_29 = next(c for c in cases if c['START'] == '19:04:00' and c['END'] == '19:29:00')

print("--- COMPARE 19:00 -> 19:20 vs 19:21 vs 19:22 ---")
for c in [c_1900_20, c_1900_21, c_1900_22]:
    lc = c['last_OHLC']
    print(f"END={c['END']} C={c['C']:6.2f} High={c['high']:8.2f} Low={c['low']:8.2f} LastOHLC={lc}")

print("\n--- COMPARE 19:04 -> 19:27 vs 19:28 vs 19:29 ---")
for c in [c_1904_27, c_1904_28, c_1904_29]:
    lc = c['last_OHLC']
    print(f"END={c['END']} C={c['C']:6.2f} High={c['high']:8.2f} Low={c['low']:8.2f} LastOHLC={lc}")
