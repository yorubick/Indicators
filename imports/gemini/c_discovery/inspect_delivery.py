import csv

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"

rows = []
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        bull = r.get("Bull delivery active", "")
        bear = r.get("Bear delivery active", "")
        if bull not in ["", "0", "0.0"] or bear not in ["", "0", "0.0"]:
            rows.append((r["time"], bull, bear))

print(f"Total rows with active delivery: {len(rows)}")
for t, bull, bear in rows[:20]:
    print(f"Time: {t} | Bull delivery: {bull} | Bear delivery: {bear}")
