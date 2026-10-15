import json, csv, glob
from pathlib import Path

# Collect all cases across all files
cases = []

# 1. G:\trading\guias\analisis\C_matriz.json
p_mat = Path(r"G:\trading\guias\analisis\C_matriz.json")
if p_mat.exists():
    d = json.loads(p_mat.read_text(encoding='utf-8'))
    for c in d['cases']:
        cases.append({
            'source': 'C_matriz.json',
            'START': c['START'],
            'END': c['END'],
            'bars': c['bars'],
            'C': c['C'],
            'high': c['high'],
            'low': c['low'],
            'range': c['high'] - c['low'],
            'first_close': c['first_OHLC']['close'],
            'last_close': c['last_OHLC']['close'],
            'file': c.get('file', '')
        })

# 2. Check all Lite_*_comparacion.json in G:\trading\guias\analisis
for p in sorted(Path(r"G:\trading\guias\analisis").glob('Lite_*_comparacion.json')):
    try:
        j = json.loads(p.read_text(encoding='utf-8-sig'))
        s = j['START_UTC'][11:19]
        e = j['END_UTC'][11:19]
        cs = list(j['Lite_C_assuming_unrounded_family'].values())
        C = sum(cs)/len(cs)
        sec = j['chart_seconds']
        # calculate bars if we can
        # avoid duplicating C_matriz
        if not any(c['START'] == s and c['END'] == e and abs(c['C'] - C) < 1e-4 for c in cases):
            cases.append({
                'source': p.name,
                'START': s,
                'END': e,
                'bars': j.get('bars_in_range', None),
                'C': C,
                'chart_sec': sec,
                'file': str(p)
            })
    except Exception as ex:
        pass

# 3. Check master_cases.py in scratch
import sys
sys.path.append(r"C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch")
try:
    import master_cases
    # inspect master_cases
except Exception as e:
    pass

print(f"Total collected cases: {len(cases)}")
print("\n--- Summary of ALL unique C values for n >= 21 ---")
n21_cases = [c for c in cases if c.get('bars') is not None and c['bars'] >= 21]
c_vals = sorted(list(set(round(c['C'], 4) for c in n21_cases)))
print("Unique C values (n >= 21):", c_vals)

for cv in c_vals:
    matching = [c for c in n21_cases if abs(round(c['C'], 4) - cv) < 1e-4]
    print(f"\nC = {cv} ({len(matching)} occurrences):")
    for m in matching:
        print(f"  START={m['START']} END={m['END']} bars={m['bars']} High={m.get('high')} Low={m.get('low')} Range={m.get('range')}")
