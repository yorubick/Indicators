import json
import pandas as pd
import numpy as np

# Load 14:00 to 14:50
d = json.load(open('data/ohlcv_2m_14oct_1400_1450.json'))

c52 = {
    "time": "2026-10-14T14:52:00.000Z",
    "open": 30453.25,
    "high": 30453.50,
    "low": 30417.75,
    "close": 30418.50,
    "volume": 3861
}

c54 = {
    "time": "2026-10-14T14:54:00.000Z",
    "open": 30418.25,
    "high": 30456.00,
    "low": 30418.25,
    "close": 30454.75,
    "volume": 2637
}

full_data = d + [c52, c54]
with open('data/ohlcv_2m_14oct_1400_1454.json', 'w') as f:
    json.dump(full_data, f, indent=2)

print(f"Dataset created with {len(full_data)} bars (14:00 to 14:54).")
