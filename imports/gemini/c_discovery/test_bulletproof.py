import csv

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows[int(r["time"])] = r

sorted_times = sorted(rows.keys())

start_time = 1791831780 # 19:03
end_time   = 1791832980 # 19:23
dt = 60

C = 50.0
alpha_a_fast = 2.0 / ((24.0 * C / dt) + 1.0)
alpha_a_slow = 2.0 / (( (89.0/3.0) * C / dt) + 1.0)
alpha_b_fast = 2.0 / ((8.0 * C / dt) + 1.0)
alpha_b_slow = 2.0 / (((89.0/9.0) * C / dt) + 1.0)
alpha_c_fast = 2.0 / (((72.0/27.0) * C / dt) + 1.0)
alpha_c_slow = 2.0 / (((89.0/27.0) * C / dt) + 1.0)

end_bar_index = None
state_bull_a_fast = None
state_bull_a_slow = None
state_bull_b_fast = None
state_bull_b_slow = None
state_bull_c_fast = None
state_bull_c_slow = None

range_high = None
range_low = None
has_broken_out = False

for bar_index, t in enumerate(sorted_times):
    time = t
    time_1 = sorted_times[bar_index - 1] if bar_index > 0 else 0
    row = rows[t]
    h = float(row["high"])
    l = float(row["low"])
    close = float(row["close"])
    
    is_in_range = time >= start_time and time <= end_time
    is_start_bar = time >= start_time and (time_1 < start_time or bar_index == 0)
    is_end_bar = (time <= end_time) and (time + dt > end_time)
    
    if is_in_range:
        if is_start_bar:
            range_high = h
            range_low = l
        else:
            range_high = max(range_high, h)
            range_low = min(range_low, l)
            
    if is_end_bar:
        end_bar_index = bar_index
        end_candle_high = h
        end_candle_low = l
        state_bull_a_fast = end_candle_low
        state_bull_a_slow = end_candle_low
        state_bull_b_fast = end_candle_low
        state_bull_b_slow = end_candle_low
        state_bull_c_fast = end_candle_low
        state_bull_c_slow = end_candle_low
        
    is_post_end = (end_bar_index is not None) and (bar_index > end_bar_index)
    
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
                
        if t == 1791833160: # 19:26:00
            print("--- COMPARING AT 19:26:00 ---")
            lanes = [
                ("Lane 3 A (Fast A)", state_bull_a_fast, float(rows[t]['Lane 3 A'])),
                ("Lane 3 B (Slow A)", state_bull_a_slow, float(rows[t]['Lane 3 B'])),
                ("Lane 2 A (Fast B)", state_bull_b_fast, float(rows[t]['Lane 2 A'])),
                ("Lane 2 B (Slow B)", state_bull_b_slow, float(rows[t]['Lane 2 B'])),
                ("Lane 1 A (Fast C)", state_bull_c_fast, float(rows[t]['Lane 1 A'])),
                ("Lane 1 B (Slow C)", state_bull_c_slow, float(rows[t]['Lane 1 B'])),
            ]
            for name, val, off in lanes:
                diff = abs(val - off)
                print(f"{name:18s} | Pine: {val:10.5f} | Official: {off:10.5f} | Diff: {diff:.2e}")
