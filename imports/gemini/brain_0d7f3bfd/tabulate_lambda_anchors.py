import json
import numpy as np
import pandas as pd

with open(r'G:\trading\guias\analisis\C_dataset_verificado.json') as f:
    data = json.load(f)

with open(r'G:\trading\guias\analisis\C_evolucion87_resultados.json') as f:
    data13 = json.load(f)

# Collect all baseline cases where C is a multiple of 3 (or cluster center)
anchors = [
    {'name': '15:30 (12 Oct)', 'start': '15:30', 'bars': 21, 'C': 69, 'lambda': 1.15},
    {'name': '04:45 (12 Oct)', 'start': '04:45', 'bars': 21, 'C': 75, 'lambda': 1.25},
    {'name': '07:00 (12 Oct)', 'start': '07:00', 'bars': 21, 'C': 75, 'lambda': 1.25},
    {'name': '06:59 (12 Oct)', 'start': '06:59', 'bars': 22, 'C': 78, 'lambda': 1.30},
    {'name': '19:00 (13 Oct)', 'start': '19:00', 'bars': 21, 'C': 81, 'lambda': 1.35},
    {'name': '06:25 (13 Oct, n=22)', 'start': '06:25', 'bars': 22, 'C': 84, 'lambda': 1.40},
    {'name': '06:25 (13 Oct, n=21)', 'start': '06:25', 'bars': 21, 'C': 87, 'lambda': 1.45},
    {'name': '15:27 (12 Oct, n=25)', 'start': '15:27', 'bars': 25, 'C': 93, 'lambda': 1.55},
    {'name': '19:00 (12 Oct, n=22)', 'start': '19:00', 'bars': 22, 'C': 102, 'lambda': 1.70},
]

print("Cluster Center Anchors of Lambda = C / 60:")
print(f"{'Anchor':24s} | {'C':3s} | {'Lambda':6s} | {'Step index (k)':14s}")
print("-" * 55)
for a in anchors:
    k = round((a['lambda'] - 1.0) / 0.05)
    print(f"{a['name']:24s} | {a['C']:3d} | {a['lambda']:6.2f} | k = {k:2d} (1.0 + {k}*0.05)")
