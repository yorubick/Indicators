import json
from pathlib import Path

# Load cases from C_matriz
mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

# Let's inspect the first 5 bars of [19:01, 19:22] vs [19:02, 19:22] vs [19:00, 19:22]
c_1900 = next(c for c in cases if c['START'] == '19:00:00' and c['END'] == '19:22:00')
c_1901 = next(c for c in cases if c['START'] == '19:01:00' and c['END'] == '19:22:00')
c_1902 = next(c for c in cases if c['START'] == '19:02:00' and c['END'] == '19:22:00')
c_1903 = next(c for c in cases if c['START'] == '19:03:00' and c['END'] == '19:23:00')
c_1904 = next(c for c in cases if c['START'] == '19:04:00' and c['END'] == '19:24:00')

print("=== COMPARING INITIAL BARS OF 19:00, 19:01, 19:02, 19:03, 19:04 ===")
for name, c in [('19:00', c_1900), ('19:01', c_1901), ('19:02', c_1902), ('19:03', c_1903), ('19:04', c_1904)]:
    print(f"\n--- START {name} (C = {c['C']}) ---")
    ohlc = c['OHLC']
    for idx, r in enumerate(ohlc[:6]):
        print(f"Bar {idx} [{r['time']}]: O={float(r['open']):.2f} H={float(r['high']):.2f} L={float(r['low']):.2f} C={float(r['close']):.2f}")
