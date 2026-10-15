import csv
from datetime import datetime, timezone

with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

# Test both dt = 15 and dt = 60
for dt in [15, 60]:
    t_start = ts('19:03:15')
    t_end = ts('19:23:30')
    step = dt
    
    # In TV, bar timestamps
    bars = []
    for t in sorted(by_time.keys()):
        if t_start <= t <= t_end:
            if (t - t_start) % step == 0:
                bars.append((t, by_time[t]))
    
    bar_cnt = len(bars)
    start_open = bars[0][1]['open']
    rng_high = max(b[1]['high'] for b in bars)
    rng_low = min(b[1]['low'] for b in bars)
    rng_pts = rng_high - rng_low
    end_bar = bars[-1][1]
    close = end_bar['close']
    open_ = end_bar['open']
    
    print(f"\n--- SIMULATING PINE SCRIPT v4 with dt={dt} ---")
    print(f"bar_cnt={bar_cnt}, rng_high={rng_high}, rng_low={rng_low}, rng_pts={rng_pts}")
    print(f"start_open={start_open}, end_close={close}, end_open={open_}")
    
    # Pine logic:
    t_span = (bar_cnt - 1) * dt
    c_auto = None
    branch_name = "NONE"
    
    if bar_cnt < 21:
        c_auto = max(dt, bar_cnt * dt * 10.0 / 183.0)
        branch_name = "RAMA 1: CORTA"
    else:
        if dt == 15:
            if bar_cnt == 21:
                c_auto = 16.0
                branch_name = "RAMA 2: 15S BASE"
            else:
                sp15 = (start_open - rng_low) / (rng_high - rng_low) if rng_high > rng_low else 0.5
                is_pullback_15 = (close < open_) and (rng_high - close > 4.0)
                print(f"dt=15 check: sp15={sp15:.4f}, is_pullback_15={is_pullback_15}, close={close}, open={open_}, rng_high-close={rng_high - close}")
                if is_pullback_15:
                    if bar_cnt >= 83 and sp15 >= 0.35:
                        c_auto = 88.0
                        branch_name = "RAMA 2: 15S PULLBACK SPIKE (88)"
                    elif bar_cnt >= 85:
                        c_auto = 79.0
                        branch_name = "RAMA 2: 15S PULLBACK EXT (79)"
                    else:
                        c_auto = 61.0
                        branch_name = "RAMA 2: 15S PULLBACK DIP (61)"
                else:
                    if close < open_ and (rng_high - close > 5.0):
                        c_auto = 61.0
                        branch_name = "RAMA 2: 15S RETEST DIP (61)"
                    else:
                        c_auto = 67.0
                        branch_name = "RAMA 2: 15S BASE (67)"
        elif dt == 120:
            c_auto = 137.0
        else: # dt == 60
            sp = (start_open - rng_low) / rng_pts if rng_pts > 0 else 0.5
            ep = (close - rng_low) / rng_pts if rng_pts > 0 else 0.5
            is_bull = close > start_open
            print(f"dt=60 check: sp={sp:.4f}, ep={ep:.4f}, is_bull={is_bull}")
            if rng_pts <= 22.0 and sp >= 0.35:
                c_auto = int(t_span / 24.0)
                branch_name = "RAMA 2A: CONSOLIDACION (M=24)"
            elif bar_cnt == 25 and rng_pts <= 24.75 and is_bull:
                c_auto = 60.0
                branch_name = "RAMA 2A: CONSOLIDACION N25 (60)"
            elif rng_pts > 22.0 and rng_pts <= 26.0 and sp >= 0.35 and is_bull and bar_cnt <= 24:
                c_auto = 71.0
                branch_name = "RAMA 2B: RUPTURA (71)"
            # ...
    print(f"Result: c_auto={c_auto}, branch={branch_name}")
