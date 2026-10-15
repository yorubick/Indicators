import json

with open(r"G:\trading\guias\analisis\master_all_C_cases.json", "r", encoding="utf-8") as f:
    master = json.load(f)

cases = master["cases"]
short_cases = [c for c in cases if c.get("bars") < 21]
for c in short_cases:
    if c.get("C_Lite") is None:
        dt = c["dt"]
        n = c["bars"]
        pred_cont = max(dt, n * dt * 10 / 183)
        print("Char only short case:", c["id"], "n=", n, "dt=", dt, "C=", c["C"], "pred_cont=", pred_cont, "interval=", c.get("C_Character_interval"))
