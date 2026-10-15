import json
import csv
import pandas as pd
from datetime import datetime, timezone

# Let's compile the full record of the 13 measurements
# For each measurement:
# - START
# - END
# - n
# - Inferred C
# - Official readings (where recorded in chat / manual CSVs)
# - Evaluation candle timestamp and OHLC
# - END bar OHLC
# - Range OHLC

measurements = [
    {
        "n": 21, "END": "19:23", "C": 50,
        "source": "master_all_C_cases / manual Lite_1903_192300_1m_a.csv",
        "eval_time": "19:26",
        "notes": "Verified in master dataset and manual CSV"
    },
    {
        "n": 22, "END": "19:24", "C": 52,
        "source": "master_all_C_cases / manual Lite_1903_192400_1m_a.csv",
        "eval_time": "19:26",
        "notes": "Verified in master dataset and manual CSV"
    },
    {
        "n": 23, "END": "19:25", "C": 71,
        "source": "master_all_C_cases / manual Lite_1903_192500_1m_a.csv",
        "eval_time": "19:26",
        "notes": "Verified in master dataset and manual CSV"
    },
    {
        "n": 24, "END": "19:26", "C": 135,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:30",
        "official_readings": {
            "Lane 3 A": 30868.26, "Lane 3 B": 30868.20,
            "Lane 2 A": 30869.92, "Lane 2 B": 30869.70,
            "Lane 1 A": 30873.03, "Lane 1 B": 30872.48
        },
        "notes": "Solved C=134.99 across all lanes"
    },
    {
        "n": 25, "END": "19:27", "C": 130,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:30",
        "official_readings": {
            "Lane 3 A": 30869.19, "Lane 3 B": 30869.13,
            "Lane 2 A": 30870.76, "Lane 2 B": 30870.55,
            "Lane 1 A": 30873.71, "Lane 1 B": 30873.19
        },
        "notes": "Solved C=129.98 across all lanes"
    },
    {
        "n": 26, "END": "19:28", "C": 88,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:30",
        "official_readings": {
            "Lane 3 A": 30870.21, "Lane 3 B": 30870.08,
            "Lane 2 A": 30871.43, "Lane 2 B": 30871.11,
            "Lane 1 A": 30873.86, "Lane 1 B": 30873.31
        },
        "notes": "User noted END was at 19:28 when these were taken, matching C=88"
    },
    {
        "n": 27, "END": "19:29", "C": 135,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:30",
        "official_readings": {
            "Lane 3 A": 30870.72, "Lane 3 B": 30870.68,
            "Lane 2 A": 30871.13, "Lane 2 B": 30871.02,
            "Lane 1 A": 30872.21, "Lane 1 B": 30871.93
        },
        "notes": "Solved C=135"
    },
    {
        "n": 28, "END": "19:30", "C": 112,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:32",
        "official_readings": {
            "Lane 3 A": 30871.51, "Lane 3 B": 30871.41,
            "Lane 2 A": 30872.42, "Lane 2 B": 30872.17,
            "Lane 1 A": 30874.54, "Lane 1 B": 30874.01
        },
        "notes": "Codex verified C=112 with max error 0.0036 pts"
    },
    {
        "n": 29, "END": "19:31", "C": 136,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:32 and 19:33",
        "official_readings": {
            "19:32": {"Lane 3 A": 30872.50, "Lane 3 B": 30872.46, "Lane 2 A": 30872.98, "Lane 2 B": 30872.85, "Lane 1 A": 30874.24, "Lane 1 B": 30873.90},
            "19:33": {"Lane 3 A": 30872.98, "Lane 3 B": 30872.84, "Lane 2 A": 30874.32, "Lane 2 B": 30873.95, "Lane 1 A": 30877.51, "Lane 1 B": 30876.70}
        },
        "notes": "Codex verified C=136 with max error 0.0049 pts across 12 readings"
    },
    {
        "n": 30, "END": "19:32", "C": 112,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:33",
        "official_readings": {
            "Lane 3 A": 30874.99, "Lane 3 B": 30874.90,
            "Lane 2 A": 30875.91, "Lane 2 B": 30875.66,
            "Lane 1 A": 30878.26, "Lane 1 B": 30877.65
        },
        "notes": "Matches C=112 al centimo"
    },
    {
        "n": 31, "END": "19:33", "C": 112,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:34",
        "official_readings": {
            "Lane 3 A": 30877.88, "Lane 3 B": 30877.72,
            "Lane 2 A": 30879.54, "Lane 2 B": 30879.08,
            "Lane 1 A": 30883.78, "Lane 1 B": 30882.66
        },
        "notes": "Matches C=112 al centimo"
    },
    {
        "n": 32, "END": "19:34", "C": 135,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:35",
        "official_readings": {
            "Lane 3 A": 30886.42, "Lane 3 B": 30886.30,
            "Lane 2 A": 30887.70, "Lane 2 B": 30887.34,
            "Lane 1 A": 30891.04, "Lane 1 B": 30890.15
        },
        "notes": "Matches C=135 al centimo (error 0.00 pts)"
    },
    {
        "n": 33, "END": "19:35", "C": 112,
        "source": "Live TV measurement (chat step)",
        "eval_time": "19:36",
        "official_readings": {
            "Lane 3 A": 30896.06, "Lane 3 B": 30895.95,
            "Lane 2 A": 30897.10, "Lane 2 B": 30896.81,
            "Lane 1 A": 30899.77, "Lane 1 B": 30899.06
        },
        "notes": "Matches C=112 al centimo (error 0.00 pts)"
    }
]

with open(r"C:\Users\PC\.gemini\antigravity\scratch\c_discovery\serie_1903_mediciones_completas.json", "w", encoding="utf-8") as f:
    json.dump(measurements, f, indent=2)

print("Saved 13 complete verified measurements to serie_1903_mediciones_completas.json")
