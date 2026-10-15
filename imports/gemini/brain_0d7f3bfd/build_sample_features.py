import json, csv, math
from pathlib import Path
import numpy as np

# Let's load both 1m and 15s data
ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
c_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

ref_1m_path = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(ref_1m_path.open(encoding='utf-8-sig')))
c_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

# Also load C_matriz cases
mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
mat_cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

def ts(dt_str, date="2026-10-12"):
    from datetime import datetime
    return int(datetime.fromisoformat(f"{date}T{dt_str}+00:00").timestamp())

all_samples = []

# Add C_matriz cases
for c in mat_cases:
    # only integer C or n >= 21
    if c['bars'] >= 21:
        s_t = ts(c['START'])
        e_t = ts(c['END'])
        sub = [c_1m[t] for t in range(s_t, e_t + 1, 60) if t in c_1m]
        if sub:
            all_samples.append({
                'id': f"1m_{c['START'][:5]}_{c['END'][:5]}",
                'tf': 60,
                'bars': len(sub),
                'C': round(c['C'], 4),
                'sub': sub,
                's': c['START'],
                'e': c['END']
            })

# Add 15s cases
cases_15s = [
    ('18:52:00', '19:20:00', 67), ('18:53:00', '19:20:00', 118), ('18:54:00', '19:20:00', 123),
    ('18:54:15', '19:20:00', 118), ('18:54:30', '19:20:00', 67), ('18:54:45', '19:20:00', 67),
    ('18:55:00', '19:20:00', 106), ('18:55:15', '19:20:00', 66), ('18:55:30', '19:20:00', 88),
    ('18:55:45', '19:20:00', 88), ('18:56:00', '19:20:00', 106), ('18:56:15', '19:20:00', 67),
    ('18:56:30', '19:20:00', 67), ('18:56:45', '19:20:00', 79), ('18:57:00', '19:20:00', 67),
    ('19:01:00', '19:20:00', 47), ('19:02:00', '19:20:00', 47),
    ('18:55:00', '19:18:00', 88), ('18:55:00', '19:19:00', 115), ('18:55:00', '19:20:15', 79),
    ('18:55:00', '19:20:30', 67), ('18:55:00', '19:20:45', 66), ('18:55:00', '19:21:00', 115),
    ('18:55:00', '19:21:15', 106), ('18:55:00', '19:21:30', 79), ('18:55:00', '19:21:45', 66),
    ('18:55:00', '19:22:00', 106)
]

for s, e, C in cases_15s:
    s_t = ts(s)
    e_t = ts(e)
    sub = [c_15s[t] for t in range(s_t, e_t + 1, 15) if t in c_15s]
    if sub:
        all_samples.append({
            'id': f"15s_{s[:5]}_{e[:5]}",
            'tf': 15,
            'bars': len(sub),
            'C': float(C),
            'sub': sub,
            's': s,
            'e': e
        })

print(f"Total structured samples (n >= 21): {len(all_samples)}")

# Now compute comprehensive feature set
features_list = []
for samp in all_samples:
    sub = samp['sub']
    H = max(x['high'] for x in sub)
    L = min(x['low'] for x in sub)
    R = H - L
    O = sub[0]['open']
    C_first = sub[0]['close']
    C_last = sub[-1]['close']
    H_last = sub[-1]['high']
    L_last = sub[-1]['low']
    
    # Distance to extremes
    highs = [x['high'] for x in sub]
    lows = [x['low'] for x in sub]
    idx_H = highs.index(H)
    idx_L = lows.index(L)
    bars_since_H = len(sub) - 1 - idx_H
    bars_since_L = len(sub) - 1 - idx_L
    
    # Range ratios
    retrace = (C_last - L) / R if R > 0 else 0
    start_pos = (O - L) / R if R > 0 else 0
    move = (C_last - O) / R if R > 0 else 0
    
    # Volatility / true range
    tr = [max(h['high'] - h['low'], abs(h['high'] - prev['close']), abs(h['low'] - prev['close']))
          for h, prev in zip(sub[1:], sub[:-1])]
    sum_tr = sum(tr)
    atr = np.mean(tr) if tr else 0
    
    # Ratio of R to ATR
    r_atr = R / atr if atr > 0 else 0
    
    # Number of bars between H and L
    h_to_l = abs(idx_H - idx_L)
    
    features_list.append({
        'id': samp['id'],
        's': samp['s'],
        'e': samp['e'],
        'tf': samp['tf'],
        'bars': samp['bars'],
        'C': samp['C'],
        'H': H, 'L': L, 'R': R,
        'idx_H': idx_H, 'idx_L': idx_L,
        'bars_since_H': bars_since_H,
        'bars_since_L': bars_since_L,
        'retrace': retrace,
        'start_pos': start_pos,
        'move': move,
        'sum_tr': sum_tr,
        'atr': atr,
        'r_atr': r_atr,
        'h_to_l': h_to_l
    })

# Save features to scratch
out_p = Path(r"C:\Users\PC\.gemini\antigravity\brain\0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27\scratch\samples_features.json")
out_p.write_text(json.dumps(features_list, indent=2))
print("Saved features to scratch/samples_features.json")
