import csv
from datetime import datetime, timezone

csv_path = r"G:\trading\guias\analisis\manual\Lite_1903_192300_1m_b.csv"
rows = []
with open(csv_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        t = int(r["time"])
        dt_utc = datetime.fromtimestamp(t, timezone.utc)
        if "2026-10-12" in str(dt_utc) and "19:" in str(dt_utc):
            rows.append({
                "time": t,
                "utc": dt_utc.strftime("%H:%M"),
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
                "volume": float(r["Volume"]) if "Volume" in r and r["Volume"] else 0.0
            })

print(f"Loaded {len(rows)} bars for 19:xx on 2026-10-12:")
for r in rows:
    if "19:00" <= r["utc"] <= "19:28":
        body = r["close"] - r["open"]
        rng = r["high"] - r["low"]
        print(f"{r['utc']} | O={r['open']:8.2f} H={r['high']:8.2f} L={r['low']:8.2f} C={r['close']:8.2f} V={r['volume']:4.0f} | body={body:+5.2f} rng={rng:4.2f}")
