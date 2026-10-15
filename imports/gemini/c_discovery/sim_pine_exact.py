import csv

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

sorted_times = sorted(rows.keys())

# Pine script exact logic simulation
start_time = 1791831780 # 19:03
end_time   = 1791832980 # 19:23

C = 50.0
dt = 60.0
alpha_a_fast = 2.0 / ((24.0 * C / dt) + 1.0)
alpha_a_slow = 2.0 / (( (89.0/3.0) * C / dt) + 1.0)
alpha_b_fast = 2.0 / ((8.0 * C / dt) + 1.0)
alpha_b_slow = 2.0 / (((89.0/9.0) * C / dt) + 1.0)
alpha_c_fast = 2.0 / (((72.0/27.0) * C / dt) + 1.0)
alpha_c_slow = 2.0 / (((89.0/27.0) * C / dt) + 1.0)

# Simulate Pine variables
range_high = None
range_low = None
end_candle_high = None
end_candle_low = None

state_bull_a_fast = None
state_bull_a_slow = None
state_bull_b_fast = None
state_bull_b_slow = None
state_bull_c_fast = None
state_bull_c_slow = None

has_broken_out = False
breakout_dir = 0
chosen_seed = None

for i, t in enumerate(sorted_times):
    time = t
    time_1 = sorted_times[i-1] if i > 0 else 0
    row = rows[t]
    h = float(row["high"])
    l = float(row["low"])
    close = float(row["close"])
    
    is_in_range = time >= start_time and time <= end_time
    is_start_bar = (time == start_time) or (time > start_time and time_1 < start_time)
    is_end_bar = (time == end_time) or (time > end_time and time_1 <= end_time)
    is_post_end = time > end_time
    
    if time < start_time:
        range_high = None
        range_low = None
    elif is_in_range:
        if is_start_bar:
            range_high = h
            range_low = l
        else:
            range_high = max(range_high, h)
            range_low = min(range_low, l)
            
    if is_end_bar:
        end_candle_high = h
        end_candle_low = l
        has_broken_out = False
        breakout_dir = 0
        state_bull_a_fast = end_candle_low
        state_bull_a_slow = end_candle_low
        state_bull_b_fast = end_candle_low
        state_bull_b_slow = end_candle_low
        state_bull_c_fast = end_candle_low
        state_bull_c_slow = end_candle_low
        print(f"Bar {t}: is_end_bar=True, end_candle_low={end_candle_low}")
        
    if is_post_end:
        state_bull_a_fast += alpha_a_fast * (close - state_bull_a_fast)
        state_bull_a_slow += alpha_a_slow * (close - state_bull_a_slow)
        state_bull_b_fast += alpha_b_fast * (close - state_bull_b_fast)
        state_bull_b_slow += alpha_b_slow * (close - state_bull_b_slow)
        state_bull_c_fast += alpha_c_fast * (close - state_bull_c_fast)
        state_bull_c_slow += alpha_c_slow * (close - state_bull_c_slow)
        
        if not has_broken_out:
            if close > range_high:
                has_broken_out = True
                breakout_dir = 1
                chosen_seed = end_candle_low
                print(f"BREAKOUT AT {t}: close={close} > range_high={range_high}")
            elif close < range_low:
                has_broken_out = True
                breakout_dir = -1
                chosen_seed = end_candle_high
                
        if t == 1791833160: # 19:26:00
            print("\n--- RESULTS AT 19:26 IN SIMULATED PINE ---")
            print(f"Lane A fast: {state_bull_a_fast:.2f}")
            print(f"Lane A slow: {state_bull_a_slow:.2f}")
            print(f"Lane B fast: {state_bull_b_fast:.2f}")
            print(f"Lane B slow: {state_bull_b_slow:.2f}")
            print(f"Lane C fast: {state_bull_c_fast:.2f}")
            print(f"Lane C slow: {state_bull_c_slow:.2f}")
