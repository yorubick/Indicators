import json
import pandas as pd
import numpy as np

d14 = json.load(open('data/ohlcv_2m_14oct_1400_1454.json'))
df14 = pd.DataFrame(d14)

d12 = json.load(open('data/ohlcv_2m_1430_1516.json'))
df12 = pd.DataFrame(d12)

d15 = json.load(open('data/ohlcv_2m_15oct_1400_1456.json'))
df15 = pd.DataFrame(d15)

all_cases = [
    {'name': '15-Oct 14:56', 'df': df15.iloc[:29], 'C': 227, 'T': 3360, 'n': 29},
    {'name': '14-Oct 14:56', 'df': df14.iloc[:28], 'C': 195, 'T': 3360, 'n': 29},
    {'name': '14-Oct 14:54', 'df': df14.iloc[:28], 'C': 177, 'T': 3240, 'n': 28},
    {'name': '14-Oct 14:52', 'df': df14.iloc[:27], 'C': 195, 'T': 3120, 'n': 27},
    {'name': '14-Oct 14:50', 'df': df14.iloc[:26], 'C': 191, 'T': 3000, 'n': 26},
    {'name': '14-Oct 14:48', 'df': df14.iloc[:25], 'C': 128, 'T': 2880, 'n': 25},
    {'name': '14-Oct 14:46', 'df': df14.iloc[:24], 'C': 191, 'T': 2760, 'n': 24},
    {'name': '14-Oct 14:44', 'df': df14.iloc[:23], 'C': 181, 'T': 2640, 'n': 23},
    {'name': '14-Oct 14:42', 'df': df14.iloc[:22], 'C': 191, 'T': 2520, 'n': 22},
    {'name': '14-Oct 14:40', 'df': df14.iloc[:21], 'C': 128, 'T': 2400, 'n': 21},
    {'name': '12-Oct 15:16', 'df': df12.iloc[:24], 'C': 190, 'T': 2760, 'n': 24},
    {'name': '12-Oct 15:14', 'df': df12.iloc[:23], 'C': 146, 'T': 2640, 'n': 23},
    {'name': '12-Oct 15:12', 'df': df12.iloc[:22], 'C': 153, 'T': 2520, 'n': 22},
    {'name': '12-Oct 15:10', 'df': df12.iloc[:21], 'C': 124, 'T': 2400, 'n': 21},
]

print("=== BÚSQUEDA DE RELACIONES EXACTAS ===")
for c in all_cases:
    df = c['df']
    T = c['T']
    n = c['n']
    C = c['C']
    
    gh = df['high'].max()
    gl = df['low'].min()
    rng = gh - gl
    
    first = df.iloc[0]
    last = df.iloc[-1]
    
    net = abs(last['close'] - first['open'])
    pos = (last['close'] - gl) / rng if rng > 0 else 0.5
    
    # Check if (T / C) has integer or simple rational forms
    ratio = T / C
    print(f"{c['name']:14s}: T={T:4d}, C={C:3d}, T/C={ratio:.4f}, C/n={C/n:.2f}, Rng={rng:6.2f}, Pos={pos:.3f}, Net={net:6.2f}")
