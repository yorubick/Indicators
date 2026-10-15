import json
import pandas as pd
import numpy as np

master = json.load(open("master_all_C_cases.json", encoding="utf-8"))
cases_60 = [c for c in master["cases"] if c["dt"] == 60 and c["bars"] == 21]

print(f"Total n=21 (dt=60) cases: {len(cases_60)}")
print("-" * 75)
print(f"{'Case ID':<28} | {'C':<3} | {'base':<4} | {'diff':<5} | {'k*9':<6} | {'res':<4}")
print("-" * 75)

for c in sorted(cases_60, key=lambda x: round(x["C"])):
    c_val = round(c["C"])
    t_sec = 21 * 60
    base = round(t_sec / 18.3)
    diff = c_val - base
    k9 = round(diff / 9.0)
    res_k9 = diff - (k9 * 9)
    cid = c["id"]
    print(f"{cid:<28} | {c_val:<3} | {base:<4} | {diff:<+5} | {k9:+2d}*9  | {res_k9:<+4}")
