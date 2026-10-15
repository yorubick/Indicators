import csv
import pandas as pd
import numpy as np

# Load the exact 1m candles for Oct 12
rows = []
with open(r"G:\trading\guias\analisis\manual\Lite_1904_193000_1m_b.csv", "r") as f:
    for r in csv.DictReader(f):
        rows.append({
            "time": int(r["time"]),
            "open": float(r["open"]),
            "high": float(r["high"]),
            "low": float(r["low"]),
            "close": float(r["close"]),
            "volume": float(r.get("volume", 0.0) if r.get("volume") and r.get("volume") != "" else 0.0)
        })

df = pd.DataFrame(rows).sort_values("time").reset_index(drop=True)
from datetime import datetime, timezone
df["time_str"] = df["time"].apply(lambda t: datetime.fromtimestamp(t, tz=timezone.utc).strftime("%H:%M"))
df["date_str"] = df["time"].apply(lambda t: datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y-%m-%d"))
df = df[df["date_str"] == "2026-10-12"].reset_index(drop=True)

# Also let's check volume from master_all_C_cases if available
import json
with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

# Find 60s bars for 19:03
vol_map = {}
for c in master["cases"]:
    if c.get("dt") == 60:
        for b in c.get("OHLCV", []):
            vol_map[b["time"]] = b.get("volume", 0.0)

for idx, r in df.iterrows():
    if r["time"] in vol_map:
        df.at[idx, "volume"] = vol_map[r["time"]]

# Ground truth:
gt = {
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

start_idx = df[df["time_str"] == "19:03"].index[0]

table = []
for m, c_val in gt.items():
    end_idx = df[df["time_str"] == m].index[0]
    w = df.iloc[start_idx : end_idx + 1].copy().reset_index(drop=True)
    
    b = w.iloc[-1]
    prev = w.iloc[-2]
    
    # Range
    r_high = w["high"].max()
    r_low = w["low"].min()
    
    # Extreme indices
    idx_h = w["high"].idxmax()
    idx_l = w["low"].idxmin()
    bars_since_high = len(w) - 1 - idx_h
    bars_since_low = len(w) - 1 - idx_l
    
    # Price relations
    c = b["close"]
    o = b["open"]
    h = b["high"]
    l = b["low"]
    v = b["volume"]
    
    table.append({
        "END": m,
        "n": len(w),
        "C": c_val,
        "Open": o,
        "High": h,
        "Low": l,
        "Close": c,
        "Vol": v,
        "H_max": r_high,
        "L_min": r_low,
        "b_since_H": bars_since_high,
        "b_since_L": bars_since_low,
        "dist_H": r_high - c,
        "dist_L": c - r_low,
        "body": c - o,
        "rng": h - l,
    })

res = pd.DataFrame(table)
print(res.to_string())
