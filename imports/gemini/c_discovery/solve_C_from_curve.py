import json
from scipy.optimize import brentq

# Load candles
with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

# Collect all 60s bars for Oct 12
bars_by_time = {}
for c in master["cases"]:
    if c.get("dt") == 60 and "2026-10-12" in c.get("START", ""):
        for b in c.get("OHLCV", []):
            bars_by_time[b["time"]] = b

from datetime import datetime, timezone
times = sorted(bars_by_time.keys())
time_map = {datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"): t for t in times}

def simulate_curve(start_str, end_str, C_val, lane_name, eval_time_str):
    t_start = time_map[start_str]
    t_end = time_map[end_str]
    t_eval = time_map[eval_time_str]
    dt = 60.0
    
    # base factors
    factors = {
        "Lane 3 A": 24.0,           # Lane A Fast
        "Lane 3 B": 89.0 / 3.0,     # Lane A Slow
        "Lane 2 A": 8.0,            # Lane B Fast
        "Lane 2 B": 89.0 / 9.0,     # Lane B Slow
        "Lane 1 A": 72.0 / 27.0,    # Lane C Fast
        "Lane 1 B": 89.0 / 27.0,    # Lane C Slow
    }
    b0 = factors[lane_name]
    alpha = 2.0 / ((b0 * C_val / dt) + 1.0)
    
    # Find end bar
    # In bull breakout, seed is end candle low
    end_bar = bars_by_time[t_end]
    state = float(end_bar["low"])
    
    # Post end bars up to eval_time
    eval_bars = [bars_by_time[t] for t in times if t_end < t <= t_eval]
    for b in eval_bars:
        c = float(b["close"])
        state += alpha * (c - state)
        
    return state

def solve_C(start_str, end_str, lane_name, observed_val, eval_time_str):
    def f(c):
        return simulate_curve(start_str, end_str, c, lane_name, eval_time_str) - observed_val
    try:
        sol = brentq(f, 20.0, 500.0)
        return sol
    except Exception as e:
        # Fallback to grid search
        best_c = None
        best_diff = 1e9
        for c_cand in range(20, 500):
            diff = abs(simulate_curve(start_str, end_str, float(c_cand), lane_name, eval_time_str) - observed_val)
            if diff < best_diff:
                best_diff = diff
                best_c = c_cand
        return float(best_c)

if __name__ == "__main__":
    # Test with user verified case: START 19:03, END 19:26, eval 19:30
    # Lane 1 A: 30873.03
    # Lane 2 A: 30869.92
    # Lane 3 A: 30868.26
    c_sol_1a = solve_C("19:03", "19:26", "Lane 1 A", 30873.03, "19:30")
    c_sol_2a = solve_C("19:03", "19:26", "Lane 2 A", 30869.92, "19:30")
    c_sol_3a = solve_C("19:03", "19:26", "Lane 3 A", 30868.26, "19:30")
    print(f"Solved C from Lane 1 A (30873.03): {c_sol_1a:.4f} -> round: {round(c_sol_1a)}")
    print(f"Solved C from Lane 2 A (30869.92): {c_sol_2a:.4f} -> round: {round(c_sol_2a)}")
    print(f"Solved C from Lane 3 A (30868.26): {c_sol_3a:.4f} -> round: {round(c_sol_3a)}")
