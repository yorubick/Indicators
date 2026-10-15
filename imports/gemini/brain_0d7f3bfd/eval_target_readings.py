import csv
from datetime import datetime

with open('G:/trading/guias/analisis/C_barrido_15s_start1854_estabilizado.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

by_time = {int(r['time']): {k: float(r[k]) for k in ('open', 'high', 'low', 'close')} for r in rows}

def ts(t_str):
    return int(datetime.fromisoformat(f'2026-10-12T{t_str}+00:00').timestamp())

target_l3a = 30866.77
target_l3b = 30866.63
t_target = ts('19:26:45')

def eval_candidate(end_str, c_val, note=""):
    t_end = ts(end_str)
    seed = by_time[t_end]['low']
    # Exact Lite formula
    len_a = (72.0 / 3.0) * (c_val / 15.0)
    len_b = (89.0 / 3.0) * (c_val / 15.0)
    alpha_a = 2.0 / (len_a + 1.0)
    alpha_b = 2.0 / (len_b + 1.0)
    
    va, vb = seed, seed
    for t in range(t_end + 15, t_target + 15, 15):
        cl = by_time[t]['close']
        va += alpha_a * (cl - va)
        vb += alpha_b * (cl - vb)
    
    print(f"END={end_str} | Seed={seed} | C={c_val:5.1f} | L3A={va:8.4f} (err={va-target_l3a:+.4f}) | L3B={vb:8.4f} (err={vb-target_l3b:+.4f}) | {note}")

print(f"TARGET AT 19:26:45: Lane 3 A = {target_l3a:.2f}, Lane 3 B = {target_l3b:.2f}\n")

eval_candidate('19:20:00', 88.0, "END 19:20, C=88")
eval_candidate('19:20:00', 88.1, "END 19:20, C=88.1 (optimum)")
eval_candidate('19:20:00', 67.0, "END 19:20, C=67")
eval_candidate('19:20:00', 62.0, "END 19:20, C=62")
eval_candidate('19:20:00', 106.0, "END 19:20, C=106")
eval_candidate('19:20:00', 118.0, "END 19:20, C=118")
print()
eval_candidate('19:23:30', 61.0, "END 19:23:30, C=61")
eval_candidate('19:23:30', 67.0, "END 19:23:30, C=67")
eval_candidate('19:23:30', 88.0, "END 19:23:30, C=88")
print()
eval_candidate('19:23:45', 61.0, "END 19:23:45, C=61")
eval_candidate('19:23:45', 66.9, "END 19:23:45, C=66.9")
eval_candidate('19:23:45', 67.0, "END 19:23:45, C=67")
eval_candidate('19:23:45', 88.0, "END 19:23:45, C=88")
