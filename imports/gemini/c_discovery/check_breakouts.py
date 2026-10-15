# Check breakout bar for each END
from test_operator_candidates import df, idx_start

gt = {
    "19:23": 50,
    "19:24": 52,
    "19:25": 71,
    "19:26": 135,
    "19:27": 130,
    "19:28": 88,
    "19:29": 135,
    "19:30": 112,
    "19:31": 136,
    "19:32": 112,
    "19:33": 112,
    "19:34": 135,
    "19:35": 112,
}

for m, c_val in gt.items():
    end_idx = df[df["time_str"] == m].index[0]
    w = df.iloc[idx_start : end_idx + 1]
    r_high = w["high"].max()
    r_low = w["low"].min()
    
    # Look at subsequent bars to find first breakout bar by CLOSE
    future = df.iloc[end_idx + 1:].copy().reset_index(drop=True)
    break_bar = None
    break_time = None
    break_dir = None
    for _, fb in future.iterrows():
        if fb["close"] > r_high:
            break_bar = fb
            break_time = fb["time_str"]
            break_dir = "UP"
            break
        elif fb["close"] < r_low:
            break_bar = fb
            break_time = fb["time_str"]
            break_dir = "DOWN"
            break
    print(f"END={m} (n={len(w):2d}) | C={c_val:3d} | R_High={r_high:8.2f} | R_Low={r_low:8.2f} | 1st Breakout: {break_time} {break_dir}")
