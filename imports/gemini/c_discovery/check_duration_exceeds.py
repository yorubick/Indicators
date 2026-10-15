import json
import pandas as pd

with open(r'G:\trading\guias\analisis\master_all_C_cases.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

cases = master['cases']
long_cases = [c for c in cases if c['bars'] >= 21 and c.get('C_Lite') is not None]

exceeds_count = 0
smaller_count = 0
equal_count = 0

rows = []
for c in long_cases:
    n = c['bars']
    dt = c['dt']
    total_sec = n * dt
    c_val = c['C_Lite']
    req_sec = c_val * 18.3
    req_bars = req_sec / dt
    
    diff_bars = req_bars - n
    if diff_bars > 0.5:
        exceeds_count += 1
    elif diff_bars < -0.5:
        smaller_count += 1
    else:
        equal_count += 1
        
    rows.append({
        'id': c['id'],
        'dt': dt,
        'n': n,
        'C': c_val,
        'total_sec': total_sec,
        'req_sec': req_sec,
        'req_bars': round(req_bars, 1),
        'diff_bars': round(diff_bars, 1)
    })

df = pd.DataFrame(rows)
print(f"Total long cases: {len(long_cases)}")
print(f"Cases where required bars > window bars: {exceeds_count} ({exceeds_count/len(long_cases)*100:.1f}%)")
print(f"Cases where required bars < window bars: {smaller_count} ({smaller_count/len(long_cases)*100:.1f}%)")
print(f"Cases where required bars == window bars: {equal_count} ({equal_count/len(long_cases)*100:.1f}%)")

print("\nSample where required bars > window bars:")
print(df[df['diff_bars'] > 5].head(15).to_string())
