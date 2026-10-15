"""Audita las mediciones nativas de 1 s de n=20..40 y sus preregistros."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from analizar_C_fuente_vs_grafico import LANES, fit_lite
from analizar_C_frontera_1s import read as read_one_second
from analizar_C_frontera_1s_replicas import BASES, read as read_replica


ROOT = Path(__file__).resolve().parent
MANUAL = ROOT / "manual"
OUT_JSON = ROOT / "resultado_C_meseta_1s_conteos.json"
OUT_CSV = ROOT / "residuos_C_meseta_1s_conteos.csv"
BAR_COLUMNS = ("time", "open", "high", "low", "close", "Volume")
COMPARE_COLUMNS = ("open", "high", "low", "close", "Volume", *LANES)


def stamp(value: str) -> int:
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())


def main() -> None:
    prereg_paths = {
        "initial": ROOT / "C_1S_SALIDA_MESETA_PREREGISTRO.json",
        "gap_fill": ROOT / "C_1S_MESETA_HUECOS_PREREGISTRO.json",
        "replicas": ROOT / "C_FRONTERA_1S_REPLICAS_PREREGISTRO.json",
    }
    initial = json.loads(prereg_paths["initial"].read_text(encoding="utf-8"))
    gaps = json.loads(prereg_paths["gap_fill"].read_text(encoding="utf-8"))
    replicas = json.loads(prereg_paths["replicas"].read_text(encoding="utf-8"))
    start = stamp(initial["START_UTC"])
    assert start == stamp(gaps["START_UTC"]) == stamp(replicas["cases"][2]["START_UTC"])

    predicted: dict[int, tuple[float, str]] = {}
    prereg_for_n: dict[int, Path] = {}
    for n, value in initial["predictions_C"].items():
        predicted[int(n)] = (float(value), "preregistro_inicial")
        prereg_for_n[int(n)] = prereg_paths["initial"]
    for n in gaps["counts"]:
        predicted[int(n)] = (float(gaps["prediction_C"]), "preregistro_complementario")
        prereg_for_n[int(n)] = prereg_paths["gap_fill"]
    for case in replicas["cases"][2:]:
        predicted[int(case["bars"])] = (float(case["prediction_C"]), "replica_preregistrada")
        prereg_for_n[int(case["bars"])] = prereg_paths["replicas"]
    for n in range(31, 40):
        prereg_for_n[n] = prereg_paths["initial"]

    raw: dict[int, tuple[Path, Path, dict[int, dict[str, str]], dict[int, dict[str, str]]]] = {}
    for n in (20, 21):
        paths = (MANUAL / f"C_1s_r1404_n{n}_a.csv", MANUAL / f"C_1s_r1404_n{n}_b.csv")
        first, second = (read_replica(path) for path in paths)
        raw[n] = (paths[0], paths[1], first, second)
    for n in range(22, 41):
        paths = (MANUAL / f"C_1s_plateau_n{n}_a.csv", MANUAL / f"C_1s_plateau_n{n}_b.csv")
        first, second = (read_one_second(path) for path in paths)
        raw[n] = (paths[0], paths[1], first, second)

    records: list[dict[str, Any]] = []
    windows: dict[int, list[dict[str, float | int]]] = {}
    pair_mtimes_ns: dict[int, list[int]] = {}
    for n in range(20, 41):
        path_a, path_b, first, second = raw[n]
        common = sorted(set(first) & set(second))
        assert common, f"no repeated timestamps at n={n}"
        assert all(first[t][column] == second[t][column] for t in common for column in COMPARE_COLUMNS), f"unstable repeat at n={n}"
        end = start + n - 1
        assert all(t in second for t in range(start, end + 1)), f"missing native 1s range at n={n}"
        assert all(t in second for t in range(end + 1, end + 601)), f"missing 600s forward horizon at n={n}"

        window = [
            {key: (int(second[t][key]) if key == "time" else float(second[t][key])) for key in BAR_COLUMNS}
            for t in range(start, end + 1)
        ]
        assert len(window) == n
        windows[n] = window
        fits = fit_lite(second, step=1, period_seconds=1)
        values = [fit["C"] for fit in fits.values()]
        c_value = sum(values) / len(values)
        spread = max(values) - min(values)
        max_rmse = max(fit["rmse"] for fit in fits.values())
        min_pairs = min(fit["pairs"] for fit in fits.values())
        assert spread <= 1e-6, f"six Lite estimates disagree at n={n}: {spread}"
        assert max_rmse <= 1e-8 and min_pairs >= 5, f"poor EMA fit at n={n}"

        high = max(row["high"] for row in window)
        low = min(row["low"] for row in window)
        breakout = next(
            t for t in range(end + 1, end + 601)
            if float(second[t]["close"]) > high or float(second[t]["close"]) < low
        )
        bullish = float(second[breakout]["close"]) > high
        seed = float(second[end]["low" if bullish else "high"])
        state = dict.fromkeys(LANES, seed)
        alphas = {lane: 2 / (base * c_value + 1) for lane, base in BASES.items()}
        reconstruction_errors: list[float] = []
        visibility_errors = 0
        for t in range(end + 1, end + 601):
            for lane in LANES:
                state[lane] += alphas[lane] * (float(second[t]["close"]) - state[lane])
                visible = bool(second[t][lane])
                visibility_errors += visible != (t >= breakout)
                if visible:
                    reconstruction_errors.append(abs(state[lane] - float(second[t][lane])))
        max_reconstruction_error = max(reconstruction_errors)
        assert visibility_errors == 0 and max_reconstruction_error < 1e-8, f"seed/reconstruction mismatch at n={n}"

        prediction = predicted.get(n)
        if prediction is None and 31 <= n <= 39:
            predicted_value, prediction_source = None, "adaptive_gap_fill_no_pointwise_prediction"
        else:
            predicted_value, prediction_source = prediction if prediction else (None, "unregistered")
        prereg_path = prereg_for_n.get(n)
        prereg_mtime_ns = prereg_path.stat().st_mtime_ns if prereg_path else None
        file_mtimes_ns = [path.stat().st_mtime_ns for path in (path_a, path_b)]
        pair_mtimes_ns[n] = file_mtimes_ns
        files_after_prereg = all(value > prereg_mtime_ns for value in file_mtimes_ns) if prereg_mtime_ns is not None else None
        if prediction is not None or prediction_source == "adaptive_gap_fill_no_pointwise_prediction":
            assert files_after_prereg, f"data files predate their preregistration at n={n}"
        records.append({
            "n": n,
            "START_UTC": initial["START_UTC"],
            "END_UTC": datetime.fromtimestamp(end, datetime.fromisoformat("2026-10-14T00:00:00+00:00").tzinfo).isoformat().replace("+00:00", "Z"),
            "C_Lite_reconstructed": c_value,
            "prediction_C": predicted_value,
            "prediction_source": prediction_source,
            "prediction_residual": c_value - predicted_value if predicted_value is not None else None,
            "prediction_matches_1e-6": abs(c_value - predicted_value) <= 1e-6 if predicted_value is not None else None,
            "preregistration_file": str(prereg_path) if prereg_path else None,
            "preregistration_sha256": hashlib.sha256(prereg_path.read_bytes()).hexdigest() if prereg_path else None,
            "preregistration_last_write_utc": datetime.fromtimestamp(prereg_mtime_ns / 1e9, timezone.utc).isoformat() if prereg_mtime_ns else None,
            "measurement_pair_last_write_utc": [datetime.fromtimestamp(value / 1e9, timezone.utc).isoformat() for value in file_mtimes_ns],
            "measurement_files_after_preregistration": files_after_prereg,
            "six_curve_spread": spread,
            "max_EMA_RMSE": max_rmse,
            "min_fit_pairs": min_pairs,
            "max_reconstruction_error": max_reconstruction_error,
            "visibility_errors": visibility_errors,
            "repeat_cells": len(common) * len(COMPARE_COLUMNS),
            "range_high": high,
            "range_low": low,
            "range_width": high - low,
            "END_seed": seed,
            "breakout_timestamp": breakout,
            "breakout_direction": "up" if bullish else "down",
            "file_a_sha256": hashlib.sha256(path_a.read_bytes()).hexdigest(),
            "file_b_sha256": hashlib.sha256(path_b.read_bytes()).hexdigest(),
        })

    for n in range(20, 40):
        assert windows[n] == windows[n + 1][:n], f"OHLCV prefix mismatch n={n}->{n+1}"

    # Summarize input-only changes when C changes, without fitting a selector.
    by_n = {row["n"]: row for row in records}
    for n in range(21, 41):
        previous, current = windows[n - 1], windows[n]
        new_bar = current[-1]
        old_high = max(row["high"] for row in previous)
        old_low = min(row["low"] for row in previous)
        old_width = old_high - old_low
        old_volumes = [row["Volume"] for row in previous]
        by_n[n].update({
            "delta_C_from_previous_n": by_n[n]["C_Lite_reconstructed"] - by_n[n - 1]["C_Lite_reconstructed"],
            "entering_range_over_previous_range": (new_bar["high"] - new_bar["low"]) / old_width if old_width else None,
            "new_high": new_bar["high"] > old_high,
            "new_low": new_bar["low"] < old_low,
            "high_extension_over_previous_range": max(0.0, new_bar["high"] - old_high) / old_width if old_width else None,
            "low_extension_over_previous_range": max(0.0, old_low - new_bar["low"]) / old_width if old_width else None,
            "entering_volume_over_previous_mean": new_bar["Volume"] / (sum(old_volumes) / len(old_volumes)) if old_volumes and sum(old_volumes) else None,
            "entering_close_location": (new_bar["close"] - new_bar["low"]) / (new_bar["high"] - new_bar["low"]) if new_bar["high"] != new_bar["low"] else None,
        })

    gap_rows = [row for row in records if row["prediction_source"] == "preregistro_complementario"]
    assert len(gap_rows) == len(gaps["counts"]) == 7
    initial_rows = [row for row in records if row["prediction_source"] == "preregistro_inicial"]
    assert len(initial_rows) == 3
    adaptive_after_n40 = all(min(pair_mtimes_ns[n]) > max(pair_mtimes_ns[40]) for n in range(31, 40))
    adaptive_ascending = all(max(pair_mtimes_ns[n]) < min(pair_mtimes_ns[n + 1]) for n in range(31, 39))
    n33_saved_after_n39 = min(pair_mtimes_ns[33]) > max(pair_mtimes_ns[39])
    assert adaptive_after_n40

    # A later three-export remeasurement of n=33 is retained as a stability check.
    n33_repeats = {
        suffix: read_one_second(MANUAL / f"C_1s_plateau_n33_{suffix}.csv")
        for suffix in ("a", "b", "pending")
    }
    n33_repeat_checks = []
    for left, right in (("a", "b"), ("a", "pending"), ("b", "pending")):
        left_rows, right_rows = n33_repeats[left], n33_repeats[right]
        common = sorted(set(left_rows) & set(right_rows))
        mismatches = sum(left_rows[t][column] != right_rows[t][column] for t in common for column in COMPARE_COLUMNS)
        n33_repeat_checks.append({
            "files": [left, right], "common_timestamps": len(common),
            "compared_cells": len(common) * len(COMPARE_COLUMNS), "mismatches": mismatches,
        })
        assert common and mismatches == 0
    n33_repeat_fits = {
        suffix: {
            "C_by_lane": {lane: fit["C"] for lane, fit in fit_lite(rows, step=1, period_seconds=1).items()},
            "max_RMSE": max(fit["rmse"] for fit in fit_lite(rows, step=1, period_seconds=1).values()),
        }
        for suffix, rows in n33_repeats.items()
    }
    n33_repeat_c = [sum(result["C_by_lane"].values()) / len(LANES) for result in n33_repeat_fits.values()]
    assert max(n33_repeat_c) - min(n33_repeat_c) <= 1e-6
    out = {
        "status": "native_1s_20_to_40_audited_against_preregistration",
        "start_utc": initial["START_UTC"],
        "master_dataset_included": False,
        "scope": "Supplementary same-session 1s sequence, not one of the 179 master cases. C is re-estimated independently from six Lite EMA lanes; all windows are exact OHLCV prefixes. Seven gap-count predictions were preregistered after exploratory n=32..40 observations; earlier 25/30/40 predictions were separately preregistered. This is not an independent episode test.",
        "counts": [row["n"] for row in records],
        "all_prefixes_verified": True,
        "gap_prediction_count": len(gap_rows),
        "gap_predictions_exact_within_1e-6": sum(row["prediction_matches_1e-6"] for row in gap_rows),
        "initial_prediction_count": len(initial_rows),
        "initial_predictions_exact_within_1e-6": sum(row["prediction_matches_1e-6"] for row in initial_rows),
        "C_1_count_n21_to_40": sum(abs(row["C_Lite_reconstructed"] - 1) <= 1e-6 for row in records if 21 <= row["n"] <= 40),
        "C_2_count_n21_to_40": sum(abs(row["C_Lite_reconstructed"] - 2) <= 1e-6 for row in records if 21 <= row["n"] <= 40),
        "max_six_curve_spread": max(row["six_curve_spread"] for row in records),
        "max_EMA_RMSE": max(row["max_EMA_RMSE"] for row in records),
        "max_reconstruction_error": max(row["max_reconstruction_error"] for row in records),
        "total_visibility_errors": sum(row["visibility_errors"] for row in records),
        "all_preregistered_pairs_saved_after_preregistration": all(
            row["measurement_files_after_preregistration"]
            for row in records if row["measurement_files_after_preregistration"] is not None
        ),
        "adaptive_counts_31_to_39_saved_after_n40_failure": adaptive_after_n40,
        "adaptive_counts_31_to_39_saved_in_ascending_order": adaptive_ascending,
        "n33_pair_saved_after_n39": n33_saved_after_n39,
        "n33_later_repeat": {
            "file_last_write_utc": {
                suffix: datetime.fromtimestamp((MANUAL / f"C_1s_plateau_n33_{suffix}.csv").stat().st_mtime, timezone.utc).isoformat()
                for suffix in ("a", "b", "pending")
            },
            "matches": n33_repeat_checks,
            "fits": n33_repeat_fits,
            "C_means": {suffix: n33_repeat_c[index] for index, suffix in enumerate(("a", "b", "pending"))},
            "spread": max(n33_repeat_c) - min(n33_repeat_c),
        },
        "preregistration_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in prereg_paths.items()},
        "rows": records,
        "residual_csv": str(OUT_CSV),
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    import csv
    fields = list(records[0])
    for row in records:
        fields.extend(key for key in row if key not in fields)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    print(json.dumps({
        "status": out["status"],
        "gap_prediction_count": out["gap_prediction_count"],
        "gap_predictions_exact_within_1e-6": out["gap_predictions_exact_within_1e-6"],
        "initial_prediction_count": out["initial_prediction_count"],
        "initial_predictions_exact_within_1e-6": out["initial_predictions_exact_within_1e-6"],
        "C_1_count_n21_to_40": out["C_1_count_n21_to_40"],
        "C_2_count_n21_to_40": out["C_2_count_n21_to_40"],
        "max_six_curve_spread": out["max_six_curve_spread"],
        "max_EMA_RMSE": out["max_EMA_RMSE"],
        "max_reconstruction_error": out["max_reconstruction_error"],
        "total_visibility_errors": out["total_visibility_errors"],
        "adaptive_counts_31_to_39_saved_after_n40_failure": out["adaptive_counts_31_to_39_saved_after_n40_failure"],
        "adaptive_counts_31_to_39_saved_in_ascending_order": out["adaptive_counts_31_to_39_saved_in_ascending_order"],
        "n33_pair_saved_after_n39": out["n33_pair_saved_after_n39"],
        "n33_later_repeat": out["n33_later_repeat"],
        "series": [{k: row.get(k) for k in ("n", "C_Lite_reconstructed", "prediction_C", "prediction_source", "delta_C_from_previous_n")} for row in records],
        "outputs": {"json": str(OUT_JSON), "csv": str(OUT_CSV)},
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
