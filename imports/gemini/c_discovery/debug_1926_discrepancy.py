import csv
from datetime import datetime, timezone

# Load Lite_1903_192300_1m_b.csv
csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = {}
with open(csv_path, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rows[int(row["time"])] = row

# Timestamps
t_1923 = int(datetime(2026, 10, 12, 19, 23, tzinfo=timezone.utc).timestamp())
t_1924 = int(datetime(2026, 10, 12, 19, 24, tzinfo=timezone.utc).timestamp())
t_1925 = int(datetime(2026, 10, 12, 19, 25, tzinfo=timezone.utc).timestamp())
t_1926 = int(datetime(2026, 10, 12, 19, 26, tzinfo=timezone.utc).timestamp())

print("Row 19:23:", rows[t_1923])
print("Row 19:24:", rows[t_1924])
print("Row 19:25:", rows[t_1925])
print("Row 19:26:", rows[t_1926])

# In auditar_C_escala_50_completa.py:
# What was the seed used by the official indicator?
# Let's check auditar_C_ancla_completa.py or similar to see how C_Lite was fitted!
