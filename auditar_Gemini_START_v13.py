"""Contrast the supplied v1.3 report against existing v1.2 observations.

No new TradingView measurements and no fitting of thresholds or C models.
"""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
master = json.loads((ROOT / "master_all_C_cases.json").read_text(encoding="utf-8"))
cases = master["cases"]
selected = []
for case in cases:
    if case["dt"] != 60 or not case["START"].startswith("2026-10-12T19:"):
        continue
    start, end = case["START"][11:19], case["END"][11:19]
    if start not in {"19:01:00", "19:02:00", "19:03:00"}:
        continue
    if end not in {"19:21:00", "19:22:00", "19:23:00", "19:24:00", "19:25:00"}:
        continue
    rows = case["OHLCV"]
    hi = max(x["high"] for x in rows)
    lo = min(x["low"] for x in rows)
    first = rows[0]
    selected.append({
        "id": case["id"], "START": start, "END": end,
        "n": len(rows), "C_Lite": case["C_Lite"], "high": hi, "low": lo,
        "first_bar": first,
        "start_close_position_in_global_range": (first["close"] - lo) / (hi - lo),
        "first_body_points": first["close"] - first["open"],
        "first_bar_range_points": first["high"] - first["low"],
        "first_20_close_mean": sum(x["close"] for x in rows[:20]) / 20,
        "global_high_first_index": next(i for i,x in enumerate(rows) if x["high"] == hi),
        "global_low_first_index": next(i for i,x in enumerate(rows) if x["low"] == lo),
    })

reported = {
    "192300": [30865.83, 30865.56, 30868.02, 30867.50, 30870.90, 30870.38],
    "192400": [30867.03, 30866.89, 30868.30, 30867.97, 30870.62, 30870.12],
    "192500": [30867.37, 30867.30, 30868.05, 30867.87, 30869.65, 30869.24],
}
columns = ["Lane 3 A", "Lane 3 B", "Lane 2 A", "Lane 2 B", "Lane 1 A", "Lane 1 B"]
stamp = int(datetime(2026,10,12,19,26,tzinfo=timezone.utc).timestamp())
curve_checks = []
for end, values in reported.items():
    path = ROOT / "manual" / f"Lite_1903_{end}_1m_b.csv"
    with path.open(encoding="utf-8-sig", newline="") as stream:
        row = next(r for r in csv.DictReader(stream) if int(float(r["time"])) == stamp)
    measured = [float(row[c]) for c in columns]
    curve_checks.append({"file": str(path), "timestamp": stamp,
        "reported": values, "old_v12_measured": measured,
        "match_after_cent_rounding": all(round(a,2) == b for a,b in zip(measured,values)),
        "absolute_differences": [abs(a-b) for a,b in zip(measured,values)]})

def get(start, end):
    return next(c for c in cases if c["dt"] == 60
        and c["START"].startswith("2026-10-12T" + start)
        and c["END"].startswith("2026-10-12T" + end))

a, b = get("19:01:00", "19:22:00"), get("19:02:00", "19:22:00")
result = {
    "scope": "Local audit of historical Lite v1.2 exports. New v1.3 version not independently measured.",
    "curve_checks_at_1926": curve_checks,
    "prefix_cases": sorted(selected, key=lambda x:(x["START"], x["END"])),
    "fixed_END_suffix_control": {
        "longer_id": a["id"], "shorter_id": b["id"],
        "complete_shared_OHLCV_suffix_identical": a["OHLCV"][1:] == b["OHLCV"],
        "longer_C": a["C_Lite"], "shorter_C": b["C_Lite"],
        "removed_bar": a["OHLCV"][0],
    },
    "limitations": [
        "Changing START changes count, prefix, and initialization jointly.",
        "Equal range extrema rule out a function of extrema alone, not their involvement.",
        "Different C at n=21 rules out a rule determined by count alone.",
        "First-20 mean and normalized START positions are diagnostic descriptors, not an inferred C formula.",
        "Cent-rounded curve agreement does not prove global or intrabar equivalence.",
    ],
}
out = ROOT / "Gemini_START_v13_auditoria.json"
out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"output":str(out), "curves_cent_matches":[x["match_after_cent_rounding"] for x in curve_checks],
    "suffix_check":result["fixed_END_suffix_control"], "cases":selected}, indent=2, ensure_ascii=False))
