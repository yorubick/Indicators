from pathlib import Path
import datetime

path = Path(r"G:\trading\guias\analisis\manual\C_escala50_base_a.csv")
lines = path.read_text(encoding="utf-8").strip().splitlines()
rows = []
for line in lines[1:]:
    parts = line.split(",")
    rows.append({
        "time": int(parts[0]),
        "open": float(parts[1]),
        "high": float(parts[2]),
        "low": float(parts[3]),
        "close": float(parts[4]),
        "lane_a_fast": float(parts[6]) if len(parts) > 6 and parts[6] else None
    })

t_start = int(datetime.datetime(2026, 10, 12, 19, 2, tzinfo=datetime.timezone.utc).timestamp())
t_end = int(datetime.datetime(2026, 10, 12, 19, 22, tzinfo=datetime.timezone.utc).timestamp())

window = [r for r in rows if t_start <= r["time"] <= t_end]
r_high = max(r["high"] for r in window)
r_low = min(r["low"] for r in window)
end_row = [r for r in rows if r["time"] == t_end][0]

print(f"Window High: {r_high}, Low: {r_low}")
print(f"End Low: {end_row['low']}, High: {end_row['high']}")

C = 50.0
delta = 60.0
base_fast_a = 24.0
alpha = 2.0 / (base_fast_a * C / delta + 1.0)

# Track both states
state_bull = end_row["low"]
state_bear = end_row["high"]

post_end = [r for r in rows if r["time"] > t_end]
for r in post_end:
    state_bull += alpha * (r["close"] - state_bull)
    state_bear += alpha * (r["close"] - state_bear)
    
    if r["close"] > r_high or r["close"] < r_low:
        up = r["close"] > r_high
        chosen = state_bull if up else state_bear
        official = r["lane_a_fast"]
        diff = abs(chosen - official)
        print(f"First breakout at {r['time']}: chosen={chosen}, official={official}, diff={diff}")
        break
