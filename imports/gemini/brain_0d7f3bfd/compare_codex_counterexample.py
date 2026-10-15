import json
from pathlib import Path

mat_path = Path(r"G:\trading\guias\analisis\C_matriz.json")
cases = json.loads(mat_path.read_text(encoding='utf-8'))['cases']

c_a = next(c for c in cases if c['START'] == '19:01:00' and c['END'] == '19:22:00')
c_b = next(c for c in cases if c['START'] == '19:02:00' and c['END'] == '19:22:00')

print("=== DEEP COMPARISON: [19:01, 19:22] (C=77) vs [19:02, 19:22] (C=50) ===")
print(f"{'Metric':<30} {'Range A [19:01] (C=77)':<25} {'Range B [19:02] (C=50)':<25} {'Difference':<15}")

metrics = [
    ('Bars (n)', c_a['bars'], c_b['bars']),
    ('Global High', c_a['high'], c_b['high']),
    ('Global Low', c_a['low'], c_b['low']),
    ('Range (H - L)', c_a['high'] - c_a['low'], c_b['high'] - c_b['low']),
    ('Start Open', float(c_a['OHLC'][0]['open']), float(c_b['OHLC'][0]['open'])),
    ('Start High', float(c_a['OHLC'][0]['high']), float(c_b['OHLC'][0]['high'])),
    ('Start Low', float(c_a['OHLC'][0]['low']), float(c_b['OHLC'][0]['low'])),
    ('Start Close', float(c_a['OHLC'][0]['close']), float(c_b['OHLC'][0]['close'])),
    ('End Close', float(c_a['OHLC'][-1]['close']), float(c_b['OHLC'][-1]['close'])),
    ('Net Displacement (EndC - StartO)', float(c_a['OHLC'][-1]['close']) - float(c_a['OHLC'][0]['open']), float(c_b['OHLC'][-1]['close']) - float(c_b['OHLC'][0]['open'])),
    ('Start Relative Pos (StartO - L)/R', (float(c_a['OHLC'][0]['open']) - c_a['low']) / (c_a['high'] - c_a['low']), (float(c_b['OHLC'][0]['open']) - c_b['low']) / (c_b['high'] - c_b['low'])),
    ('Total True Range Sum', sum(max(float(h['high']) - float(h['low']), abs(float(h['high']) - float(prev['close'])), abs(float(h['low']) - float(prev['close']))) for h, prev in zip(c_a['OHLC'][1:], c_a['OHLC'][:-1])),
                             sum(max(float(h['high']) - float(h['low']), abs(float(h['high']) - float(prev['close'])), abs(float(h['low']) - float(prev['close']))) for h, prev in zip(c_b['OHLC'][1:], c_b['OHLC'][:-1]))),
    ('Cumulative Volume', sum(float(r.get('volume', 0)) for r in c_a['OHLC']), sum(float(r.get('volume', 0)) for r in c_b['OHLC'])),
    ('Cumulative Ticks', sum(float(r.get('ticks', 0)) for r in c_a['OHLC']), sum(float(r.get('ticks', 0)) for r in c_b['OHLC']))
]

for name, val_a, val_b in metrics:
    diff = val_a - val_b if isinstance(val_a, (int, float)) else "N/A"
    diff_str = f"{diff:.4f}" if isinstance(diff, float) else str(diff)
    print(f"{name:<30} {val_a:<25.4f} {val_b:<25.4f} {diff_str:<15}")
