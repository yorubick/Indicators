import csv, json, datetime
from master_cases import dataset

print(f"{'START':8s} {'END':8s} {'dt':3s} | {'C':4s} {'bars':4s} | {'High':8s} {'Low':8s} {'Range':6s} {'Ticks':5s} | {'Open':8s} {'Close':8s}")
for d in dataset:
    h = d['high']
    l = d['low']
    rng = d['range']
    ticks = rng / 0.25
    o = d['open']
    c = d['close']
    print(f"{d['s']:8s} {d['e']:8s} {d['dt']:3d} | {d['C']:4d} {d['bars']:4d} | {h:8.2f} {l:8.2f} {rng:6.2f} {ticks:5.0f} | {o:8.2f} {c:8.2f}")
