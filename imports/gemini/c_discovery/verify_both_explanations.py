import json
import pandas as pd
import numpy as np

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = {c['id']: c for c in master['cases']}

print("="*70)
print("TEST 1: CAN AN ANCHOR BEFORE 'START' EXPLAIN C?")
print("="*70)

# Cases with fixed END = 19:20:00
end_1920_cases = []
for cid, c in cases.items():
    if '19:20:00' in c.get('END', '') and c.get('C_Lite') is not None and c['bars'] >= 21:
        end_1920_cases.append({
            'id': cid,
            'START': c['START'].split('T')[1][:8],
            'dt': c['dt'],
            'bars': c['bars'],
            'C': round(c['C_Lite']),
            'req_sec': round(c['C_Lite'] * 18.3),
            'window_sec': c['bars'] * c['dt'],
            'diff_sec': round(c['C_Lite'] * 18.3) - (c['bars'] * c['dt'])
        })

df_1920 = pd.DataFrame(end_1920_cases).sort_values(by=['dt', 'START'])
print("Cases with fixed END 19:20:00:")
print(df_1920.to_string(index=False))

print("\n" + "="*70)
print("TEST 2: QUANTIZATION AND DISCRETE HARMONIC LADDER")
print("="*70)

with open(r"G:\trading\guias\analisis\C_barrido_END_1855_1920_1924_15s.json", "r", encoding="utf-8") as f:
    barrido = json.load(f)

b_cases = barrido["cases"]
b_c = [round(c["C_Lite"]) for c in b_cases]
b_times = [c["END"].split("T")[1][:8] for c in b_cases]

jumps = []
for i in range(len(b_c) - 1):
    diff = b_c[i+1] - b_c[i]
    is_mult_3 = (diff % 3 == 0)
    is_mult_9 = (diff % 9 == 0)
    is_mult_27 = (diff % 27 == 0)
    jumps.append({
        'from_time': b_times[i],
        'to_time': b_times[i+1],
        'from_C': b_c[i],
        'to_C': b_c[i+1],
        'diff': diff,
        'abs_diff': abs(diff),
        'mult_3': is_mult_3,
        'mult_9': is_mult_9,
        'mult_27': is_mult_27
    })

df_jumps = pd.DataFrame(jumps)
print("Transitions in 17-bar END sweep:")
print(df_jumps.to_string(index=False))

print(f"\nTotal jumps: {len(df_jumps)}")
print(f"Jumps multiple of 3: {df_jumps['mult_3'].sum()} / {len(df_jumps)} ({df_jumps['mult_3'].sum()/len(df_jumps)*100:.1f}%)")
print(f"Jumps multiple of 9: {df_jumps['mult_9'].sum()} / {len(df_jumps)} ({df_jumps['mult_9'].sum()/len(df_jumps)*100:.1f}%)")
print(f"Jumps multiple of 27: {df_jumps['mult_27'].sum()} / {len(df_jumps)} ({df_jumps['mult_27'].sum()/len(df_jumps)*100:.1f}%)")
