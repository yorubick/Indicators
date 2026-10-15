import csv, json, datetime
from pathlib import Path

# Load all cases from C_barrido_ampliado.json and C_sensibilidad_15s.json
sens_15s = json.load(open('G:/trading/guias/analisis/C_sensibilidad_15s.json', encoding='utf-8'))
barrido = json.load(open('G:/trading/guias/analisis/C_barrido_ampliado.json', encoding='utf-8'))

# Let's inspect all cases where END = 19:20:00, dt = 15s
cases = {}
for c in barrido['cases']:
    cases[c['START_UTC']] = c['C']

print(f"{'START':10s} | {'C':5s} | {'Bars to END':12s} | {'Duration s':10s}")
for s in sorted(cases.keys()):
    c = cases[s]
    # parse time
    h, m, sec = map(int, s.split(':'))
    t_start = h*3600 + m*60 + sec
    t_end = 19*3600 + 20*60
    dur = t_end - t_start
    bars = dur // 15 + 1
    print(f"{s:10s} | {c:5d} | {bars:12d} | {dur:10d}")
