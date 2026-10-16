#!/usr/bin/env python3
"""Audit the 16-Oct-2026 TradingView Character Tree Auto Balanced M5 exports.

The Auto START times were read from the variable left edge of each orange range box,
using the screenshot time-axis labels. CSVs do not expose that box boundary as a field.
This script computes the OHLC/cloud observations and invariance checks from the exports.
"""
from __future__ import annotations
import csv
import datetime as dt
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DAY = dt.date(2026, 10, 12)
CASES = [
    ("w1429H", "CT_auto_1422_w1429H.csv", "14:29", 30906.00, "14:02"),
    ("w1443H", "CT_auto_1422_w1443H.csv", "14:43", 30911.25, "13:56"),
    ("w1448H", "CT_auto_1422_w1448H.csv", "14:48", 30921.25, "13:49"),
    ("w1426L", "CT_auto_1422_w1426L.csv", "14:26", 30859.00, "14:02"),
]
CLOUDS = [
    "Slow cloud", "Slow cloud boundary", "Middle cloud", "Middle cloud boundary",
    "Fast cloud", "Fast cloud boundary", "Extra cloud 1", "Extra cloud 1 boundary",
    "Extra cloud 2", "Extra cloud 2 boundary",
]
LANES = ["Lane 3 A", "Lane 3 B", "Lane 2 A", "Lane 2 B", "Lane 1 A", "Lane 1 B"]


def read_rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def timestamp(row: dict[str, str]) -> dt.datetime:
    return dt.datetime.fromtimestamp(int(row["time"]), dt.timezone.utc)


def by_minute(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {timestamp(row).strftime("%Y-%m-%d %H:%M"): row for row in rows}


def is_day(key: str) -> bool:
    return key.startswith(DAY.isoformat() + " ")


def main() -> None:
    case_maps: list[dict[str, dict[str, str]]] = []
    summary: list[list[object]] = []
    for case, filename, wick, price, start in CASES:
        rows = read_rows(filename)
        data = by_minute(rows)
        case_maps.append(data)
        start_row = data[f"{DAY.isoformat()} {start}"]
        wick_row = data[f"{DAY.isoformat()} {wick}"]
        first_cloud = next((row for row in rows if timestamp(row).date() == DAY and any(row[c].strip() for c in CLOUDS)), None)
        first_cloud_time = timestamp(first_cloud).strftime("%H:%M") if first_cloud else ""
        first_middle = first_cloud["Middle cloud"] if first_cloud and first_cloud["Middle cloud"].strip() else ""
        clouds_blank = all(not wick_row[column].strip() for column in CLOUDS)
        duration = int((dt.datetime.strptime("14:22", "%H:%M") - dt.datetime.strptime(start, "%H:%M")).total_seconds() / 60)
        summary.append([
            case, filename, wick, f"{price:.2f}", start, duration,
            "/".join(start_row[c] for c in ("open", "high", "low", "close")),
            "/".join(wick_row[c] for c in ("open", "high", "low", "close")),
            clouds_blank, first_cloud_time, first_middle,
            f"CT_auto_1422_{case}_cruceta.png",
        ])

    with (ROOT / "CT_auto_M5_resumen.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["caso", "archivo_csv", "mecha_utc", "precio_mecha", "inicio_auto_utc", "duracion_min", "OHLC_primera_vela", "OHLC_mecha", "clouds_CT_vacios_en_mecha", "primer_cloud_utc", "middle_cloud_primero", "captura_cruceta"])
        writer.writerows(summary)

    common = set(case_maps[0])
    for data in case_maps[1:]:
        common.intersection_update(data)
    lite_rows = [key for key in common if is_day(key) and any(case_maps[0][key][c].strip() for c in LANES)]
    lite_mismatches = 0
    for key in lite_rows:
        if any(len({data[key][col].strip() for data in case_maps}) > 1 for col in LANES):
            lite_mismatches += 1

    manual = by_minute(read_rows("CT_manual_1400_1422.csv"))
    auto = case_maps[0]
    compare_keys = [key for key in (set(auto) & set(manual)) if is_day(key) and key[11:16] >= "14:00"]
    comparison = []
    for col in CLOUDS:
        diffs = []
        exact = 0
        only_auto = only_manual = 0
        for key in compare_keys:
            av, mv = auto[key][col].strip(), manual[key][col].strip()
            if not av and mv:
                only_manual += 1
                continue
            if av and not mv:
                only_auto += 1
                continue
            if not av or not mv:
                continue
            delta = abs(float(av) - float(mv))
            diffs.append(delta)
            exact += delta < 5e-7
        comparison.append([col, len(diffs), exact, only_auto, only_manual, statistics.mean(diffs) if diffs else "", max(diffs) if diffs else ""])
    with (ROOT / "CT_auto_M5_manual_1400_comparacion.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["columna_CT", "muestras_comparadas", "coincidencias_exactas", "solo_auto", "solo_manual", "error_abs_medio_pts", "error_abs_max_pts"])
        writer.writerows(comparison)

    print(f"Lite: {len(lite_rows)} timestamps comunes con datos; mismatches={lite_mismatches}")
    for row in summary:
        print(f"{row[0]}: Auto START={row[4]}, rango={row[5]}m, vela Point2 CT vacío={row[8]}, primer cloud={row[9]}")
    print("Manual comparison uses the earlier 14:00-14:22 range; it is not equivalent to Auto START 14:02.")


if __name__ == "__main__":
    main()

