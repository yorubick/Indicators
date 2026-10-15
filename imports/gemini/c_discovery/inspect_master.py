import json
from collections import Counter

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master["cases"]
print("Measurement kinds:", Counter(c.get("C_measurement_kind") for c in cases))
print("dt counts:", Counter(c.get("dt") for c in cases))
print("bars distribution (min, max):", min(c.get("bars") for c in cases), max(c.get("bars") for c in cases))

short_cases = [c for c in cases if c.get("bars") < 21]
long_cases = [c for c in cases if c.get("bars") >= 21]
print(f"Short cases (bars < 21): {len(short_cases)}")
print(f"Long cases (bars >= 21): {len(long_cases)}")

short_diffs = []
for c in short_cases:
    dt = c["dt"]
    n = c["bars"]
    # Formula: max(dt, n * dt * 10 / 183)
    pred_cont = max(dt, n * dt * 10 / 183)
    pred_round = max(dt, round(n * dt * 10 / 183))
    c_lite = c.get("C_Lite")
    c_val = c.get("C")
    if c_lite is not None:
        short_diffs.append((abs(c_lite - pred_cont), c["id"], n, dt, c_lite, pred_cont))
    else:
        # Check against Character interval
        interval = c.get("C_Character_interval")
        # print interval
        pass

print(f"Short cases with C_Lite: {len(short_diffs)}")
max_diff = max(d[0] for d in short_diffs)
print(f"Max diff for short cases with C_Lite vs continuous formula: {max_diff:.8e}")
for d in short_diffs:
    if d[0] > 1e-4:
        print(f"  Diff > 1e-4: {d}")

# Let's inspect long cases
print("\n--- Long cases summary ---")
print(f"Total long cases: {len(long_cases)}")
long_with_lite = [c for c in long_cases if c.get("C_Lite") is not None]
print(f"Long cases with C_Lite: {len(long_with_lite)}")
long_char_only = [c for c in long_cases if c.get("C_Lite") is None]
print(f"Long cases Character only: {len(long_char_only)}")
