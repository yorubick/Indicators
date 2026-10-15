import json
from pathlib import Path
import numpy as np

p = Path("G:/trading/guias/analisis/C_dataset_verificado.json")
with open(p, "r", encoding="utf-8") as f:
    d = json.load(f)

c102 = [x for x in d["cases"] if x["id"] == "20261012_190000_192100_60s"][0]
c77  = [x for x in d["cases"] if x["id"] == "20261012_190100_192100_60s"][0]

print("=== Case 19:00 -> 19:21 (C=102) ===")
ohlc_A = c102["OHLC"]
print(f"n = {len(ohlc_A)}")
print(f"First candle (19:00): {ohlc_A[0]}")
print(f"Global High: {max(b['high'] for b in ohlc_A)} at index {np.argmax([b['high'] for b in ohlc_A])}")
print(f"Global Low:  {min(b['low'] for b in ohlc_A)} at index {np.argmin([b['low'] for b in ohlc_A])}")

print("\n=== Case 19:01 -> 19:21 (C=77) ===")
ohlc_B = c77["OHLC"]
print(f"n = {len(ohlc_B)}")
print(f"First candle (19:01): {ohlc_B[0]}")
print(f"Global High: {max(b['high'] for b in ohlc_B)} at index {np.argmax([b['high'] for b in ohlc_B])}")
print(f"Global Low:  {min(b['low'] for b in ohlc_B)} at index {np.argmin([b['low'] for b in ohlc_B])}")
