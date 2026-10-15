import json
from pathlib import Path

files = [
    'Lite_1903_192500_1m_comparacion.json',
    'Lite_1904_192500_1m_comparacion.json',
    'Lite_1904_192600_1m_comparacion.json',
    'Lite_1904_192700_1m_comparacion.json',
    'Lite_1904_192800_1m_comparacion.json',
]

for f in files:
    p = Path('G:/trading/guias/analisis') / f
    if p.exists():
        d = json.load(open(p, encoding='utf-8-sig'))
        c_val = sum(d['Lite_C_assuming_unrounded_family'].values()) / 6
        s_utc = d['START_UTC']
        e_utc = d['END_UTC']
        print(f"{f:38s} | START={s_utc} | END={e_utc} | C={c_val:12.6f}")
