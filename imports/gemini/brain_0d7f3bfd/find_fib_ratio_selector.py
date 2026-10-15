import csv, json, datetime
from pathlib import Path
import numpy as np

# Load 1m candles
p_1m = Path('G:/trading/guias/analisis/character_manual_15m_1m.csv')
rows_1m = list(csv.DictReader(p_1m.open(encoding='utf-8-sig')))
candles_1m = {int(r['time']): {k: float(r[k]) for k in ('open','high','low','close')} for r in rows_1m}

def stamp(s, date="2026-10-12"):
    return int(datetime.datetime.fromisoformat(f"{date}T{s}+00:00").timestamp())

# Master test cases with n >= 21
cases = [
    # 1m Evening (12 Oct)
    ("18:50:00", "19:20:00", 118, 118/89),
    ("18:54:00", "19:20:00", 134, 134/89),
    ("18:55:00", "19:20:00", 62, 62/89),
    ("18:56:00", "19:20:00", 109, 109/89),
    ("18:57:00", "19:20:00", 77, 77/89),
    ("19:00:00", "19:20:00", 77, 77/89),
    ("19:00:00", "19:21:00", 102, 102/89),
    ("19:00:00", "19:22:00", 77, 77/89),
    ("19:11:00", "19:31:00", 80, 80/89),
    # 1m Morning (12 Oct)
    ("04:45:00", "05:05:00", 75, 75/89),
    ("04:45:05", "05:15:00", 116, 116/89),
    ("04:45:00", "05:25:00", 113, 113/89),
    ("04:45:00", "05:30:00", 110, 110/89),
]

print("=== SEARCHING FOR THE SELECTOR OF THE FIBONACCI RATIO (C / 89) ===")

results = []
for s_str, e_str, C, target_ratio in cases:
    t_s = stamp(s_str)
    t_e = stamp(e_str)
    sub = [candles_1m[t] for t in range(t_s, t_e + 60, 60) if t in candles_1m]
    if not sub:
        continue
    n = len(sub)
    highs = [b['high'] for b in sub]
    lows = [b['low'] for b in sub]
    closes = [b['close'] for b in sub]
    opens = [b['open'] for b in sub]
    
    H = max(highs)
    L = min(lows)
    Rng = H - L
    
    O_start = opens[0]
    C_end = closes[-1]
    
    # 1. Start candle position inside the range: (O_start - L) / Rng
    pos_start = (O_start - L) / Rng
    
    # 2. End candle position inside the range: (C_end - L) / Rng
    pos_end = (C_end - L) / Rng
    
    # 3. Net displacement ratio: abs(C_end - O_start) / Rng
    disp_ratio = abs(C_end - O_start) / Rng
    
    # 4. Retracement from extreme:
    # If bullish trend (C_end > O_start), retracement from high:
    # (H - min(lows after high)) / (H - L)
    idx_h = highs.index(H)
    idx_l = lows.index(L)
    
    # 5. Swing ratio: distance between global low and global high
    swing_bars = abs(idx_h - idx_l)
    swing_ratio = swing_bars / n
    
    # 6. First swing / impulse:
    first_move = abs(closes[1] - opens[0]) if n > 1 else 0
    first_ratio = first_move / Rng
    
    # 7. Range to bars:
    # Rng / n
    rng_per_bar = Rng / n
    
    results.append({
        'case': f"{s_str[:5]}->{e_str[:5]}",
        'C': C,
        'target': target_ratio,
        'pos_start': pos_start,
        'pos_end': pos_end,
        'disp_ratio': disp_ratio,
        'swing_ratio': swing_ratio,
        'rng_per_bar': rng_per_bar
    })

print(f"{'Case':12s} | {'C':3s} | {'Target (C/89)':13s} | {'Pos_Start':9s} | {'Disp/Rng':8s} | {'SwingRatio':10s} | {'Rng/Bar':7s}")
for r in results:
    print(f"{r['case']:12s} | {r['C']:3d} | {r['target']:13.4f} | {r['pos_start']:9.4f} | {r['disp_ratio']:8.4f} | {r['swing_ratio']:10.4f} | {r['rng_per_bar']:7.4f}")
