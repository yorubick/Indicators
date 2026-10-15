import csv
from datetime import datetime, timezone
import numpy as np

# Load 15s bars from C_barrido_15s_start1902.csv
with open(r"G:\trading\guias\analisis\C_barrido_15s_start1902.csv", "r", encoding="utf-8") as f:
    r = csv.DictReader(f)
    bars_15s = {int(row["time"]): row for row in r}

# Build 1m bars from 18:50 to 19:40
t_start_build = int(datetime(2026, 10, 12, 18, 50, 0, tzinfo=timezone.utc).timestamp())
t_end_build = int(datetime(2026, 10, 12, 19, 40, 0, tzinfo=timezone.utc).timestamp())

bars_1m = []
for t in range(t_start_build, t_end_build + 60, 60):
    sub = [bars_15s[t + s] for s in [0, 15, 30, 45]]
    bars_1m.append({
        "time": t,
        "dt": datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"),
        "open": float(sub[0]["open"]),
        "high": max(float(b["high"]) for b in sub),
        "low": min(float(b["low"]) for b in sub),
        "close": float(sub[3]["close"]),
        "subbars": sub
    })

# Ground truth C values for 19:26 to 19:35 (n=24 to 33)
# In 1m: Peaks are 19:26, 19:29, 19:31, 19:34 (C in {135, 136})
# Baselines are 19:30, 19:32, 19:33, 19:35 (C == 112)
targets_1m = {
    "19:26": 1, # Peak (135)
    "19:27": 1, # High (130)
    "19:28": 0, # Drop (88)
    "19:29": 1, # Peak (135)
    "19:30": 0, # Baseline (112)
    "19:31": 1, # Peak (136)
    "19:32": 0, # Baseline (112)
    "19:33": 0, # Baseline (112)
    "19:34": 1, # Peak (135)
    "19:35": 0, # Baseline (112)
}

# In 15s: Peaks are 19:29, 19:32, 19:34 (C in {106, 123})
# Baselines are 19:30, 19:31, 19:33, 19:35 (C in {67, 87})
targets_15s = {
    "19:26": 0, # 88
    "19:27": 0, # 79
    "19:28": 0, # 102
    "19:29": 1, # 123
    "19:30": 0, # 67
    "19:31": 0, # 87
    "19:32": 1, # 106
    "19:33": 0, # 87
    "19:34": 1, # 123
    "19:35": 0, # 87
}

# Test hundreds of deterministic causal features
time_to_idx = {b["dt"]: i for i, b in enumerate(bars_1m)}

tested_rules = []

def eval_rule(name, condition_fn, targets):
    correct = 0
    total = len(targets)
    pred_dict = {}
    for dt_str, actual in targets.items():
        idx = time_to_idx[dt_str]
        pred = bool(condition_fn(idx))
        pred_dict[dt_str] = pred
        if (1 if pred else 0) == actual:
            correct += 1
    accuracy = correct / total
    return accuracy, pred_dict

# 1. Close above previous high
acc, p = eval_rule("close > high[1]", lambda i: bars_1m[i]["close"] > bars_1m[i-1]["high"], targets_1m)
tested_rules.append(("close > high[1]", acc, p))

# 2. Close above previous 2 highs
acc, p = eval_rule("close > max(high[1], high[2])", lambda i: bars_1m[i]["close"] > max(bars_1m[i-1]["high"], bars_1m[i-2]["high"]), targets_1m)
tested_rules.append(("close > max(high[1], high[2])", acc, p))

# 3. High is highest of window [START..END]
t_start = int(datetime(2026, 10, 12, 19, 3, 0, tzinfo=timezone.utc).timestamp())
i_start = time_to_idx["19:03"]
acc, p = eval_rule("high == highest(START..END)", lambda i: bars_1m[i]["high"] >= max(bars_1m[k]["high"] for k in range(i_start, i+1)), targets_1m)
tested_rules.append(("high == highest(START..END)", acc, p))

# 4. Close is highest close of window [START..END]
acc, p = eval_rule("close == highest_close(START..END)", lambda i: bars_1m[i]["close"] >= max(bars_1m[k]["close"] for k in range(i_start, i+1)), targets_1m)
tested_rules.append(("close == highest_close(START..END)", acc, p))

# 5. Upper wick < threshold * range
for thresh in [0.15, 0.20, 0.25, 0.30, 0.35]:
    acc, p = eval_rule(f"upper_wick < {thresh}*range", lambda i, th=thresh: (bars_1m[i]["high"] - max(bars_1m[i]["open"], bars_1m[i]["close"])) < th * (bars_1m[i]["high"] - bars_1m[i]["low"]), targets_1m)
    tested_rules.append((f"upper_wick < {thresh}*range", acc, p))

# 6. Body > 0 and close > high[1]
acc, p = eval_rule("body > 0 and close > high[1]", lambda i: (bars_1m[i]["close"] > bars_1m[i]["open"]) and (bars_1m[i]["close"] > bars_1m[i-1]["high"]), targets_1m)
tested_rules.append(("body > 0 and close > high[1]", acc, p))

# 7. Sub-bar feature: last 15s sub-bar close is above 15s sub-bar 0, 1, 2
acc, p = eval_rule("15s close[3] > max(close[0..2])", lambda i: bars_1m[i]["subbars"][3]["close"] > max(bars_1m[i]["subbars"][k]["close"] for k in range(3)), targets_1m)
tested_rules.append(("15s close[3] > max(close[0..2])", acc, p))

# 8. Range > ATR(14)
# calculate ATR
tr_list = []
for i in range(1, len(bars_1m)):
    tr = max(bars_1m[i]["high"] - bars_1m[i]["low"], abs(bars_1m[i]["high"] - bars_1m[i-1]["close"]), abs(bars_1m[i]["low"] - bars_1m[i-1]["close"]))
    tr_list.append(tr)

# Sort rules by accuracy on 1m
tested_rules.sort(key=lambda x: x[1], reverse=True)

print("=== TOP DISCRIMINATOR RULES ON 1M PEAKS (10 cases) ===")
for name, acc, p in tested_rules[:10]:
    fails = [dt for dt, actual in targets_1m.items() if (1 if p[dt] else 0) != actual]
    print(f"{name:<35} | Acc: {acc*100:>5.1f}% | Fails: {fails}")
