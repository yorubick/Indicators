import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    d = json.load(f)

cases_n21_60s = [c for c in d["cases"] if c.get("bars") == 21 and c.get("dt") == 60 and c.get("C_Lite") is not None]

print(f"Total n=21, dt=60s cases: {len(cases_n21_60s)}")
for c in cases_n21_60s:
    print(f"{c['id'][:28]} | START={c['START'][11:19]} END={c['END'][11:19]} | C={c['C_Lite']:.1f}")
