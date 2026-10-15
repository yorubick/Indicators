import csv, datetime
from pathlib import Path
import numpy as np

ref_15s_path = Path('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv')
rows_15s = list(csv.DictReader(ref_15s_path.open(encoding='utf-8-sig')))
candles_15s = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_15s}

def ts(t_str):
    return int(datetime.datetime.fromisoformat(f"2026-10-12T{t_str}+00:00").timestamp())

end_cases_15s = [
    ('19:20:00', 106),
    ('19:20:15', 79),
    ('19:20:30', 67),
    ('19:20:45', 66),
    ('19:21:00', 115),
    ('19:21:15', 106),
    ('19:21:30', 79),
    ('19:21:45', 66),
    ('19:22:00', 106),
]

t_start = ts('18:55:00')

print("Testing decay models on 15s END sweep:")
for e_str, C in end_cases_15s:
    t_end = ts(e_str)
    sub = [candles_15s[t] for t in range(t_start, t_end + 15, 15) if t in candles_15s]
    closes = np.array([b['close'] for b in sub])
    highs = np.array([b['high'] for b in sub])
    lows = np.array([b['low'] for b in sub])
    
    # 1. Kaufman ER
    net_c = abs(closes[-1] - closes[0])
    path = np.sum(np.abs(np.diff(closes)))
    er = net_c / path if path > 0 else 0
    
    # 2. Local ER over last 10 bars
    local_path = np.sum(np.abs(np.diff(closes[-10:])))
    local_net = abs(closes[-1] - closes[-10])
    local_er = local_net / local_path if local_path > 0 else 0
    
    # 3. Ratio of (High - Low) / path
    h_tot = highs.max()
    l_tot = lows.min()
    rng_path_ratio = (h_tot - l_tot) / path
    
    print(f"END {e_str} | C={C:3d} | ER={er:.4f} | Local_ER={local_er:.4f} | Rng/path={rng_path_ratio:.4f}")
