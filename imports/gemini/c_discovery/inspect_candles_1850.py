import json
import pandas as pd

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

# Find a case that covers 18:50 to 19:25 in 60s
case_60s = None
for c in master["cases"]:
    if c["dt"] == 60 and c["START"].startswith("2026-10-12T18:50"):
        case_60s = c
        break

if not case_60s:
    # Try 18:54
    for c in master["cases"]:
        if c["dt"] == 60 and c["START"].startswith("2026-10-12T18:54"):
            case_60s = c
            break

print("Found case:", case_60s["id"] if case_60s else "None")
if case_60s:
    df = pd.DataFrame(case_60s["OHLCV"])
    df['time_str'] = pd.to_datetime(df['time'], unit='s', utc=True).dt.strftime('%H:%M:%S')
    print(df[['time_str', 'open', 'high', 'low', 'close', 'volume']].to_string(index=False))
